/*
 * Copyright (c) 2022, NVIDIA CORPORATION.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "common/check.h"
#include "lookup/impl/embedding_collection_adapter.h"

namespace sok {

template <typename DType>
__global__ static void UniqueReverseKernel(DType** unique_output, uint64_t* reverse_ids,
                                           uint64_t num, DType** output) {
  uint64_t id = threadIdx.x + blockIdx.x * blockDim.x;
  if (id < num) {
    output[id] = unique_output[reverse_ids[id]];
  }
  return;
}

template <typename KeyType, typename OffsetType, typename DType>
__global__ static void TFAdapterKernel(float** data, int* dimensions, int* scales,
                                       int* id_space_to_local_index, const KeyType* keys,
                                       size_t num_keys, const OffsetType* id_space_offset,
                                       size_t num_id_space_offset, const int* id_space,
                                       DType** outputs) {
  size_t offset = 0;
  for (int i = 0; i < num_id_space_offset; ++i) {
    int index = id_space_to_local_index[id_space[i]];
    float* input = data[index];
    int dimension = dimensions[index];
    const KeyType* key = keys + id_space_offset[i];
    DType* output = outputs[i];
    size_t num_keys = id_space_offset[i + 1] - id_space_offset[i];
    int scale = scales[index];

    size_t thread_cnt = blockDim.x * gridDim.x;
    size_t thread_idx = blockDim.x * blockIdx.x + threadIdx.x;
    // size_t items = num_keys * dimension;
    // for (size_t j = thread_idx; j < items; j += thread_cnt) {
    for (size_t j = thread_idx; j < num_keys; j += thread_cnt) {
      outputs[offset + j] = input + key[j] / scale * dimension;
      // size_t row = key[j / dimension];
      // size_t col = j % dimension;
      // output[j] = input[row * dimension + col];
      // output[j] = 0;
    }
    offset += num_keys;
  }
}

template <typename KeyType, typename OffsetType, typename DType>
TFAdapter<KeyType, OffsetType, DType>::TFAdapter()
    : d_data_(nullptr),
      d_dimensions_(nullptr),
      d_id_space_to_local_index_(nullptr),
      d_scale_(nullptr),
      stream_(0) {
  int device;
  CUDACHECK(cudaGetDevice(&device));
  CUDACHECK(cudaDeviceGetAttribute(&sm_count_, cudaDevAttrMultiProcessorCount, device));
}

template <typename KeyType, typename OffsetType, typename DType>
void TFAdapter<KeyType, OffsetType, DType>::set(std::vector<float*>& vars,
                                                std::vector<int>& dimensions,
                                                std::vector<int>& scale, cudaStream_t stream) {
  std::vector<float*> data;
  std::vector<int> id_space;
  for (int i = 0; i < vars.size(); ++i) {
    float* input = vars[i];
    data.push_back(input);
    id_space.push_back(i);
  }

  if (data_.size() == data.size()) {
    bool skip = true;
    for (int i = 0; i < data.size(); ++i) {
      if (data_[i] != data[i]) {
        skip = false;
        break;
      }
    }
    if (skip) {
      return;
    }
  }

  data_ = data;
  dimensions_ = dimensions;
  scale_ = scale;
  stream_ = stream;

  id_space_to_local_index_.resize(vars.size(), -1);
  for (int i = 0; i < id_space.size(); ++i) {
    id_space_to_local_index_[id_space[i]] = i;
  }

  free();

  CUDACHECK(cudaMalloc(&d_data_, sizeof(float*) * data_.size()));
  CUDACHECK(cudaMalloc(&d_dimensions_, sizeof(int) * dimensions_.size()));
  CUDACHECK(cudaMalloc(&d_id_space_to_local_index_, sizeof(int) * id_space_to_local_index_.size()));
  CUDACHECK(cudaMalloc(&d_scale_, sizeof(int) * scale_.size()));

  // clang-format off
  CUDACHECK(cudaMemcpyAsync(d_data_, data_.data(),
                            sizeof(float*) * data_.size(),
                            cudaMemcpyHostToDevice, stream_));
  CUDACHECK(cudaMemcpyAsync(d_dimensions_, dimensions_.data(),
                            sizeof(int) * dimensions_.size(),
                            cudaMemcpyHostToDevice, stream_));
  CUDACHECK(cudaMemcpyAsync(d_id_space_to_local_index_, id_space_to_local_index_.data(),
                            sizeof(int) * id_space_to_local_index_.size(),
                            cudaMemcpyHostToDevice, stream_));
  CUDACHECK(cudaMemcpyAsync(d_scale_, scale_.data(),
                            sizeof(int) * scale_.size(),
                            cudaMemcpyHostToDevice, stream_));
  // clang-format on
}

template <typename KeyType, typename OffsetType, typename DType>
void TFAdapter<KeyType, OffsetType, DType>::set(
    std::shared_ptr<sok::CoreResourceManager> tf_backend,
    std::vector<tensorflow::core::RefCountPtr<tensorflow::Var>>& vars,
    std::vector<tensorflow::tf_shared_lock>& locks, std::vector<int>& dimensions,
    std::vector<int>& scale, cudaStream_t stream) {
  tf_backend_ = tf_backend;
  std::vector<float*> data;
  std::vector<int> id_space;
  for (int i = 0; i < vars.size(); ++i) {
    float* input = vars[i]->tensor()->flat<float>().data();
    bool is_unique = true;
    for (int j = 0; j < i; ++j) {
      if (input == data[j]) {
        is_unique = false;
        break;
      }
    }
    if (is_unique) {
      tensorflow::tf_shared_lock lock(*vars[i]->mu());
      locks.push_back(std::move(lock));
    }
    data.push_back(input);
    id_space.push_back(i);
  }

  if (data_.size() == data.size()) {
    bool skip = true;
    for (int i = 0; i < data.size(); ++i) {
      if (data_[i] != data[i]) {
        skip = false;
        break;
      }
    }
    if (skip) {
      return;
    }
  }

  data_ = data;
  dimensions_ = dimensions;
  scale_ = scale;
  stream_ = stream;

  id_space_to_local_index_.resize(vars.size(), -1);
  for (int i = 0; i < id_space.size(); ++i) {
    id_space_to_local_index_[id_space[i]] = i;
  }

  free();

  CUDACHECK(cudaMalloc(&d_data_, sizeof(float*) * data_.size()));
  CUDACHECK(cudaMalloc(&d_dimensions_, sizeof(int) * dimensions_.size()));
  CUDACHECK(cudaMalloc(&d_id_space_to_local_index_, sizeof(int) * id_space_to_local_index_.size()));
  CUDACHECK(cudaMalloc(&d_scale_, sizeof(int) * scale_.size()));

  // clang-format off
  CUDACHECK(cudaMemcpyAsync(d_data_, data_.data(),
                            sizeof(float*) * data_.size(),
                            cudaMemcpyHostToDevice, stream_));
  CUDACHECK(cudaMemcpyAsync(d_dimensions_, dimensions_.data(),
                            sizeof(int) * dimensions_.size(),
                            cudaMemcpyHostToDevice, stream_));
  CUDACHECK(cudaMemcpyAsync(d_id_space_to_local_index_, id_space_to_local_index_.data(),
                            sizeof(int) * id_space_to_local_index_.size(),
                            cudaMemcpyHostToDevice, stream_));
  CUDACHECK(cudaMemcpyAsync(d_scale_, scale_.data(),
                            sizeof(int) * scale_.size(),
                            cudaMemcpyHostToDevice, stream_));
  // clang-format on
}

template <typename KeyType, typename OffsetType, typename DType>
void TFAdapter<KeyType, OffsetType, DType>::free() {
  if (d_data_) {
    CUDACHECK(cudaFree(d_data_));
    d_data_ = nullptr;
  }
  if (d_dimensions_) {
    CUDACHECK(cudaFree(d_dimensions_));
    d_dimensions_ = nullptr;
  }
  if (d_id_space_to_local_index_) {
    CUDACHECK(cudaFree(d_id_space_to_local_index_));
    d_id_space_to_local_index_ = nullptr;
  }
  if (d_scale_) {
    CUDACHECK(cudaFree(d_scale_));
    d_scale_ = nullptr;
  }
}

template <typename KeyType, typename OffsetType, typename DType>
TFAdapter<KeyType, OffsetType, DType>::~TFAdapter() {
  free();
}

template <typename KeyType, typename OffsetType, typename DType>
void TFAdapter<KeyType, OffsetType, DType>::lookup(const core23::Tensor& keys, size_t num_keys,
                                                   const core23::Tensor& id_space_offset,
                                                   size_t num_id_space_offset,
                                                   const core23::Tensor& id_space,
                                                   core23::Tensor& embedding_vec) {
  TFAdapterKernel<KeyType, OffsetType, DType><<<2 * sm_count_, 1024ul, 0, stream_>>>(
      d_data_, d_dimensions_, d_scale_, d_id_space_to_local_index_, keys.data<KeyType>(), num_keys,
      id_space_offset.data<OffsetType>(), num_id_space_offset - 1, id_space.data<int>(),
      static_cast<DType**>(embedding_vec.data()));
  // CUDACHECK(cudaStreamSynchronize(stream_));
  // CUDACHECK(cudaGetLastError());
}

template class TFAdapter<int32_t, int32_t, float>;
template class TFAdapter<int32_t, int64_t, float>;
// template class TFAdapter<int32_t, __half>;
template class TFAdapter<int64_t, int32_t, float>;
template class TFAdapter<int64_t, int64_t, float>;
// template class TFAdapter<int64_t, __half>;

template <typename KeyType, typename OffsetType, typename DType>
DummyVarAdapter<KeyType, OffsetType, DType>::DummyVarAdapter() : stream_(0) {
  int device;
  CUDACHECK(cudaGetDevice(&device));
  CUDACHECK(cudaDeviceGetAttribute(&sm_count_, cudaDevAttrMultiProcessorCount, device));
}

template <typename KeyType, typename OffsetType, typename DType>
void DummyVarAdapter<KeyType, OffsetType, DType>::set(
    std::shared_ptr<sok::CoreResourceManager> tf_backend,
    std::vector<tensorflow::core::RefCountPtr<tensorflow::DummyVar<KeyType, DType>>>& vars,
    std::vector<tensorflow::tf_shared_lock>& locks, std::vector<int>& dimensions,
    std::vector<int>& scale, cudaStream_t stream) {
  tf_backend_ = tf_backend;
  vars_.resize(vars.size());
  same_table_.resize(vars.size());
  // id_space_to_local_index_.resize(vars.size());
  for (int i = 0; i < vars.size(); ++i) {
    std::shared_ptr<VariableBase<KeyType, DType>> var = vars[i]->get_var();
    bool is_unique = true;
    for (int j = 0; j < i; ++j) {
      if (var == vars_[j]) {
        is_unique = false;
        break;
      }
    }
    if (is_unique) {
      tensorflow::tf_shared_lock lock(*vars[i]->mu());
      locks.push_back(std::move(lock));
    }

    if (i == 0) {
      same_table_[i] = i;
    } else {
      if (var == vars_[i - 1]) {
        same_table_[i] = same_table_[i - 1];
      } else {
        same_table_[i] = i;
      }
    }

    vars_[i] = var;
    // id_space_to_local_index_[i] = i;
  }
}

template <typename KeyType, typename OffsetType, typename DType>
void DummyVarAdapter<KeyType, OffsetType, DType>::lookup(
    const core23::Tensor& keys, size_t num_keys, const core23::Tensor& id_space_offset,
    size_t num_id_space_offset, const core23::Tensor& id_space, core23::Tensor& embedding_vec) {
  // clang-format off
  id_space_offset_.clear();
  id_space_.clear();
  id_space_offset_.resize(num_id_space_offset);
  CUDACHECK(cudaMemcpyAsync(id_space_offset_.data(),
                            id_space_offset.data<OffsetType>(),
                            sizeof(OffsetType) * (num_id_space_offset),
                            cudaMemcpyDeviceToHost, stream_));
  id_space_.resize(num_id_space_offset - 1);
  CUDACHECK(cudaMemcpyAsync(id_space_.data(),
                            id_space.data<int>(),
                            sizeof(int) * (num_id_space_offset - 1),
                            cudaMemcpyDeviceToHost, stream_));
  // clang-format on

  CUDACHECK(cudaStreamSynchronize(stream_));

  DType** output = static_cast<DType**>(embedding_vec.data());
  const KeyType* input = keys.data<KeyType>();

  // HugeCTR::CudaDeviceContext context(tf_backend_->get_device_id());
  core23::Device device(core23::DeviceType::GPU, tf_backend_->get_device_id());
  core23::Device device_cpu(core23::DeviceType::CPU, tf_backend_->get_device_id());
  core23::BufferParams buffer_params;
  buffer_params.unitary = false;
  core23::TensorParams params = core23::TensorParams().device(device).buffer_params(buffer_params);
  core23::TensorParams params_cpu =
      core23::TensorParams().device(device_cpu).buffer_params(buffer_params);

  int start_index = 0;
  size_t num = 0;
  bool is_lookup = false;
  for (int i = 0; i < num_id_space_offset - 1; ++i) {
    if (i == num_id_space_offset - 2) {
      num += id_space_offset_[i + 1] - id_space_offset_[i];
      is_lookup = true;
    } else {
      if (same_table_[i + 1] != same_table_[i]) {
        num += id_space_offset_[i + 1] - id_space_offset_[i];
        is_lookup = true;
      } else {
        num += id_space_offset_[i + 1] - id_space_offset_[i];
      }
    }
    if (num != 0 && is_lookup) {
      core23::Tensor unique_keys =
          core23::Tensor(params.shape({static_cast<int64_t>(num)})
                             .data_type(core23::ToScalarType<KeyType>::value));
      core23::Tensor num_unique_keys = core23::Tensor(
          params_cpu.shape({static_cast<int64_t>(1)}).data_type(core23::ScalarType::UInt64));
      core23::Tensor unique_reverse_idxs = core23::Tensor(
          params.shape({static_cast<int64_t>(num)}).data_type(core23::ScalarType::UInt64));
      core23::Tensor unique_output =
          core23::Tensor(params.shape({static_cast<int64_t>(num * sizeof(float*))})
                             .data_type(core23::ScalarType::Char));

      embedding::unique_op<KeyType, uint64_t, std::numeric_limits<KeyType>::max(),
                           std::numeric_limits<uint64_t>::max()>
          unique = embedding::unique_op<KeyType, uint64_t, std::numeric_limits<KeyType>::max(),
                                        std::numeric_limits<uint64_t>::max()>(tf_backend_, num);

      unique.unique(input, num, unique_reverse_idxs.data<uint64_t>(), unique_keys.data<KeyType>(),
                    num_unique_keys.data<uint64_t>(), stream_);

      CUDACHECK(cudaStreamSynchronize(stream_));
      auto var = vars_[id_space_[start_index]];
      // var->lookup(input, output, num, stream_);
      DType** unique_output_ptr = static_cast<DType**>(unique_output.data());
      var->lookup(unique_keys.data<KeyType>(), unique_output_ptr,
                  static_cast<size_t>(*(num_unique_keys.data<uint64_t>())), stream_);
      UniqueReverseKernel<<<((num - 1) / 1024) + 1, 1024, 0, stream_>>>(
          unique_output_ptr, unique_reverse_idxs.data<uint64_t>(), num, output);
      CUDACHECK(cudaStreamSynchronize(stream_));
      input += num;
      output += num;
      num = 0;
      is_lookup = false;
      start_index = i + 1;
    }
  }
}

template class DummyVarAdapter<int32_t, int32_t, float>;
template class DummyVarAdapter<int32_t, int64_t, float>;
// template class DummyVarAdapter<int32_t, __half>;
template class DummyVarAdapter<int64_t, int32_t, float>;
template class DummyVarAdapter<int64_t, int64_t, float>;
// template class DummyVarAdapter<int64_t, __half>;

}  // namespace sok
