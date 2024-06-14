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

#include <cudnn.h>

#include <layer.hpp>

namespace HugeCTR {

/**
 * Dropout layer which selects an arbitrary fraction of inputs to 0
 */
template <typename T>
class DropoutLayer : public Layer {
 public:
  DropoutLayer(const core23::Tensor& input_tensor, const core23::Tensor& output_tensor, float rate,
               const std::shared_ptr<GPUResource>& gpu_resource);
  ~DropoutLayer() override;

  /**
   * A method of implementing the forward pass of Dropout
   * @param stream CUDA stream where the forward propagation is executed
   */
  void fprop(bool is_train) override;
  /**
   * A method of implementing the backward pass of Dropout
   * @param stream CUDA stream where the backward propagation is executed
   */
  void bprop() override;

  const float* mask() const { return noise_mask_.data<float>(); }

 private:
  cudnnDropoutDescriptor_t dropout_descriptor_;
  float rate_;
  float scale_;
  void* cudnn_status_;
  core23::Tensor noise_mask_;
  cudnnTensorDescriptor_t in_out_desc_;
  size_t reserveSpaceSizeInBytes_;
};

}  // namespace HugeCTR
