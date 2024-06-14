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

#include <algorithm>
#include <functional>
#include <include/utils.cuh>
#include <layers/sigmoid_layer.hpp>
#include <linalg/binary_op.cuh>
#include <linalg/unary_op.cuh>
#include <utils.hpp>

namespace HugeCTR {

template <typename T>
__device__ T exponential(T in) {
  return exp(in);
}
template __device__ float exponential<float>(float);
template <>
__device__ __half exponential(__half in) {
  return hexp(in);
}
template <>
__device__ __half2 exponential<__half2>(__half2 in) {
  return h2exp(in);
}

template <typename T>
SigmoidLayer<T>::SigmoidLayer(const core23::Tensor& input_tensor,
                              const core23::Tensor& output_tensor,
                              const std::shared_ptr<GPUResource>& gpu_resource)
    : Layer({input_tensor}, {output_tensor}, gpu_resource) {
  assert(input_tensors_[0].num_elements() == output_tensors_[0].num_elements());
  assert(input_tensors_[0].num_elements() % 2 == 0);
}

template <typename T>
void SigmoidLayer<T>::fprop(bool is_train) {
  CudaDeviceContext context(get_device_id());

  int len = input_tensors_[0].num_elements();

  auto fop = [] __device__(T in) { return T(1) / (T(1) + exponential(-in)); };

  MLCommon::LinAlg::unaryOp(output_tensors_[0].data<T>(), input_tensors_[0].data<T>(), len, fop,
                            get_gpu().get_stream());
}

template <>
void SigmoidLayer<__half>::fprop(bool is_train) {
  CudaDeviceContext context(get_device_id());

  int len = input_tensors_[0].num_elements();

  const __half2 one2 = __float2half2_rn(1.0f);
  auto fop = [one2] __device__(__half2 in) { return one2 / (one2 + exponential(-in)); };

  MLCommon::LinAlg::unaryOp(reinterpret_cast<__half2*>(output_tensors_[0].data<__half>()),
                            reinterpret_cast<__half2*>(input_tensors_[0].data<__half>()), len / 2,
                            fop, get_gpu().get_stream());
}

template <typename T>
void SigmoidLayer<T>::bprop() {
  CudaDeviceContext context(get_device_id());

  int len = input_tensors_[0].num_elements();

  auto bop = [] __device__(T d_out, T d_in) {
    T y = T(1) / (T(1) + exponential(-d_in));
    return d_out * y * (T(1) - y);
  };

  MLCommon::LinAlg::binaryOp(input_tensors_[0].data<T>(), output_tensors_[0].data<T>(),
                             input_tensors_[0].data<T>(), len, bop, get_gpu().get_stream());
}

template <>
void SigmoidLayer<__half>::bprop() {
  CudaDeviceContext context(get_device_id());

  int len = input_tensors_[0].num_elements();

  const __half2 one2 = __float2half2_rn(1.0f);
  auto bop = [one2] __device__(__half2 d_out, __half2 d_in) {
    __half2 y = one2 / (one2 + exponential(-d_in));
    return d_out * y * (one2 - y);
  };

  MLCommon::LinAlg::binaryOp(reinterpret_cast<__half2*>(input_tensors_[0].data<__half>()),
                             reinterpret_cast<__half2*>(output_tensors_[0].data<__half>()),
                             reinterpret_cast<__half2*>(input_tensors_[0].data<__half>()), len / 2,
                             bop, get_gpu().get_stream());
}

template class SigmoidLayer<float>;
template class SigmoidLayer<__half>;

}  // namespace HugeCTR
