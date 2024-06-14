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

#include <layer.hpp>

namespace HugeCTR {

/**
 * Elu activation function as a derived class of Layer
 */
template <typename T>
class EluLayer : public Layer {
 public:
  EluLayer(const core23::Tensor& input_tensor, const core23::Tensor& output_tensor, T alpha,
           const std::shared_ptr<GPUResource>& gpu_resource);
  /**
   * A method of implementing the forward pass of Relu
   * @param stream CUDA stream where the forward propagation is executed
   */
  void fprop(bool is_train) override;
  /**
   * A method of implementing the backward pass of Relu
   * @param stream CUDA stream where the backward propagation is executed
   */
  void bprop() override;

 private:
  T alpha_;
};

}  // namespace HugeCTR
