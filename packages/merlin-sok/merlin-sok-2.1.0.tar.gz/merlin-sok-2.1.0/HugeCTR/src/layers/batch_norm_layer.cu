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
#include <layers/batch_norm_layer.hpp>
#include <string>
#include <utils.hpp>

namespace HugeCTR {

namespace {

template <typename T>
using ToStringType = typename std::conditional<std::is_same<T, __half>::value, float, T>::type;
}

template <typename T>
BatchNormLayer<T>::BatchNormLayer(const core23::Tensor& in_tensor, const core23::Tensor& out_tensor,
                                  const Params& params,
                                  const std::shared_ptr<GPUResource>& gpu_resource,
                                  std::vector<Initializer_t> initializer_types)
    : Base({in_tensor}, {out_tensor}, gpu_resource, initializer_types),
      params_(params),
      mode_(CUDNN_BATCHNORM_PER_ACTIVATION) {
  CudaDeviceContext context(this->get_device_id());
  const auto& in_tensor_dim = in_tensor.shape();
  const auto& out_tensor_dim = out_tensor.shape();

  assert(in_tensor_dim.size() == out_tensor_dim.size());
  assert(in_tensor_dim.dims() == 2 && out_tensor_dim.dims() == 2);
  assert(in_tensor_dim.size(0) == out_tensor_dim.size(0));
  assert(in_tensor_dim.size(1) == out_tensor_dim.size(1));

  HCTR_LIB_THROW(cudnnCreateTensorDescriptor(&in_out_desc_));

  int64_t num_feature = in_tensor_dim.size(1);
  int batch_size = in_tensor_dim.size(0);

  cudnnDataType_t data_type = std::is_same<T, __half>::value ? CUDNN_DATA_HALF : CUDNN_DATA_FLOAT;
  int n_stride = num_feature;
  int w_stride = 1;

  HCTR_LIB_THROW(cudnnSetTensor4dDescriptorEx(in_out_desc_, data_type, batch_size, 1, 1,
                                              num_feature, n_stride, 1, 1, w_stride));

  HCTR_LIB_THROW(cudnnCreateTensorDescriptor(&gamma_beta_desc_));

  HCTR_LIB_THROW(cudnnDeriveBNTensorDescriptor(gamma_beta_desc_, in_out_desc_, mode_));

  core23::Shape gamma_dim = {num_feature, 1};

  // gamma & beta
  this->set_weight(0, gamma_dim);
  this->set_weight(1, gamma_dim);

  gamma_ = this->get_weight(0);
  beta_ = this->get_weight(1);
  // gamma grad & beta grad
  this->set_wgrad(0, gamma_dim);
  this->set_wgrad(1, gamma_dim);
  gamma_grad_ = this->get_wgrad(0);
  beta_grad_ = this->get_wgrad(1);

  core23::BufferParams blobs_buffer_params = {};
  blobs_buffer_params.channel = GetBlobsBufferChannel();
  core23::Device device(core23::DeviceType::GPU, gpu_resource->get_device_id());

  // result running mean & var
  result_running_mean_ = core23::Tensor(core23::TensorParams()
                                            .data_type(core23::ToScalarType<float>::value)
                                            .shape(gamma_dim)
                                            .device(device)
                                            .buffer_params(blobs_buffer_params));

  result_running_var_ = core23::Tensor(core23::TensorParams()
                                           .data_type(core23::ToScalarType<float>::value)
                                           .shape(gamma_dim)
                                           .device(device)
                                           .buffer_params(blobs_buffer_params));

  // save running mean & var (cache)
  result_save_mean_ = core23::Tensor(core23::TensorParams()
                                         .data_type(core23::ToScalarType<float>::value)
                                         .shape(gamma_dim)
                                         .device(device)
                                         .buffer_params(blobs_buffer_params));

  result_save_inv_var_ = core23::Tensor(core23::TensorParams()
                                            .data_type(core23::ToScalarType<float>::value)
                                            .shape(gamma_dim)
                                            .device(device)
                                            .buffer_params(blobs_buffer_params));
}

template <typename T>
BatchNormLayer<T>::~BatchNormLayer() {
  try {
    HCTR_LIB_THROW(cudnnDestroyTensorDescriptor(in_out_desc_));
    HCTR_LIB_THROW(cudnnDestroyTensorDescriptor(gamma_beta_desc_));
  } catch (const std::runtime_error& rt_err) {
    HCTR_LOG_S(ERROR, WORLD) << rt_err.what() << std::endl;
  }
}

template <typename T>
void BatchNormLayer<T>::initialize() {
  // host array to get running mean & var

  int64_t num_feature = this->input_tensors_[0].shape().size(1);

  h_result_running_mean_ = core23::Tensor(core23::TensorParams()
                                              .data_type(core23::ToScalarType<float>::value)
                                              .shape({num_feature})
                                              .device(core23::DeviceType::CPU));

  h_result_running_var_ = core23::Tensor(core23::TensorParams()
                                             .data_type(core23::ToScalarType<float>::value)
                                             .shape({num_feature})
                                             .device(core23::DeviceType::CPU));
}

template <typename T>
void BatchNormLayer<T>::fprop(bool is_train) {
  CudaDeviceContext context(this->get_device_id());
  float one = 1.0f, zero = 0.0f;

  core23::Tensor& in_tensor = this->input_tensors_[0];
  core23::Tensor& out_tensor = this->output_tensors_[0];
  T* in = in_tensor.data<T>();
  T* out = out_tensor.data<T>();

  float* gamma = gamma_.data<float>();
  float* beta = beta_.data<float>();

  float* result_running_mean = result_running_mean_.data<float>();
  float* result_running_var = result_running_var_.data<float>();
  float* result_save_mean = result_save_mean_.data<float>();
  float* result_save_inv_var = result_save_inv_var_.data<float>();

  if (is_train) {
    HCTR_LIB_THROW(cudnnBatchNormalizationForwardTraining(
        this->get_gpu().get_cudnn_handle(), mode_, &one, &zero, in_out_desc_, in, in_out_desc_, out,
        gamma_beta_desc_, gamma, beta, params_.factor, result_running_mean, result_running_var,
        params_.eps, result_save_mean, result_save_inv_var));
  } else {
    HCTR_LIB_THROW(cudnnBatchNormalizationForwardInference(
        this->get_gpu().get_cudnn_handle(), mode_, &one, &zero, in_out_desc_, in, in_out_desc_, out,
        gamma_beta_desc_, gamma, beta, result_running_mean, result_running_var, params_.eps));
  }
}

template <typename T>
void BatchNormLayer<T>::bprop() {
  CudaDeviceContext context(this->get_device_id());

  float one = 1.0f, zero = 0.0f;

  core23::Tensor& in_tensor = this->input_tensors_[0];
  core23::Tensor& out_tensor = this->output_tensors_[0];
  T* in = in_tensor.data<T>();
  T* out = out_tensor.data<T>();

  float* gamma = gamma_.data<float>();

  float* gamma_grad = gamma_grad_.data<float>();
  float* beta_grad = beta_grad_.data<float>();

  float* result_save_mean = result_save_mean_.data<float>();
  float* result_save_inv_var = result_save_inv_var_.data<float>();

  HCTR_LIB_THROW(cudnnBatchNormalizationBackward(
      this->get_gpu().get_cudnn_handle(), mode_, &one, &zero, &one, &zero, in_out_desc_, in,
      in_out_desc_, out, in_out_desc_, in, gamma_beta_desc_, gamma, gamma_grad, beta_grad,
      params_.eps, result_save_mean, result_save_inv_var));
}

template <typename T>
std::string BatchNormLayer<T>::get_no_trained_params_in_string() {
  float* d_result_running_mean = result_running_mean_.data<float>();
  float* d_result_running_var = result_running_var_.data<float>();
  int64_t n_byte = result_running_mean_.num_bytes();

  int64_t n_elem = n_byte / sizeof(T);

  HCTR_LIB_THROW(cudaMemcpy(h_result_running_mean_.data(), d_result_running_mean, n_byte,
                            cudaMemcpyDeviceToHost));
  HCTR_LIB_THROW(cudaMemcpy(h_result_running_var_.data(), d_result_running_var, n_byte,
                            cudaMemcpyDeviceToHost));

  std::string result = "      \"type\": \"BatchNorm\",\n";
  result += "      \"mean\": [";
  for (int64_t i = 0; i < n_elem; i++) {
    result += std::to_string(ToStringType<T>(h_result_running_mean_.data<float>()[i]));
    if (i != (n_elem - 1)) result += ", ";
  }
  result += "],\n";

  result += "      \"var\": [";
  for (int64_t i = 0; i < n_elem; i++) {
    result += std::to_string(ToStringType<T>(h_result_running_var_.data<float>()[i]));
    if (i != (n_elem - 1)) result += ", ";
  }
  result += "]";

  return result;
}

template <typename T>
std::vector<core23::Tensor> BatchNormLayer<T>::get_non_trainable_params_as_tensors() {
  return {result_running_mean_, result_running_var_};
}

template <typename T>
std::unique_ptr<DataSimulator> BatchNormLayer<T>::get_default_initializer(const int index) {
  std::unique_ptr<DataSimulator> simu;
  if (0 == index) {
    simu.reset(new ConstantDataSimulator(1.0f));
  } else if (1 == index) {
    simu.reset(new ConstantDataSimulator(0.0f));
  } else {
    HCTR_OWN_THROW(Error_t::OutOfBound, "index != {0, 1}.");
  }
  return simu;
}

template class BatchNormLayer<float>;
template class BatchNormLayer<__half>;
}  // namespace HugeCTR
