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

#include <algorithm>
#include <random>

#include "common/check.h"
#include "variable/impl/det_variable.h"

namespace sok {

template <typename T>
std::vector<size_t> argsort(const std::vector<T>& array) {
  std::vector<size_t> indices(array.size());
  std::iota(indices.begin(), indices.end(), 0);
  std::sort(indices.begin(), indices.end(), [&array](size_t left, size_t right) -> bool {
    // sort indices according to corresponding array element
    return array[left] < array[right];
  });

  return indices;
}

template <typename KeyType, typename ValueType>
void gather_by_index(std::vector<size_t>& inx, KeyType* src_key, ValueType* src_value,
                     KeyType* dst_key, ValueType* dst_value, size_t num_keys, size_t value_dim) {
  for (int i = 0; i < num_keys; i++) {
    dst_key[i] = src_key[inx[i]];
    std::memcpy(dst_value + i * value_dim, src_value + (inx[i]) * value_dim,
                sizeof(ValueType) * value_dim);
  }
  return;
}

// TODO: Move this into cuco::initializer
__global__ static void setup_kernel(unsigned long long seed, curandState* states) {
  auto grid = cooperative_groups::this_grid();
  curand_init(seed, grid.thread_rank(), 0, &states[grid.thread_rank()]);
}

static void set_curand_states(curandState** states, cudaStream_t stream = 0) {
  int device;
  CUDACHECK(cudaGetDevice(&device));
  cudaDeviceProp deviceProp;
  CUDACHECK(cudaGetDeviceProperties(&deviceProp, device));
  // TODO: Use a more compatible way instead of `2048` to calculate the size.
  //       Note that the code of cuco::initializer also needs to be modified.
  // CUDACHECK(
  //     cudaMallocAsync(states, sizeof(curandState) * deviceProp.multiProcessorCount * 2048,
  //     stream));
  CUDACHECK(cudaMalloc(states, sizeof(curandState) * deviceProp.multiProcessorCount * 2048));
  std::random_device rd;
  auto seed = rd();
  setup_kernel<<<deviceProp.multiProcessorCount * 2, 1024, 0, stream>>>(seed, *states);
  // To avoid unexpected errors caused by using `states` in other non-blocking streams.
  // It's OK to do synchronization here because this method should be called very few times.
  // CUDACHECK(cudaStreamSynchronize(stream));
}

class ConstInitializer {
 private:
  float val_;

 public:
  ConstInitializer(float val) : val_(val) {}
  // Note that the `val_` below is not the `val_` in the host object, because the entire
  // `ConstInitializer` object will be passed by value to a __global__ function before
  // this __device__ function is called.
  __device__ float operator()() const { return val_; }
};

static void parse_initializer(const std::string& initializer, bool& is_const, float& val) {
  if (initializer == "random" || initializer == "") {
    is_const = false;
    return;
  }

  is_const = true;
  if (initializer == "ones") {
    val = 1.0;
  } else if (initializer == "zeros") {
    val = 0.0;
  } else {
    try {
      val = std::stof(initializer);
    } catch (std::invalid_argument& err) {
      throw std::runtime_error("Unrecognized initializer {" + initializer + "}");
    }
  }
}

template <typename KeyType, typename ValueType>
DETVariable<KeyType, ValueType>::DETVariable(size_t dimension, size_t initial_capacity,
                                             const std::string& initializer, cudaStream_t stream)
    : dimension_(dimension),
      initial_capacity_(initial_capacity),
      initializer_(initializer),
      curand_states_(nullptr) {
  if (dimension_ <= 0) {
    throw std::invalid_argument("dimension must > 0 but got " + std::to_string(dimension));
  }

  set_curand_states(&curand_states_, stream);

  bool use_const_initializer = false;
  float initial_val = 0.0;
  parse_initializer(initializer_, use_const_initializer, initial_val);

  map_ = std::make_unique<cuco::dynamic_map<KeyType, ValueType, cuco::initializer>>(
      dimension_, initial_capacity_,
      cuco::initializer(curand_states_, use_const_initializer, initial_val));
  if (!map_) {
    throw std::runtime_error("Create DET failed");
  }
  map_->initialize(stream);
}

template <typename KeyType, typename ValueType>
DETVariable<KeyType, ValueType>::~DETVariable() {
  map_->uninitialize();
  if (curand_states_) {
    CUDACHECK(cudaFree(curand_states_));
  }
}

template <typename KeyType, typename ValueType>
int64_t DETVariable<KeyType, ValueType>::rows() {
  return map_->get_size();
}

template <typename KeyType, typename ValueType>
int64_t DETVariable<KeyType, ValueType>::cols() {
  return dimension_;
}

template <typename KeyType, typename ValueType>
void DETVariable<KeyType, ValueType>::eXport(KeyType* keys, ValueType* values,
                                             cudaStream_t stream) {
  size_t num_keys = rows();
  size_t dim = cols();

  // `keys` and `values` are pointers of host memory
  KeyType* d_keys;
  CUDACHECK(cudaMallocManaged(&d_keys, sizeof(KeyType) * num_keys));
  ValueType* d_values;
  CUDACHECK(cudaMallocManaged(&d_values, sizeof(ValueType) * num_keys * dim));

  map_->eXport(d_keys, d_values, num_keys, stream);
  CUDACHECK(cudaStreamSynchronize(stream));

  std::vector<KeyType> dk_vector = std::vector<KeyType>(d_keys, d_keys + num_keys);
  auto dk_indices = argsort(dk_vector);

  gather_by_index(dk_indices, d_keys, d_values, keys, values, num_keys, dim);

  // clang-format on
  CUDACHECK(cudaFree(d_keys));
  CUDACHECK(cudaFree(d_values));
}

template <typename KeyType, typename ValueType>
void DETVariable<KeyType, ValueType>::eXport_if(KeyType* keys, ValueType* values, size_t* counter,
                                                uint64_t threshold, cudaStream_t stream) {
  throw std::runtime_error("SOK dynamic variable with DET backend don't support eXport_if");
}

template <typename KeyType, typename ValueType>
void DETVariable<KeyType, ValueType>::assign(const KeyType* keys, const ValueType* values,
                                             size_t num_keys, cudaStream_t stream) {
  size_t dim = cols();

  // `keys` and `values` are pointers of host memory
  KeyType* d_keys;
  CUDACHECK(cudaMallocManaged(&d_keys, sizeof(KeyType) * num_keys));
  ValueType* d_values;
  CUDACHECK(cudaMallocManaged(&d_values, sizeof(ValueType) * num_keys * dim));

  // clang-format off
  //CUDACHECK(cudaMemcpyAsync(d_keys, keys, sizeof(KeyType) * num_keys,
  //                          cudaMemcpyHostToDevice, stream));
  std::memcpy(d_keys,keys, sizeof(KeyType) * num_keys);
  // clang-format on
  map_->lookup(d_keys, d_values, num_keys, stream);
  CUDACHECK(cudaStreamSynchronize(stream));

  // CUDACHECK(cudaMemcpyAsync(d_values, values, sizeof(ValueType) * num_keys * dim,
  //                           cudaMemcpyHostToDevice, stream));

  std::memcpy(d_values, values, sizeof(ValueType) * num_keys * dim);
  map_->scatter_update(d_keys, d_values, num_keys, stream);
  CUDACHECK(cudaStreamSynchronize(stream));
  CUDACHECK(cudaFree(d_keys));
  CUDACHECK(cudaFree(d_values));
}

template <typename KeyType, typename ValueType>
void DETVariable<KeyType, ValueType>::lookup(const KeyType* keys, ValueType* values,
                                             size_t num_keys, cudaStream_t stream) {
  map_->lookup(keys, values, num_keys, stream);
}

template <typename KeyType, typename ValueType>
void DETVariable<KeyType, ValueType>::lookup(const KeyType* keys, ValueType** values,
                                             size_t num_keys, cudaStream_t stream) {
  map_->lookup(keys, values, num_keys, stream);
}

template <typename KeyType, typename ValueType>
void DETVariable<KeyType, ValueType>::lookup_with_evict(const KeyType* keys, KeyType* tmp_keys,
                                                        ValueType* tmp_values, ValueType* values,
                                                        uint64_t* evict_num_keys, uint64_t num_keys,
                                                        cudaStream_t stream) {
  throw std::runtime_error(
      "SOK dynamic variable with DET backend don't support lookup_with_evict!");
}

template <typename KeyType, typename ValueType>
void DETVariable<KeyType, ValueType>::copy_evict_keys(const KeyType* keys, const ValueType* values,
                                                      size_t num_keys, size_t dim,
                                                      KeyType* ret_keys, ValueType* ret_values,
                                                      cudaStream_t stream) {
  throw std::runtime_error(
      "SOK dynamic variable with DET backend don't support lookup_with_evict!");
}

template <typename KeyType, typename ValueType>
void DETVariable<KeyType, ValueType>::scatter_add(const KeyType* keys, const ValueType* values,
                                                  size_t num_keys, cudaStream_t stream) {
  map_->scatter_add(keys, values, num_keys, stream);
}

template <typename KeyType, typename ValueType>
void DETVariable<KeyType, ValueType>::scatter_update(const KeyType* keys, const ValueType* values,
                                                     size_t num_keys, cudaStream_t stream) {
  map_->scatter_update(keys, values, num_keys, stream);
}

template class DETVariable<int32_t, float>;
template class DETVariable<int64_t, float>;

}  // namespace sok
