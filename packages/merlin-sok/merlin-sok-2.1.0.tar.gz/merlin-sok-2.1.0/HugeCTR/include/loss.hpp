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
#pragma once

#include <functional>
#include <regularizer.hpp>
#include <vector>

namespace HugeCTR {

class ILoss {
 public:
  virtual ~ILoss() = 0;
  virtual void compute(bool is_train, long long current_batchsize, float rterm) = 0;
  virtual void compute_and_init(bool is_train, long long current_batchsize) = 0;
  virtual void compute_and_init(bool is_train) = 0;
  virtual int get_device_id() const = 0;
  virtual float regularizer_compute_rterm() = 0;
  virtual void regularizer_initialize_wgrad(bool is_train) = 0;

  virtual float get_label_weight() const = 0;
  virtual void set_label_weight(float new_weight) = 0;

  virtual const std::vector<core23::Tensor>& get_loss_tensors() const = 0;
};

/**
 * @brief
 *
 * Implements three kinds of loss calculations, cross entropy, binary cross entropy
 * and the multi-class cross-entropy loss.
 *
 * Loss is the base class.
 *
 * The forward and backward passes are fused into one function called compute.
 *
 */
template <typename T>
class Loss : public ILoss {
  std::shared_ptr<Regularizer<T>> regularizer_;
  std::shared_ptr<GPUResource> gpu_resource_;
  int total_gpu_count_;
  float scaler_;

  /**
   * label_tensors_(type: float): stores the label information during the training process.
   */
  std::vector<core23::Tensor> label_tensors_;

  /**
   * input_tensors_(type: T): at beginning, the input_tensors_ stores the result of the last layer
   * for the final loss calculation.
   *
   * After the train is called, the input_tensors_ will be updated to the input
   * gradient values for the backward pass.
   */
  std::vector<core23::Tensor> input_tensors_;
  /**
   * loss_tensors_(type: float): contains a single value, which stores the average cross entropy,
   * binary cross entropy or multi-class cross entropy loss value.
   */
  std::vector<core23::Tensor> loss_tensors_;

  float label_weight;

  virtual void do_compute(T* input, const float* label, float* loss, int batch_size,
                          int feature_dim, float scaler, float rterm, float label_weight,
                          bool is_train, cudaStream_t stream) = 0;

  const std::vector<core23::Tensor>& get_label_tensors(bool is_train) const {
    return label_tensors_;
  }
  std::vector<core23::Tensor>& get_input_tensors(bool is_train) { return input_tensors_; }

 protected:
  bool gen_loss_summary_;
  int get_total_gpu_count() const { return total_gpu_count_; }
  const GPUResource& get_gpu() const { return *gpu_resource_; }

 public:
  /**
   * @brief
   * Forward and backward passes are fused into one function.
   *
   * gradient values to prevent the overflow issue.
   *
   * @param is_train whether it is on training or evaluating
   * @param current_batchsize loss we set batchsize - current_batchsize rows of dgrad to 0
   */
  void compute(bool is_train, long long current_batchsize, float rterm) override;
  void compute_and_init(bool is_train, long long current_batchsize) override;
  void compute_and_init(bool is_train) override;

  Loss(const core23::Tensor& label_tensor, const core23::Tensor& input_tensor,
       const core23::Tensor& loss_tensor, const std::shared_ptr<Regularizer<T>>& regularizer,
       const std::shared_ptr<GPUResource>& gpu_resource, int total_gpu_count, float scaler = 1.0,
       bool gen_loss_summary = true);
  Loss(const Loss&) = delete;
  Loss& operator=(const Loss&) = delete;
  ~Loss() override {}

  int get_device_id() const override { return gpu_resource_->get_device_id(); }

  float regularizer_compute_rterm();
  void regularizer_initialize_wgrad(bool is_train);

  float get_label_weight() const override { return label_weight; }
  void set_label_weight(float new_weight) override { label_weight = new_weight; }

  const std::vector<core23::Tensor>& get_loss_tensors() const override { return loss_tensors_; }
};

template <typename T>
class CrossEntropyLoss : public Loss<T> {
 public:
  void do_compute(T* input, const float* label, float* loss, int batch_size, int feature_dim,
                  float scaler, float rterm, float label_weight, bool is_train,
                  cudaStream_t stream) override final;

  CrossEntropyLoss(const core23::Tensor& label_tensor, const core23::Tensor& input_tensor,
                   const core23::Tensor& loss_tensor,
                   const std::shared_ptr<Regularizer<T>>& regularizer,
                   const std::shared_ptr<GPUResource>& gpu_resource, int total_gpu_count,
                   float scaler = 1.f, bool gen_loss_summary = true);
};

template <typename T>
class BinaryCrossEntropyLoss : public Loss<T> {
 public:
  void do_compute(T* input, const float* label, float* loss, int batch_size, int feature_dim,
                  float scaler, float rterm, float label_weight, bool is_train,
                  cudaStream_t stream) override final;
  BinaryCrossEntropyLoss(const core23::Tensor& label_tensor, const core23::Tensor& input_tensor,
                         const core23::Tensor& loss_tensor,
                         const std::shared_ptr<Regularizer<T>>& regularizer,
                         const std::shared_ptr<GPUResource>& gpu_resource, int total_gpu_count,
                         float scaler = 1.f, bool gen_loss_summary = true);
};

template <typename T>
class MultiCrossEntropyLoss : public Loss<T> {
 private:
  core23::Tensor target_weight_;

 public:
  void do_compute(T* input, const float* label, float* loss, int batch_size, int feature_dim,
                  float scaler, float rterm, float label_weight, bool is_train,
                  cudaStream_t stream) override final;
  MultiCrossEntropyLoss(const core23::Tensor& label_tensor, const core23::Tensor& input_tensor,
                        const core23::Tensor& loss_tensor,
                        const std::shared_ptr<Regularizer<T>>& regularizer,
                        const std::vector<float>& target_weight,
                        const std::shared_ptr<GPUResource>& gpu_resource, int total_gpu_count,
                        float scaler = 1.f, bool gen_loss_summary = true);
};

}  // namespace HugeCTR
