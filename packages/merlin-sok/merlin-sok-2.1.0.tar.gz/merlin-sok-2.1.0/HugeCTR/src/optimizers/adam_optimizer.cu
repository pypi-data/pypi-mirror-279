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

#include <core23/data_type.hpp>
#include <general_buffer2.hpp>
#include <optimizers/adam_optimizer.hpp>
#include <utils.cuh>
#include <utils.hpp>

namespace HugeCTR {

namespace {

template <typename T>
__global__ void adam_update_kernel(int len, float* weight, float* m, float* v, const T* wgrad,
                                   float alpha_t, float beta1, float beta2, float epsilon,
                                   float scaler) {
  const int i = blockIdx.x * blockDim.x + threadIdx.x;
  if (i < len) {
    float gi = TypeConvertFunc<float, T>::convert(wgrad[i]) / scaler;
    float mi = beta1 * m[i] + (1.f - beta1) * gi;
    float vi = beta2 * v[i] + (1.f - beta2) * gi * gi;
    m[i] = mi;
    v[i] = vi;
    weight[i] -= alpha_t * mi / (sqrt(vi) + epsilon);
  }
}

}  // namespace

template <typename T>
AdamOptimizer<T>::AdamOptimizer(std::optional<WeightTensors> weight_tensors,
                                std::optional<WgradTensors<T>> wgrad_tensors,
                                const std::shared_ptr<GPUResource>& gpu_resource,
                                float learning_rate, float beta1, float beta2, float epsilon,
                                float scaler)
    : Optimizer(weight_tensors, gpu_resource, learning_rate, scaler),
      wgrad_tensors_(wgrad_tensors),
      t_(0),
      beta1_(beta1),
      beta2_(beta2),
      epsilon_(epsilon) {
  core23::TensorParams tensor_params =
      core23::TensorParams()
          .device(core23::Device(core23::DeviceType::GPU, gpu_resource->get_device_id()))
          .data_type(core23::ScalarType::Float)
          .shape(core23::Shape({weight_tensors_->flatten().size(0)}))
          .buffer_channel(GetOptStateBufferChannnel());

  m_tensor_ = core23::Tensor(tensor_params);
  v_tensor_ = core23::Tensor(tensor_params);
}

template <typename T>
void AdamOptimizer<T>::initialize() {
  HCTR_LIB_THROW(
      cudaMemsetAsync(m_tensor_.data(), 0, m_tensor_.num_bytes(), gpu_resource_->get_stream()));
  HCTR_LIB_THROW(
      cudaMemsetAsync(v_tensor_.data(), 0, v_tensor_.num_bytes(), gpu_resource_->get_stream()));
}

template <typename T>
void AdamOptimizer<T>::update() {
  CudaDeviceContext context(get_device_id());

  constexpr size_t block_dim = 256;

  ++t_;
  const float alpha_t = lr_ * std::sqrt(1 - std::pow(beta2_, t_)) / (1 - std::pow(beta1_, t_));

  auto flat_weight_tensor = weight_tensors_->flatten();
  auto flat_wgrad_tensor = wgrad_tensors_->flatten();
  float* weight = flat_weight_tensor.data();
  const T* wgrad = flat_wgrad_tensor.data();

  auto len = flat_weight_tensor.size(0);
  const size_t grid_dim = (len - 1) / block_dim + 1;

  float* m = m_tensor_.data<float>();
  float* v = v_tensor_.data<float>();

  adam_update_kernel<<<grid_dim, block_dim, 0, gpu_resource_->get_stream()>>>(
      len, weight, m, v, wgrad, alpha_t, beta1_, beta2_, epsilon_, scaler_);
}

template class AdamOptimizer<float>;
template class AdamOptimizer<__half>;

}  // namespace HugeCTR
