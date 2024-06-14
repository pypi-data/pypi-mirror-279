/*
 * Copyright (c) 2023, NVIDIA CORPORATION.
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

#include <cub/cub.cuh>
#include <embedding/common.hpp>
#include <embedding/operators/dp_index_calculation.hpp>
#include <embedding/operators/index_calculation.hpp>
#include <embedding/operators/mp_index_calculation.hpp>
#include <embedding/view.hpp>
#include <utils.cuh>
#include <utils.hpp>

#if CUB_VERSION >= 200200
#include <cuda/std/tuple>
#endif

namespace embedding {

namespace {

struct BucketInfo {
  uint32_t start;
  uint32_t end;
  int shard_id;
  int num_shards;
};

template <typename key_t, typename offset_t>
struct KeySelectorGPU {
  const key_t *__restrict__ keys_ptr;
  const offset_t *__restrict__ bucket_range_ptr;
  const int *__restrict__ lookup_ids_ptr;
  int num_lookup_before_filter;
  int num_lookup_after_filter;
  int gpu_id;
  int num_gpus;
  int batch_size_per_gpu;
  const int *shard_ids_ptr_;
  const int *num_shards_ptr_;

  KeySelectorGPU(const core23::Tensor &keys, const core23::Tensor &bucket_range,
                 const MPKeySelector &key_selector, int batch_size)
      : keys_ptr(keys.data<key_t>()),
        bucket_range_ptr(bucket_range.data<offset_t>()),
        lookup_ids_ptr(key_selector.lookup_ids.data<int>()),
        num_lookup_before_filter(key_selector.num_lookup_before_filter),
        num_lookup_after_filter(key_selector.num_lookup_after_filter),
        gpu_id(0),
        num_gpus(1),
        batch_size_per_gpu(batch_size),
        shard_ids_ptr_(key_selector.shard_ids.data<int>()),
        num_shards_ptr_(key_selector.num_shards.data<int>()) {}

  KeySelectorGPU(const core23::Tensor &keys, const core23::Tensor &bucket_range,
                 const DPKeySelector &key_selector, int batch_size)
      : keys_ptr(keys.data<key_t>()),
        bucket_range_ptr(bucket_range.data<offset_t>()),
        lookup_ids_ptr(key_selector.lookup_ids.data<int>()),
        num_lookup_before_filter(key_selector.num_lookup_before_filter),
        num_lookup_after_filter(key_selector.num_lookup_after_filter),
        gpu_id(key_selector.gpu_id),
        num_gpus(key_selector.num_gpus),
        batch_size_per_gpu(batch_size / key_selector.num_gpus),
        shard_ids_ptr_(nullptr),
        num_shards_ptr_(nullptr) {}

  DEVICE_INLINE int cal_bucket_idx(const int &i) const {
    int lookup_id = (lookup_ids_ptr == nullptr) ? i / batch_size_per_gpu
                                                : lookup_ids_ptr[i / batch_size_per_gpu];
    int idx = batch_size_per_gpu * num_lookup_before_filter * num_gpus;
    if (i < batch_size_per_gpu * num_lookup_before_filter * num_gpus) {
      idx = lookup_id * batch_size_per_gpu * num_gpus + gpu_id * batch_size_per_gpu +
            (i % batch_size_per_gpu);
    }
    return idx;
  }

  __device__ BucketInfo idx_to_selected_bucket(const int &i) const {
    offset_t start = bucket_range_ptr[cal_bucket_idx(i)];
    offset_t end = bucket_range_ptr[cal_bucket_idx(i) + 1];
    int shard_id = (shard_ids_ptr_ == nullptr) ? 0 : shard_ids_ptr_[i / batch_size_per_gpu];
    int num_shards = (num_shards_ptr_ == nullptr) ? 1 : num_shards_ptr_[i / batch_size_per_gpu];
    return {static_cast<uint32_t>(start), static_cast<uint32_t>(end), shard_id, num_shards};
  }
};

// Cautions: Dont use pass KeySelector by reference
template <typename key_t, typename offset_t>
__global__ void mask_and_count_keys_in_bucket_kernel(KeySelectorGPU<key_t, offset_t> key_selector,
                                                     const key_t *__restrict__ keys,
                                                     offset_t *bucket_range_after_filter,
                                                     char *flag, int num) {
  int batch_size = key_selector.batch_size_per_gpu;
  CUDA_1D_KERNEL_LOOP(i, num) {
    if (i >= batch_size * key_selector.num_lookup_after_filter) {
      bucket_range_after_filter[1 + i] = 0;
      continue;
    }

    BucketInfo bucket_info = key_selector.idx_to_selected_bucket(i);
    uint32_t start_before_filter = bucket_info.start;
    uint32_t end_before_filter = bucket_info.end;
    int shard_id = bucket_info.shard_id;
    int num_shards = bucket_info.num_shards;

    uint32_t cnt_selected = 0;
    for (uint32_t l = 0; l < (end_before_filter - start_before_filter); ++l) {
      key_t k = keys[l + start_before_filter];
      if (k % num_shards == shard_id) {
        flag[l + start_before_filter] = 1;
        cnt_selected += 1;
      }
    }
    bucket_range_after_filter[1 + i] = cnt_selected;
    if (i == 0) {
      bucket_range_after_filter[0] = 0;
    }
  }
}

}  // namespace

void IndexCalculationTempStorage::init(const std::shared_ptr<CoreResourceManager> &core,
                                       int max_num_keys_before_filter,
                                       int max_num_keys_after_filter, int batch_size_before_filter,
                                       int batch_size_after_filter, int num_lookup) {
  HugeCTR::CudaDeviceContext ctx(core->get_device_id());
  core23::Device device(core23::DeviceType::GPU, core->get_device_id());
  core23::TensorParams params = core23::TensorParams().device(device);

  this->flag = core23::Tensor(params.shape({batch_size_before_filter * max_num_keys_before_filter})
                                  .data_type(core23::ScalarType::Char));
  {
    size_t temp_bytes = 0;
    cub::DeviceSelect::Flagged(nullptr, temp_bytes, (uint64_t *)nullptr, (char *)nullptr,
                               (uint64_t *)nullptr, (size_t *)nullptr,
                               batch_size_before_filter * max_num_keys_before_filter);
    this->temp_select_storage = core23::Tensor(
        params.shape({static_cast<int64_t>(temp_bytes)}).data_type(core23::ScalarType::Char));
  }
  {
    size_t temp_bytes = 0;
    cub::DeviceScan::InclusiveSum(nullptr, temp_bytes, (uint64_t *)nullptr, (uint32_t *)nullptr,
                                  batch_size_after_filter * num_lookup + 1);
    this->temp_scan_storage = core23::Tensor(
        params.shape({static_cast<int64_t>(temp_bytes)}).data_type(core23::ScalarType::Char));
  }
}

template <>
void IndexCalculation<MPKeySelector>::init(std::shared_ptr<CoreResourceManager> core,
                                           const MPKeySelector &key_selector, int batch_size) {
  this->core_ = core;
  this->key_selector_ = key_selector;
  this->temp_storage_.init(core, key_selector.max_num_keys_before_filter,
                           key_selector.max_num_keys_after_filter, batch_size, batch_size,
                           key_selector.num_lookup_after_filter);
}

template <>
void IndexCalculation<DPKeySelector>::init(std::shared_ptr<CoreResourceManager> core,
                                           const embedding::DPKeySelector &key_selector,
                                           int batch_size) {
  this->core_ = core;
  this->key_selector_ = key_selector;
  this->temp_storage_.init(
      core, key_selector.max_num_keys_before_filter, key_selector.max_num_keys_after_filter,
      batch_size, batch_size / key_selector.num_gpus, key_selector.num_lookup_after_filter);
}

template <typename KeySelector>
void IndexCalculation<KeySelector>::filter_sparse_input(const core23::Tensor &keys,
                                                        const core23::Tensor &bucket_range,
                                                        EmbeddingInput &result, int batch_size) {
  HugeCTR::CudaDeviceContext ctx(core_->get_device_id());
  auto stream = core_->get_local_gpu()->get_stream();

  HCTR_LIB_THROW(cudaMemsetAsync(result.keys.data(), 0, result.keys.num_bytes(), stream));
  HCTR_LIB_THROW(
      cudaMemsetAsync(result.bucket_range.data(), 0, result.bucket_range.num_bytes(), stream));
  HCTR_LIB_THROW(
      cudaMemsetAsync(temp_storage_.flag.data(), 0, temp_storage_.flag.num_bytes(), stream));

  DISPATCH_INTEGRAL_FUNCTION_CORE23(keys.data_type().type(), key_t, [&] {
    DISPATCH_INTEGRAL_FUNCTION_CORE23(bucket_range.data_type().type(), offset_t, [&] {
      const key_t *keys_ptr = keys.data<key_t>();

      offset_t *bucket_range_after_filter = result.bucket_range.data<offset_t>();
      key_t *keys_after_filter = result.keys.data<key_t>();

      KeySelectorGPU<key_t, offset_t> key_selector_gpu{keys, bucket_range, key_selector_,
                                                       batch_size};
      const int block_size = 256;
      const int grid_size = core_->get_kernel_param().num_sms *
                            core_->get_kernel_param().max_thread_per_block / block_size;
      mask_and_count_keys_in_bucket_kernel<<<grid_size, block_size, 0, stream>>>(
          key_selector_gpu, key_selector_gpu.keys_ptr, bucket_range_after_filter,
          temp_storage_.flag.data<char>(), result.bucket_range.num_elements() - 1);

      size_t temp_scan_storage_nbytes = temp_storage_.temp_scan_storage.num_bytes();
      cub::DeviceScan::InclusiveSum(temp_storage_.temp_scan_storage.data(),
                                    temp_scan_storage_nbytes, bucket_range_after_filter,
                                    bucket_range_after_filter, result.bucket_range.num_elements(),
                                    stream);

      size_t temp_select_storage_nbytes = temp_storage_.temp_select_storage.num_bytes();
      cub::DeviceSelect::Flagged(temp_storage_.temp_select_storage.data(),
                                 temp_select_storage_nbytes, keys_ptr,
                                 temp_storage_.flag.data<char>(), keys_after_filter,
                                 result.num_keys.data<size_t>(), keys.num_elements(), stream);
      HCTR_LIB_THROW(cudaStreamSynchronize(stream));
      result.h_num_keys = static_cast<size_t>(result.num_keys.data<uint64_t>()[0]);
    });
  });
}

template class IndexCalculation<MPKeySelector>;
template class IndexCalculation<DPKeySelector>;

void ReductionIndices::init(std::shared_ptr<CoreResourceManager> core, int local_hotness_sum,
                            int batch_size, core23::DataType key_type) {
  HugeCTR::CudaDeviceContext context(core->get_device_id());
  int max_num_key_for_reduction = local_hotness_sum * batch_size;

  core23::Device device(core23::DeviceType::GPU, core->get_device_id());
  core23::TensorParams params = core23::TensorParams().device(device);

  this->sorted_keys =
      core23::Tensor(params.shape({batch_size * local_hotness_sum}).data_type(key_type));

  this->src_ids = core23::Tensor(
      params.shape({max_num_key_for_reduction}).data_type(core23::ScalarType::UInt32));

  this->dst_ids = core23::Tensor(
      params.shape({max_num_key_for_reduction}).data_type(core23::ScalarType::UInt32));
  this->table_ids = core23::Tensor(
      params.shape({max_num_key_for_reduction}).data_type(core23::ScalarType::Int32));
  this->ev_sizes = core23::Tensor(
      params.shape({max_num_key_for_reduction}).data_type(core23::ScalarType::Int32));
  this->num_key = core23::Tensor(params.shape({1}).data_type(core23::ScalarType::UInt64));
}

PartitionedResult::PartitionedResult(std::shared_ptr<CoreResourceManager> core, int num_lookup,
                                     int local_hotness_sum, int batch_size,
                                     core23::DataType key_type, core23::DataType offset_type) {
  HugeCTR::CudaDeviceContext context(core->get_device_id());

  core23::Device device(core23::DeviceType::GPU, core->get_device_id());
  core23::TensorParams params = core23::TensorParams().device(device);

  this->partitioned_keys =
      core23::Tensor(params.shape({batch_size * local_hotness_sum}).data_type(key_type));
  this->partitioned_src_ids = core23::Tensor(
      params.shape({batch_size * local_hotness_sum}).data_type(core23::ScalarType::UInt32));
  this->partitioned_bucket_range =
      core23::Tensor(params.shape({num_lookup * batch_size + 1}).data_type(offset_type));
}

namespace {

template <typename offset_t>
__global__ void subtract_left_kernel(const int *sorted_lookup_ids, const offset_t *bucket_range,
                                     int num_lookup, int batch_size, offset_t *output) {
  CUDA_1D_KERNEL_LOOP(i, num_lookup * batch_size) {
    int lookup_id = sorted_lookup_ids[i / batch_size];
    int idx = lookup_id * batch_size + i % batch_size;
    output[1 + i] = bucket_range[idx + 1] - bucket_range[idx];
  }
  if (threadIdx.x + blockIdx.x * blockDim.x == 0) {
    output[0] = 0ul;
  }
}

template <typename key_t, typename offset_t>
__global__ void group_keys_by_lookup_id_kernel(const int *sorted_lookup_ids, const key_t *keys,
                                               const offset_t *bucket_range,
                                               const offset_t *partitioned_bucket_range,
                                               int num_lookup, int batch_size,
                                               key_t *partitioned_keys) {
  CUDA_1D_KERNEL_LOOP(idx, num_lookup * batch_size) {
    int lookup_id = sorted_lookup_ids[idx / batch_size];
    uint32_t start = static_cast<uint32_t>(bucket_range[lookup_id * batch_size + idx % batch_size]);
    uint32_t end =
        static_cast<uint32_t>(bucket_range[lookup_id * batch_size + idx % batch_size + 1]);

    offset_t partitioned_start = partitioned_bucket_range[idx];

    for (uint32_t i = start; i < end; ++i) {
      partitioned_keys[partitioned_start + i - start] = keys[i];
    }
  }
}

void group_keys_by_lookup_id(const core23::Tensor &keys, const core23::Tensor &bucket_range,
                             const core23::Tensor &sorted_lookup_ids, int num_lookup,
                             int batch_size, core23::Tensor &partitioned_keys,
                             core23::Tensor &partitioned_bucket_range,
                             LocalReduceIndexCalculationTempStorage &temp_storage,
                             std::shared_ptr<CoreResourceManager> core) {
  auto stream = core->get_local_gpu()->get_stream();
  DISPATCH_INTEGRAL_FUNCTION_CORE23(keys.data_type().type(), key_t, [&] {
    DISPATCH_INTEGRAL_FUNCTION_CORE23(bucket_range.data_type().type(), offset_t, [&] {
      const int block_size = 256;
      const int grid_size = core->get_kernel_param().num_sms *
                            core->get_kernel_param().max_thread_per_block / block_size;
      subtract_left_kernel<<<grid_size, block_size, 0, stream>>>(
          sorted_lookup_ids.data<int>(), bucket_range.data<offset_t>(), num_lookup, batch_size,
          partitioned_bucket_range.data<offset_t>());

      size_t temp_storage_nbytes = temp_storage.temp_scan_storage.num_bytes();
      cub::DeviceScan::InclusiveSum(temp_storage.temp_scan_storage.data(), temp_storage_nbytes,
                                    partitioned_bucket_range.data<offset_t>(),
                                    partitioned_bucket_range.data<offset_t>(),
                                    num_lookup * batch_size + 1, stream);

      group_keys_by_lookup_id_kernel<<<grid_size, block_size, 0, stream>>>(
          sorted_lookup_ids.data<int>(), keys.data<key_t>(), bucket_range.data<offset_t>(),
          partitioned_bucket_range.data<offset_t>(), num_lookup, batch_size,
          partitioned_keys.data<key_t>());
    });
  });
}

template <typename offset_t>
__global__ void replicate_bucket_range_kernel(const offset_t *bucket_range,
                                              const int *sorted_lookup_ids,
                                              const int *sorted_table_ids,
                                              const int *table_id_to_ev_size, int num_lookup,
                                              int batch_size, uint32_t *src_ids, int *table_ids,
                                              int *ev_sizes, uint64_t *num_key) {
  extern __shared__ uint32_t smem_buffer[];
  uint32_t *smem_bucket_range = smem_buffer;

  int32_t max_bucket_num = num_lookup * batch_size;
  for (int32_t i = blockIdx.x * blockDim.x, step = blockDim.x * gridDim.x; i < max_bucket_num;
       i += step) {
    int max_local_id = blockDim.x < max_bucket_num - i ? blockDim.x : max_bucket_num - i;
    {
      int32_t global_id = i + threadIdx.x;
      if (threadIdx.x < max_local_id) {
        uint32_t start = static_cast<uint32_t>(bucket_range[global_id]);
        uint32_t end = static_cast<uint32_t>(bucket_range[global_id + 1]);
        smem_bucket_range[threadIdx.x] = start;
        if (threadIdx.x == max_local_id - 1) smem_bucket_range[max_local_id] = end;
        if (global_id == max_bucket_num - 1) num_key[0] = end;
      }
    }
    __syncthreads();
    for (int local_index = smem_bucket_range[0] + threadIdx.x;
         local_index < smem_bucket_range[max_local_id]; local_index += blockDim.x) {
      int idx =
          bs_upper_bound_sub_one(smem_bucket_range, max_local_id + 1, (uint32_t)local_index) + i;
      int lookup_id = sorted_lookup_ids[idx / batch_size];
      uint32_t bucket_id = lookup_id * batch_size + idx % batch_size;
      int table_id = sorted_table_ids[idx / batch_size];
      table_ids[local_index] = table_id;
      ev_sizes[local_index] = table_id_to_ev_size[table_id];
      src_ids[local_index] = bucket_id;
    }
    __syncthreads();
  }
}

void replicate_bucket_range(const core23::Tensor &bucket_range,
                            const core23::Tensor &sorted_lookup_ids,
                            const core23::Tensor &sorted_table_ids,
                            const core23::Tensor &table_id_to_ev_size, int num_lookup,
                            int batch_size, core23::Tensor &src_ids, core23::Tensor &table_ids,
                            core23::Tensor &ev_sizes, core23::Tensor &num_key,
                            std::shared_ptr<CoreResourceManager> core) {
  auto stream = core->get_local_gpu()->get_stream();
  DISPATCH_INTEGRAL_FUNCTION_CORE23(bucket_range.data_type().type(), offset_t, [&] {
    const int block_size = 256;
    const int grid_size = core->get_kernel_param().num_sms *
                          core->get_kernel_param().max_thread_per_block / block_size;
    replicate_bucket_range_kernel<<<grid_size, block_size, sizeof(uint32_t) * (block_size + 1),
                                    stream>>>(
        bucket_range.data<offset_t>(), sorted_lookup_ids.data<int>(), sorted_table_ids.data<int>(),
        table_id_to_ev_size.data<int>(), num_lookup, batch_size, src_ids.data<uint32_t>(),
        table_ids.data<int>(), ev_sizes.data<int>(), num_key.data<uint64_t>());
  });
}

struct LessThan {
  int compare;
  __host__ __device__ __forceinline__ LessThan(int compare) : compare(compare) {}
  __host__ __device__ __forceinline__ bool operator()(const int &a) const { return (a < compare); }
};

template <typename offset_t>
__global__ void cal_table_range_kernel(const offset_t *bucket_range, const int *sorted_table_ids,
                                       int num_lookup, int *table_range, int batch_size) {
  CUDA_1D_KERNEL_LOOP(idx, num_lookup) {
    if (idx == 0 || sorted_table_ids[idx] != sorted_table_ids[idx - 1]) {
      table_range[idx] = bucket_range[idx * batch_size];
    } else {
      table_range[idx] = std::numeric_limits<int>::max();
    }
  }
  if (threadIdx.x == 0) {
    table_range[num_lookup] = bucket_range[num_lookup * batch_size];
  }
}

void partition_by_table_id(const core23::Tensor &keys, const core23::Tensor &bucket_range,
                           const core23::Tensor &sorted_lookup_ids,
                           const core23::Tensor &sorted_table_ids,
                           const core23::Tensor &table_id_to_ev_size, int num_lookup, int num_table,
                           PartitionedResult &result, ReductionIndices &reduction_indices,
                           int batch_size, LocalReduceIndexCalculationTempStorage &temp_storage,
                           std::shared_ptr<CoreResourceManager> core) {
  if (num_table != num_lookup) {
    group_keys_by_lookup_id(keys, bucket_range, sorted_lookup_ids, num_lookup, batch_size,
                            result.partitioned_keys, result.partitioned_bucket_range, temp_storage,
                            core);

  } else {
    result.partitioned_keys = keys;
    result.partitioned_bucket_range = bucket_range;
  }

  replicate_bucket_range(result.partitioned_bucket_range, sorted_lookup_ids, sorted_table_ids,
                         table_id_to_ev_size, num_lookup, batch_size, result.partitioned_src_ids,
                         reduction_indices.table_ids, reduction_indices.ev_sizes,
                         reduction_indices.num_key, core);
}

}  // namespace

template <typename offset_t>
void LocalReduceIndexCalculationTempStorage::init(const std::shared_ptr<CoreResourceManager> &core,
                                                  int num_lookup, int batch_size) {
  HugeCTR::CudaDeviceContext ctx(core->get_device_id());

  core23::Device device(core23::DeviceType::GPU, core->get_device_id());
  core23::TensorParams params = core23::TensorParams().device(device);

  {
    size_t temp_bytes = 0;
    cub::DeviceScan::InclusiveSum(nullptr, temp_bytes, (offset_t *)nullptr, (offset_t *)nullptr,
                                  (size_t)num_lookup * batch_size + 1);
    this->temp_scan_storage = core23::Tensor(
        params.shape({static_cast<int64_t>(temp_bytes)}).data_type(core23::ScalarType::Char));
  }
}

LocalReduceIndexCalculation::LocalReduceIndexCalculation(std::shared_ptr<CoreResourceManager> core,
                                                         int num_lookup, int local_hotness_sum,
                                                         int batch_size, core23::DataType key_type,
                                                         core23::DataType offset_type)
    : core_(core),
      partitioned_result_(core, num_lookup, local_hotness_sum, batch_size, key_type, offset_type) {
  DISPATCH_INTEGRAL_FUNCTION_CORE23(
      partitioned_result_.partitioned_bucket_range.data_type().type(), offset_t,
      [&] { temp_storage_.init<offset_t>(core, num_lookup, batch_size); });
}

#if CUB_VERSION >= 200200

template <typename T>
struct ComposeTidKey {
  int tid;
  T key;
} __attribute__((packed));

template <typename T>
struct Decomposr {
  __host__ __device__ ::cuda::std::tuple<int &, T &> operator()(
      ComposeTidKey<T> &compose_key) const {
    return {compose_key.tid, compose_key.key};
  }
};

template <typename key_t>
__global__ void compose_tid_key_kernel(const key_t *keys, const int *table_range,
                                       const size_t num_keys, const int num_table_range,
                                       struct ComposeTidKey<key_t> *compose_arr) {
  CUDA_1D_KERNEL_LOOP(idx, num_keys) {
    key_t tmp_key = keys[idx];
    int table_id = bs_upper_bound_sub_one(table_range, num_table_range, idx);
    ComposeTidKey<key_t> compose;
    compose.tid = table_id;
    compose.key = tmp_key;
    compose_arr[idx] = compose;
  }
}

template <typename key_t>
__global__ void decompose_tid_key_kernel(const struct ComposeTidKey<key_t> *compose_arr,
                                         const size_t num_keys, key_t *keys) {
  CUDA_1D_KERNEL_LOOP(idx, num_keys) { keys[idx] = compose_arr[idx].key; }
}

#endif

SegmentedSortDevice::SegmentedSortDevice(const std::shared_ptr<CoreResourceManager> &core,
                                         core23::Tensor sorted_table_ids, int max_num_keys,
                                         int batch_size, int num_lookup, int num_table,
                                         core23::DataType key_type)
    : sorted_table_ids_(sorted_table_ids),
      num_lookup_(num_lookup),
      num_table_(num_table),
      batch_size_(batch_size) {
  HugeCTR::CudaDeviceContext context(core->get_device_id());

  core23::Device device(core23::DeviceType::GPU, core->get_device_id());
  core23::TensorParams params = core23::TensorParams().device(device);

  max_key_num_ = ((size_t)max_num_keys) * ((size_t)batch_size);
#if CUB_VERSION >= 200200
  DISPATCH_INTEGRAL_FUNCTION_CORE23(key_type.type(), key_t, [&] {
    this->compose_tid_keys_input = core23::Tensor(
        params.shape({static_cast<int64_t>(max_key_num_ * (sizeof(ComposeTidKey<key_t>)))})
            .data_type(core23::ScalarType::Char));
    this->compose_tid_keys_output = core23::Tensor(
        params.shape({static_cast<int64_t>(max_key_num_ * (sizeof(ComposeTidKey<key_t>)))})
            .data_type(core23::ScalarType::Char));
    cub::DeviceRadixSort::SortPairs(nullptr, cub_sort_temp_bytes_, (ComposeTidKey<key_t> *)nullptr,
                                    (ComposeTidKey<key_t> *)nullptr, (uint32_t *)nullptr,
                                    (uint32_t *)nullptr, max_key_num_, Decomposr<key_t>{}, 0,
                                    sizeof(struct ComposeTidKey<key_t>) * 8);
    cub_sort_temp_buffer_ =
        core23::Tensor(params.shape({static_cast<int64_t>(cub_sort_temp_bytes_)})
                           .data_type(core23::ScalarType::Char));
  });
#else
  DISPATCH_INTEGRAL_FUNCTION_CORE23(key_type.type(), key_t, [&] {
    cub::DeviceSegmentedRadixSort::SortPairs(
        nullptr, cub_sort_temp_bytes_, (key_t *)nullptr, (key_t *)nullptr, (uint32_t *)nullptr,
        (uint32_t *)nullptr, max_key_num_, num_table, (int *)nullptr, (int *)nullptr);
    cub_sort_temp_buffer_ =
        core23::Tensor(params.shape({static_cast<int64_t>(cub_sort_temp_bytes_)})
                           .data_type(core23::ScalarType::Char));
  });
#endif

  this->partitioned_table_range =
      core23::Tensor(params.shape({num_table + 1}).data_type(core23::ScalarType::Int32));

  {
    size_t temp_bytes = 0;
    LessThan select_op(std::numeric_limits<int>::max());
    cub::DeviceSelect::If(nullptr, temp_bytes, (int *)nullptr, (int *)nullptr, (int *)nullptr,
                          num_lookup + 1, select_op);
    this->temp_select_storage = core23::Tensor(
        params.shape({static_cast<int64_t>(temp_bytes)}).data_type(core23::ScalarType::Char));
  }
  this->d_num_selected_table_range_ =
      core23::Tensor(params.shape({1}).data_type(core23::ScalarType::Int32));
  this->temp_lookup_range =
      core23::Tensor(params.shape({num_lookup + 1}).data_type(core23::ScalarType::Int32));
}

void SegmentedSortDevice::operator()(embedding::SortInput &input, embedding::SortOutput &output,
                                     std::shared_ptr<CoreResourceManager> core) {
  auto stream = core->get_local_gpu()->get_stream();
  auto &bucket_range = input.bucket_range;
  const int block_size = 256;
  const int grid_size =
      core->get_kernel_param().num_sms * core->get_kernel_param().max_thread_per_block / block_size;

  DISPATCH_INTEGRAL_FUNCTION_CORE23(bucket_range.data_type().type(), offset_t, [&] {
    cal_table_range_kernel<<<grid_size, block_size, 0, stream>>>(
        bucket_range.data<offset_t>(), sorted_table_ids_.data<int>(), num_lookup_,
        temp_lookup_range.data<int>(), batch_size_);
  });
  LessThan select_op(std::numeric_limits<int>::max());
  size_t temp_storage_nbytes = temp_select_storage.num_bytes();
  cub::DeviceSelect::If(temp_select_storage.data(), temp_storage_nbytes,
                        temp_lookup_range.data<int>(), partitioned_table_range.data<int>(),
                        d_num_selected_table_range_.data<int>(), temp_lookup_range.num_elements(),
                        select_op, stream);

  // sort
#if CUB_VERSION >= 200200
  DISPATCH_INTEGRAL_FUNCTION_CORE23(input.keys.data_type().type(), key_t, [&] {
    compose_tid_key_kernel<<<grid_size, block_size, 0, stream>>>(
        input.keys.data<key_t>(), partitioned_table_range.data<int>(), input.h_num_key,
        num_table_ + 1, static_cast<struct ComposeTidKey<key_t> *>(compose_tid_keys_input.data()));
    cub::DeviceRadixSort::SortPairs(
        cub_sort_temp_buffer_.data(), cub_sort_temp_bytes_,
        static_cast<struct ComposeTidKey<key_t> *>(compose_tid_keys_input.data()),
        static_cast<struct ComposeTidKey<key_t> *>(compose_tid_keys_output.data()),
        input.src_ids.data<uint32_t>(), output.sorted_src_ids.data<uint32_t>(), input.h_num_key,
        Decomposr<key_t>{}, 0, sizeof(struct ComposeTidKey<key_t>) * 8, stream);
    decompose_tid_key_kernel<<<grid_size, block_size, 0, stream>>>(
        static_cast<struct ComposeTidKey<key_t> *>(compose_tid_keys_output.data()), input.h_num_key,
        output.sorted_keys.data<key_t>());
  });
#else
  DISPATCH_INTEGRAL_FUNCTION_CORE23(input.keys.data_type().type(), key_t, [&] {
    cub::DeviceSegmentedRadixSort::SortPairs(
        cub_sort_temp_buffer_.data(), cub_sort_temp_bytes_, input.keys.data<key_t>(),
        output.sorted_keys.data<key_t>(), input.src_ids.data<uint32_t>(),
        output.sorted_src_ids.data<uint32_t>(), input.h_num_key, num_table_,
        partitioned_table_range.data<int>(), partitioned_table_range.data<int>() + 1, 0,
        sizeof(key_t) * 8, stream);
  });
#endif
}

IndicesSort::IndicesSort(const std::shared_ptr<CoreResourceManager> &core, int max_num_keys,
                         int batch_size, core23::DataType key_type) {
  core23::Device device(core23::DeviceType::GPU, core->get_device_id());
  core23::TensorParams params = core23::TensorParams().device(device);

  DISPATCH_INTEGRAL_FUNCTION_CORE23(key_type.type(), key_t, [&] {
    size_t temp_bytes = 0;
    // ATTENTION: cub radix sort requires NumItemT to be consistent
    auto num_items = batch_size * max_num_keys;
    cub::DeviceRadixSort::SortPairs(nullptr, temp_bytes, (key_t *)nullptr, (key_t *)nullptr,
                                    (uint32_t *)nullptr, (uint32_t *)nullptr,
                                    static_cast<int64_t>(num_items));
    d_temp_sort_storage = core23::Tensor(
        params.shape({static_cast<int64_t>(temp_bytes)}).data_type(core23::ScalarType::Char));
  });
}

void IndicesSort::operator()(embedding::SortInput &input, embedding::SortOutput &output,
                             std::shared_ptr<CoreResourceManager> core) {
  auto stream = core->get_local_gpu()->get_stream();
  auto key_type = input.keys.data_type();

  DISPATCH_INTEGRAL_FUNCTION_CORE23(key_type.type(), key_t, [&] {
    size_t temp_bytes = d_temp_sort_storage.num_bytes();
    cub::DeviceRadixSort::SortPairs(
        d_temp_sort_storage.data(), temp_bytes, input.keys.data<key_t>(),
        output.sorted_keys.data<key_t>(), input.src_ids.data<uint32_t>(),
        output.sorted_src_ids.data<uint32_t>(), static_cast<int64_t>(input.h_num_key), 0,
        sizeof(key_t) * 8, stream);
  });
}

template <typename key_t>
__global__ void get_keys_flag(const key_t *__restrict__ sorted_keys,
                              const int *__restrict__ table_ids,
                              const uint64_t *__restrict__ num_key,
                              uint32_t *__restrict__ key_flag_buffer) {
  CUDA_1D_KERNEL_LOOP(tid, *num_key) {
    key_t local_key = sorted_keys[tid];
    int table_id = table_ids[tid];
    uint32_t is_first = 0;
    if ((tid == 0) ||
        ((tid > 0) && ((sorted_keys[tid - 1] != local_key) || (table_ids[tid - 1] != table_id))))
      is_first = 1;
    key_flag_buffer[tid] = is_first;
  }
}

template <typename key_t>
__global__ void get_unique_key(const key_t *__restrict__ sorted_keys,
                               const int *__restrict__ table_ids,
                               const uint32_t *__restrict__ key_flag_buffer,
                               const uint64_t *__restrict__ num_key,
                               key_t *__restrict__ unique_keys, int *__restrict__ unique_table_ids,
                               uint64_t *__restrict__ unique_key_num,
                               uint32_t *__restrict__ dst_ids) {
  uint32_t key_num = *num_key;
  CUDA_1D_KERNEL_LOOP(tid, key_num) {
    uint32_t key_buffer = key_flag_buffer[tid];  // need size_t?
    dst_ids[tid] = key_buffer - 1;
    if ((tid > 0 && key_flag_buffer[tid - 1] != key_buffer) || tid == 0) {
      unique_keys[key_buffer - 1] = sorted_keys[tid];
      unique_table_ids[key_buffer - 1] = table_ids[tid];
    }
  }

  if (blockIdx.x * blockDim.x + threadIdx.x == 0) {
    *unique_key_num = key_flag_buffer[key_num - 1];
  }
}

template <typename key_t>
__global__ void get_unique_key_same_ev_size(
    const key_t *__restrict__ sorted_keys, const int *__restrict__ table_ids,
    const uint32_t *__restrict__ key_flag_buffer, const size_t *__restrict__ num_key,
    const int ev_size, key_t *__restrict__ unique_keys, int *__restrict__ unique_table_ids,
    uint32_t *__restrict__ unique_key_offset, size_t *__restrict__ unique_key_num,
    uint32_t *__restrict__ dst_ids) {
  int key_num = *num_key;
  CUDA_1D_KERNEL_LOOP(tid, key_num) {
    uint32_t key_buffer = key_flag_buffer[tid];  // need size_t?
    dst_ids[tid] = key_buffer - 1;
    if ((tid > 0 && key_flag_buffer[tid - 1] != key_buffer) || tid == 0) {
      unique_keys[key_buffer - 1] = sorted_keys[tid];
      unique_table_ids[key_buffer - 1] = table_ids[tid];
      unique_key_offset[key_buffer - 1] = (key_buffer - 1) * ev_size;
    }
  }

  if (blockIdx.x * blockDim.x + threadIdx.x == 0) {
    *unique_key_num = key_flag_buffer[key_num - 1];
  }
}

SegmentdUnique::SegmentdUnique(const std::shared_ptr<CoreResourceManager> &core, int max_num_keys,
                               int batch_size, bool need_allocate_wgrad_buffer, int max_ev_size) {
  need_allocate_wgrad_buffer_ = need_allocate_wgrad_buffer;
  max_ev_size_ = max_ev_size;
  core23::Device device(core23::DeviceType::GPU, core->get_device_id());
  core23::TensorParams params = core23::TensorParams().device(device);

  max_key_num_ = ((size_t)max_num_keys) * ((size_t)batch_size);
  key_flag_buffer_ = core23::Tensor(
      params.shape({static_cast<int64_t>(max_key_num_)}).data_type(core23::ScalarType::UInt32));

  cub::DeviceScan::InclusiveSum(nullptr, cub_scan_temp_bytes_, (uint32_t *)nullptr,
                                (uint32_t *)nullptr, max_key_num_);
  cub_scan_temp_buffer_ = core23::Tensor(params.shape({static_cast<int64_t>(cub_scan_temp_bytes_)})
                                             .data_type(core23::ScalarType::Char));
}

void SegmentdUnique::operator()(const core23::Tensor &sorted_keys, const core23::Tensor &table_ids,
                                const core23::Tensor &key_num, Wgrad &wgrad,
                                core23::Tensor &dst_ids, size_t h_num_key, bool is_same_ev_size,
                                int ev_size, std::shared_ptr<CoreResourceManager> core) {
  auto stream = core->get_local_gpu()->get_stream();
  auto key_type = sorted_keys.data_type();
  const int block_size = 256;
  const int grid_size =
      core->get_kernel_param().num_sms * core->get_kernel_param().max_thread_per_block / block_size;
  DISPATCH_INTEGRAL_FUNCTION_CORE23(key_type.type(), key_t, [&] {
    get_keys_flag<<<grid_size, block_size, 0, stream>>>(
        sorted_keys.data<key_t>(), table_ids.data<int>(), key_num.data<uint64_t>(),
        key_flag_buffer_.data<uint32_t>());
  });

  DISPATCH_INTEGRAL_FUNCTION_CORE23(key_type.type(), key_t, [&] {
    size_t temp_bytes = cub_scan_temp_buffer_.num_bytes();
    cub::DeviceScan::InclusiveSum(cub_scan_temp_buffer_.data(), temp_bytes,
                                  key_flag_buffer_.data<uint32_t>(),
                                  key_flag_buffer_.data<uint32_t>(), h_num_key, stream);
  });

  if (need_allocate_wgrad_buffer_) {
    HCTR_CHECK_HINT((!wgrad.data_allocated && !wgrad.indices_allocated),
                    "Wgrad should not be allocate before");
    DynamicWgradInitiazlier{}.init_indices_and_data(wgrad, h_num_key, key_flag_buffer_,
                                                    max_ev_size_, core, stream);
  }

  DISPATCH_INTEGRAL_FUNCTION_CORE23(key_type.type(), key_t, [&] {
    if (is_same_ev_size) {
      get_unique_key_same_ev_size<<<grid_size, block_size, 0, stream>>>(
          sorted_keys.data<key_t>(), table_ids.data<int>(), key_flag_buffer_.data<uint32_t>(),
          key_num.data<size_t>(), ev_size, wgrad.unique_keys.data<key_t>(),
          wgrad.table_ids.data<int>(), wgrad.ev_start_indices.data<uint32_t>(),
          wgrad.num_unique_keys.data<size_t>(), dst_ids.data<uint32_t>());
    } else {
      get_unique_key<<<grid_size, block_size, 0, stream>>>(
          sorted_keys.data<key_t>(), table_ids.data<int>(), key_flag_buffer_.data<uint32_t>(),
          key_num.data<uint64_t>(), wgrad.unique_keys.data<key_t>(), wgrad.table_ids.data<int>(),
          wgrad.num_unique_keys.data<uint64_t>(), dst_ids.data<uint32_t>());
    }
  });
}

template <typename key_t>
__global__ void get_ids_flag(const key_t *__restrict__ sorted_keys, const int *table_range,
                             int table_num, uint32_t *__restrict__ ids_buffer) {
  size_t key_num = table_range[table_num];
  CUDA_1D_KERNEL_LOOP(tid, key_num) {
    int table_index = bs_upper_bound_sub_one(table_range, table_num + 1, tid);
    key_t local_key;
    local_key = sorted_keys[tid];
    size_t is_first = 0;
    if (tid > 0 && ((sorted_keys[tid - 1] != local_key) || (tid == table_range[table_index])))
      is_first = 1;
    ids_buffer[tid] = is_first;
  }
}

CalDstIds::CalDstIds(const std::shared_ptr<CoreResourceManager> &core, int max_num_keys,
                     int batch_size) {
  core23::Device device(core23::DeviceType::GPU, core->get_device_id());
  core23::TensorParams params = core23::TensorParams().device(device);
  max_key_num_ = ((size_t)max_num_keys) * ((size_t)batch_size);
  cub::DeviceScan::InclusiveSum(nullptr, cub_scan_temp_bytes_, (uint32_t *)nullptr,
                                (uint32_t *)nullptr, max_key_num_);
  cub_scan_temp_buffer_ = core23::Tensor(params.shape({static_cast<int64_t>(cub_scan_temp_bytes_)})
                                             .data_type(core23::ScalarType::Char));
}

void CalDstIds::operator()(core23::Tensor &sorted_keys, int num_table,
                           const core23::Tensor &table_range, core23::Tensor &dst_ids,
                           std::shared_ptr<CoreResourceManager> core, cudaStream_t stream) {
  auto key_type = sorted_keys.data_type();
  const int block_size = 256;
  const int grid_size =
      core->get_kernel_param().num_sms * core->get_kernel_param().max_thread_per_block / block_size;
  DISPATCH_INTEGRAL_FUNCTION_CORE23(key_type.type(), key_t, [&] {
    get_ids_flag<<<grid_size, block_size, 0, stream>>>(
        sorted_keys.data<key_t>(), table_range.data<int>(), num_table, dst_ids.data<uint32_t>());
  });

  cub::DeviceScan::InclusiveSum(cub_scan_temp_buffer_.data(), cub_scan_temp_bytes_,
                                dst_ids.data<uint32_t>(), dst_ids.data<uint32_t>(), max_key_num_,
                                stream);
}

void intra_partition_sort(SortKeyAndSrcIdOp sort_op, const PartitionedResult &partitioned_result,
                          ReductionIndices &reduction_indices,
                          std::shared_ptr<CoreResourceManager> core) {
  SortInput input{
      partitioned_result.partitioned_keys,
      partitioned_result.partitioned_src_ids,
      reduction_indices.num_elements,
      partitioned_result.partitioned_bucket_range,
  };
  SortOutput output{reduction_indices.sorted_keys, reduction_indices.src_ids};
  sort_op(input, output, core);
}

__global__ void get_dst_length_per_key(const int *__restrict__ unique_key_table_ids,
                                       const int *table_id_to_evsizes,
                                       const uint64_t *num_unique_keys, uint32_t *dst_key_offset) {
  CUDA_1D_KERNEL_LOOP(tid, *num_unique_keys) {
    int table_id = unique_key_table_ids[tid];
    dst_key_offset[tid] = table_id_to_evsizes[table_id];
  }
}

__global__ void set_unique_key_num_to_zero(uint64_t *__restrict__ num_unique_keys) {
  if (blockIdx.x == 0 && threadIdx.x == 0) num_unique_keys[0] = 0;
  return;
}

CalDstOffsetMP::CalDstOffsetMP(const std::shared_ptr<CoreResourceManager> &core, int max_num_keys,
                               int batch_size) {
  core23::Device device(core23::DeviceType::GPU, core->get_device_id());
  core23::TensorParams params = core23::TensorParams().device(device);
  max_key_num_ = ((size_t)max_num_keys) * ((size_t)batch_size);
  cub::DeviceScan::ExclusiveSum(nullptr, cub_scan_temp_bytes_, (uint32_t *)nullptr,
                                (uint32_t *)nullptr, max_key_num_);
  cub_scan_temp_buffer_ = core23::Tensor(params.shape({static_cast<int64_t>(cub_scan_temp_bytes_)})
                                             .data_type(core23::ScalarType::Char));
}

void CalDstOffsetMP::operator()(Wgrad &wgrad, std::shared_ptr<CoreResourceManager> core,
                                cudaStream_t stream) {
  const int block_size = 256;
  const int grid_size =
      core->get_kernel_param().num_sms * core->get_kernel_param().max_thread_per_block / block_size;

  get_dst_length_per_key<<<grid_size, block_size, 0, stream>>>(
      wgrad.table_ids.data<int>(), wgrad.attr.table_id_to_ev_size.data<int>(),
      wgrad.num_unique_keys.data<uint64_t>(), wgrad.ev_start_indices.data<uint32_t>());
  size_t temp_bytes = cub_scan_temp_buffer_.num_bytes();

  size_t scan_num = wgrad.is_dynamic_allocate ? wgrad.h_unique_keys : max_key_num_;
  cub::DeviceScan::ExclusiveSum(cub_scan_temp_buffer_.data(), temp_bytes,
                                wgrad.ev_start_indices.data<uint32_t>(),
                                wgrad.ev_start_indices.data<uint32_t>(), scan_num, stream);
}

void unique_keys(SegmentdUnique &segmented_unique_kernel, ReductionIndices &reduction_indices,
                 Wgrad &wgrad, std::shared_ptr<CoreResourceManager> core) {
  segmented_unique_kernel(reduction_indices.sorted_keys, reduction_indices.table_ids,
                          reduction_indices.num_key, wgrad, reduction_indices.dst_ids,
                          reduction_indices.num_elements, wgrad.attr.is_same_ev_size,
                          wgrad.attr.same_ev_size, core);
}

void LocalReduceIndexCalculation::cal_for_sparse_input(const EmbeddingInput &embedding_input,
                                                       SortKeyAndSrcIdOp sort_key_and_src_id_op,
                                                       SegmentdUnique &segmented_unique,
                                                       ReductionIndices &reduction_indices,
                                                       Wgrad &wgrad, int batch_size) {
  HugeCTR::CudaDeviceContext ctx(core_->get_device_id());
  HCTR_LIB_THROW(cudaGetLastError());
  reduction_indices.num_elements = embedding_input.h_num_keys;

  if (embedding_input.h_num_keys == 0) {
    set_unique_key_num_to_zero<<<1, 1, 0, core_->get_local_gpu()->get_stream()>>>(
        wgrad.num_unique_keys.data<uint64_t>());

    return;
  }

  partition_by_table_id(embedding_input.keys, embedding_input.bucket_range,
                        wgrad.attr.sorted_lookup_ids, wgrad.attr.sorted_table_ids,
                        wgrad.attr.table_id_to_ev_size, wgrad.attr.num_lookup, wgrad.attr.num_table,
                        partitioned_result_, reduction_indices, batch_size, temp_storage_, core_);
  HCTR_LIB_THROW(cudaGetLastError());

  intra_partition_sort(sort_key_and_src_id_op, partitioned_result_, reduction_indices, core_);
  HCTR_LIB_THROW(cudaGetLastError());

  unique_keys(segmented_unique, reduction_indices, wgrad, core_);
  HCTR_LIB_THROW(cudaGetLastError());
}

}  // namespace embedding
