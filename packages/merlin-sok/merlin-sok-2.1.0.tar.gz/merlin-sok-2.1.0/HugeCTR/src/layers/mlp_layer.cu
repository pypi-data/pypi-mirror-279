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

#include <layers/mlp_layer.hpp>
#include <type_traits>

namespace HugeCTR {

template class MLPLayer<float>;
template class MLPLayer<__half>;

template <typename T>
MLPLayer<T>::MLPLayer(const std::vector<core23::Tensor>& bottom_tensors,
                      const std::vector<core23::Tensor>& top_tensors,
                      const std::vector<int64_t>& num_outputs,
                      const std::shared_ptr<GPUResource>& gpu_resource,
                      const std::vector<Activation_t>& acts, const std::vector<bool>& use_bias,
                      std::vector<Initializer_t> initializer_types, bool skip_head_dgrad,
                      bool async_wgrad, bool fuse_wb, bool enable_tf32_compute)
    : TrainableLayer<T>(bottom_tensors, top_tensors, gpu_resource, initializer_types),
      num_outputs_(num_outputs),
      acts_(acts),
      use_bias_(use_bias),
      skip_head_dgrad_(skip_head_dgrad),
      async_wgrad_(async_wgrad),
      fuse_wb_(fuse_wb),
      enable_tf32_compute_(enable_tf32_compute),
      event_overlap_created_(false) {
  int num_layers = num_outputs.size();
  train_tensors_.resize(num_layers);
  mask_tensors_.resize(num_layers);
  output_mask_.resize(num_layers);
  dact_tensors_.resize(num_layers);
  layer_desc_.resize(num_layers);
  layer_algo_.resize(num_layers);

  for (int i = 0; i < num_layers; i++) {
    const auto& bottom_tensor_dim =
        i == 0 ? this->input_tensors_[0].shape() : train_tensors_[i - 1].shape();
    int64_t batch_size = bottom_tensor_dim.size(0);
    int64_t input_size = bottom_tensor_dim.size(1);
    int64_t output_size = num_outputs[i];

    core23::Shape kernel_dim = {input_size, output_size};
    core23::Shape bias_dim = {1, output_size};

    this->set_weight(i * 2, kernel_dim);
    kernels_.push_back(this->get_weight(i * 2));
    this->set_weight(i * 2 + 1, bias_dim);
    biases_.push_back(this->get_weight(i * 2 + 1));
    this->set_wgrad(i * 2, kernel_dim);
    kernels_grad_.push_back(this->get_wgrad(i * 2));
    this->set_wgrad(i * 2 + 1, bias_dim);
    db_tensors_.push_back(this->get_wgrad(i * 2 + 1));

    const auto& train_in_tensor = i == 0 ? this->input_tensors_[0] : train_tensors_[i - 1];
    int64_t num_output = num_outputs[i];

    core23::BufferParams buffer_params = {};
    buffer_params.channel = GetBlobsBufferChannel();
    core23::Device device(core23::DeviceType::GPU, gpu_resource->get_device_id());

    if (i != num_layers - 1) {
      core23::Shape shape({train_in_tensor.shape().size(0), num_output});
      auto data_type = core23::ToScalarType<T>::value;
      train_tensors_[i] = core23::Tensor(
          core23::TensorParams().data_type(data_type).shape(shape).device(device).buffer_params(
              buffer_params));
      if (acts_[i] == Activation_t::Relu) {
        mask_tensors_[i] = core23::Tensor(
            core23::TensorParams().data_type(data_type).shape(shape).device(device).buffer_params(
                buffer_params));
        dact_tensors_[i] = core23::Tensor(
            core23::TensorParams().data_type(data_type).shape(shape).device(device).buffer_params(
                buffer_params));
      }
    } else {
      core23::Shape shape({train_in_tensor.shape().size(0), num_output});
      auto data_type = core23::ToScalarType<T>::value;

      train_tensors_[i] = this->output_tensors_[0];
      if (this->output_tensors_.size() == 1) {
        if (acts_[i] == Activation_t::Relu) {
          mask_tensors_[i] = core23::Tensor(
              core23::TensorParams().data_type(data_type).shape(shape).device(device).buffer_params(
                  buffer_params));
        }
        dact_tensors_[i] = core23::Tensor(
            core23::TensorParams().data_type(data_type).shape(shape).device(device).buffer_params(
                buffer_params));
      }
    }

    output_mask_[i] = (acts_[i] == Activation_t::Relu) && (i != num_layers - 1);
  }
}

template <typename T>
void MLPLayer<T>::fprop(bool is_train) {
  CudaDeviceContext context(this->get_device_id());
  int num_layers = num_outputs_.size();
  for (int i = 0; i < num_layers; i++) {
    const T* kernel = kernels_[i].data<T>();
    const T* bottom =
        i == 0 ? this->input_tensors_[0].template data<T>() : train_tensors_[i - 1].data<T>();
    T* top_fprop = train_tensors_[i].data<T>();
    layer_functors_.fprop(kernel, bottom, top_fprop, layer_desc_[i], layer_algo_[i],
                          this->get_gpu().get_cublaslt_handle(), this->get_gpu().get_stream());
    if (i == num_layers - 1 && acts_[i] == Activation_t::Relu) {
      T* mask_out = mask_tensors_[i].data<T>();
      int64_t len = train_tensors_[i].num_elements();
      HCTR_LIB_THROW(cudaMemcpyAsync(mask_out, top_fprop, len * sizeof(T), cudaMemcpyDeviceToDevice,
                                     this->get_gpu().get_stream()));
    }
  }
}

template <typename T>
void MLPLayer<T>::bprop() {
  CudaDeviceContext context(this->get_device_id());

  int num_layers = num_outputs_.size();
  for (int i = num_layers - 1; i >= 0; i--) {
    const auto& bottom_tensor_dim =
        i == 0 ? this->input_tensors_[0].shape() : train_tensors_[i - 1].shape();
    int64_t batch_size = bottom_tensor_dim.size(0);
    int64_t top_size = num_outputs_[i];

    const T* kernel = kernels_[i].data<T>();
    const T* train_top = train_tensors_[i].data<T>();

    // Only the last layer needs the mask of itself to get the grad.
    const T* mask_top = (i == num_layers - 1 && acts_[i] == Activation_t::Relu)
                            ? mask_tensors_[i].data<T>()
                            : nullptr;

    T* grad_top =
        acts_[i] == Activation_t::None ? train_tensors_[i].data<T>() : dact_tensors_[i].data<T>();
    T* kernel_grad = kernels_grad_[i].data<T>();
    T* bottom =
        i == 0 ? this->input_tensors_[0].template data<T>() : train_tensors_[i - 1].data<T>();
    bool enable_async_wgrad = async_wgrad_;
    T* bottom_bprop = nullptr;
    if (i != 0) {
      bottom_bprop = acts_[i - 1] == Activation_t::None ? train_tensors_[i - 1].data<T>()
                                                        : dact_tensors_[i - 1].data<T>();
    } else {
      if (this->input_tensors_.size() == 1) {
        // train_in_tensor
        bottom_bprop = this->input_tensors_[0].template data<T>();
        enable_async_wgrad = false;
      } else {
        bottom_bprop = this->input_tensors_[1].template data<T>();
      }
    }
    layer_functors_.bprop(kernel, bottom, train_top, mask_top, batch_size * top_size, grad_top,
                          bottom_bprop, kernel_grad, layer_desc_[i], layer_algo_[i],
                          this->get_gpu().get_cublaslt_handle(), this->get_gpu().get_stream(),
                          this->get_gpu().get_comp_overlap_stream(), event_overlap_,
                          enable_async_wgrad, i == 0 ? skip_head_dgrad_ : false);
  }

  if (async_wgrad_) {
    HCTR_LIB_THROW(cudaEventRecord(event_overlap_, this->get_gpu().get_comp_overlap_stream()));
    HCTR_LIB_THROW(cudaStreamWaitEvent(this->get_gpu().get_stream(), event_overlap_));
  }
}

template <typename T>
void MLPLayer<T>::initialize() {
  CudaDeviceContext context(this->get_device_id());

  HCTR_LIB_THROW(cudaEventCreate(&event_overlap_));
  event_overlap_created_ = true;

  int num_layers = num_outputs_.size();
  for (int i = 0; i < num_layers; i++) {
    const auto& bottom_tensor_dim =
        i == 0 ? this->input_tensors_[0].shape() : train_tensors_[i - 1].shape();
    int64_t batch_size = bottom_tensor_dim.size(0);
    int64_t input_size = bottom_tensor_dim.size(1);
    int64_t output_size = num_outputs_[i];

    const T* bias_ptr = nullptr;
    if (use_bias_[i]) {
      bias_ptr = biases_[i].data<T>();
    }

    T* mask_out_ptr = nullptr;
    bool output_mask = output_mask_[i];
    if (output_mask) {
      mask_out_ptr = mask_tensors_[i].data<T>();
    }
    layer_desc_[i].set_fprop_attr(bias_ptr, acts_[i], mask_out_ptr, batch_size, input_size,
                                  output_size, enable_tf32_compute_);

    T* mask_in_ptr = nullptr;
    if (i > 0) {
      if (acts_[i - 1] == Activation_t::Relu) {
        mask_in_ptr = mask_tensors_[i - 1].data<T>();
      }
    }
    T* dbias_bottom_ptr = nullptr;
    T* dbias_top_ptr = nullptr;
    // If there is no ReLu, then dbias should be fused with wgrad.
    // Compute the bias gradient for this layer.
    if (fuse_wb_ || i == num_layers - 1 || acts_[i] == Activation_t::None) {
      if (use_bias_[i]) {
        dbias_top_ptr = db_tensors_[i].data<T>();
      }
    }
    // Compute the bias gradient for bottom layer. For the last layer of MLP, it should compute both
    // gradients.
    if (!fuse_wb_ && i > 0 && use_bias_[i - 1] && acts_[i - 1] != Activation_t::None) {
      dbias_bottom_ptr = db_tensors_[i - 1].data<T>();
    }
    layer_desc_[i].set_bprop_attr(dbias_bottom_ptr, dbias_top_ptr, mask_in_ptr, batch_size,
                                  input_size, output_size, enable_tf32_compute_);
    layer_algo_[i].set_fprop_algo(layer_desc_[i], this->get_gpu().get_cublaslt_handle());
    layer_algo_[i].set_bprop_algo(layer_desc_[i], this->get_gpu().get_cublaslt_handle());
  }
}

template <typename T>
void MLPLayer<T>::search_algorithm() {
  CudaDeviceContext context(this->get_device_id());
  int num_layers = num_outputs_.size();
  for (int i = 0; i < num_layers; i++) {
    T* kernel = kernels_[i].data<T>();
    T* bottom =
        i == 0 ? this->input_tensors_[0].template data<T>() : train_tensors_[i - 1].data<T>();
    T* top = train_tensors_[i].data<T>();

    const auto& bottom_tensor_dim =
        i == 0 ? this->input_tensors_[0].shape() : train_tensors_[i - 1].shape();
    int64_t batch_size = bottom_tensor_dim.size(0);
    int64_t input_size = bottom_tensor_dim.size(1);
    int64_t output_size = num_outputs_[i];

    layer_functors_.search_algorithm(
        bottom, top, kernel, batch_size, input_size, output_size, layer_desc_[i], layer_algo_[i],
        this->get_gpu().get_cublaslt_handle(), this->get_gpu().get_stream());
  }
}

template <typename T>
std::unique_ptr<DataSimulator> MLPLayer<T>::get_uniform_initializer(const int index) {
  int i = index / 2;
  int64_t bottom_dim =
      i == 0 ? this->input_tensors_[0].shape().size(1) : train_tensors_[i - 1].shape().size(1);
  float limit = sqrt(1.0f / (bottom_dim));
  return std::make_unique<UniformDataSimulator>(-1 * limit, limit);
}

template <typename T>
std::unique_ptr<DataSimulator> MLPLayer<T>::get_xavier_uniform_initializer(const int index) {
  int i = index / 2;
  int64_t bottom_dim =
      i == 0 ? this->input_tensors_[0].shape().size(1) : train_tensors_[i - 1].shape().size(1);
  int64_t top_dim = train_tensors_[i].shape().size(1);
  // fan_avg for weight
  // fan_out for bias
  auto fan_mode = i % 2 ? data_simu::Mode_t::Fan_out : data_simu::Mode_t::Fan_avg;
  return std::make_unique<VarianceScalingSimulator>(
      1.f, fan_mode, data_simu::Distribution_t::Uniform, bottom_dim, top_dim);
}
template <typename T>
std::unique_ptr<DataSimulator> MLPLayer<T>::get_xavier_norm_initializer(const int index) {
  int i = index / 2;
  int64_t bottom_dim =
      i == 0 ? this->input_tensors_[0].shape().size(1) : train_tensors_[i - 1].shape().size(1);
  int64_t top_dim = train_tensors_[i].shape().size(1);
  // fan_avg for weight
  // fan_out for bias
  auto fan_mode = i % 2 ? data_simu::Mode_t::Fan_out : data_simu::Mode_t::Fan_avg;
  return std::make_unique<VarianceScalingSimulator>(1.f, fan_mode, data_simu::Distribution_t::Norm,
                                                    bottom_dim, top_dim);
}

template <typename T>
std::unique_ptr<DataSimulator> MLPLayer<T>::get_default_initializer(const int index) {
  return this->get_uniform_initializer(index);
}

}  // namespace HugeCTR
