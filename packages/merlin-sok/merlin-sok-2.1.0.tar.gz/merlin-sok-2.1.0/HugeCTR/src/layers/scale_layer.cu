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
#include <cuda_utils.cuh>
#include <functional>
#include <include/utils.cuh>
#include <layers/scale_layer.hpp>
#include <linalg/binary_op.cuh>
#include <linalg/reduce.cuh>
#include <linalg/unary_op.cuh>
#include <network_buffer_channels.hpp>
#include <utils.hpp>

namespace HugeCTR {
namespace {

template <typename T>
void __global__ upscale_kernel(T* out, T* in, int batchsize, int num_elems, int axis, int factor) {
  int tid = blockIdx.x * blockDim.x + threadIdx.x;
  int threads_num = blockDim.x * gridDim.x;
  int len = batchsize * num_elems;
  if (axis == 0) {
    for (int index = tid; index < len; index += threads_num) {
      for (int i = 0; i < factor; i++) {
        out[index * factor + i] = in[index];
      }
    }
  } else {
    for (int index = threadIdx.x; index < num_elems; index += blockDim.x) {
      for (int i = 0; i < factor; i++) {
        out[blockIdx.x * factor * num_elems + i * num_elems + index] =
            in[index + blockIdx.x * num_elems];
      }
    }
  }
}

template <typename T>
void __global__ downscale_kernel(T* out, T* in, int batchsize, int num_elems, int axis,
                                 int factor) {
  int tid = blockIdx.x * blockDim.x + threadIdx.x;
  int threads_num = blockDim.x * gridDim.x;
  int len = batchsize * num_elems;
  if (axis == 0) {
    for (int index = tid; index < len; index += threads_num) {
      out[index] = in[index * factor];
    }
  } else {
    for (int index = threadIdx.x; index < num_elems; index += blockDim.x) {
      out[blockIdx.x * num_elems + index] = in[index + blockIdx.x * num_elems * factor];
    }
  }
}

template <typename T>
void scale(T* out, T* in, int batchsize, int num_elems, int axis, int factor, cudaStream_t stream,
           bool forward) {
  dim3 grid(batchsize);
  dim3 block(min(num_elems, 1024));

  if (forward)
    upscale_kernel<<<grid, block, 0, stream>>>(out, in, batchsize, num_elems, axis, factor);
  else
    downscale_kernel<<<grid, block, 0, stream>>>(out, in, batchsize, num_elems, axis, factor);
}

}  // namespace

template <typename T>
ScaleLayer<T>::ScaleLayer(const core23::Tensor& in_tensor, core23::Tensor& out_tensor, int axis,
                          int factor, const std::shared_ptr<GPUResource>& gpu_resource)
    : Layer(gpu_resource) {
  assert(axis < 2);
  auto out_y = axis == 1 ? in_tensor.shape()[0] * factor : in_tensor.shape()[0];
  auto out_x = axis == 0 ? in_tensor.shape()[1] * factor : in_tensor.shape()[1];
  core23::Shape out_dims = {out_y, out_x};
  core23::BufferParams blobs_buffer_params = {};
  blobs_buffer_params.channel = GetBlobsBufferChannel();

  out_tensor =
      core23::Tensor(in_tensor.my_params().shape(out_dims).buffer_params(blobs_buffer_params));
  in_tensors_.push_back(in_tensor);
  out_tensors_.push_back(out_tensor);
  axis_ = axis;
  factor_ = factor;
}

template <typename T>
void ScaleLayer<T>::fprop(bool is_train) {
  CudaDeviceContext context(get_device_id());
  auto& in_tensor = in_tensors_[0];
  auto& out_tensor = out_tensors_[0];
  const auto& in_tensor_dim = in_tensor.shape();
  int axis = axis_;
  int factor = factor_;

  scale(out_tensor.data<T>(), in_tensor.data<T>(), in_tensor_dim[0], in_tensor_dim[1], axis, factor,
        get_gpu().get_stream(), true);
}

template <typename T>
void ScaleLayer<T>::bprop() {
  CudaDeviceContext context(get_device_id());
  auto& bottom_tensor = in_tensors_[0];
  auto& top_tensor = out_tensors_[0];
  const auto& bottom_tensor_dim = bottom_tensor.shape();
  int axis = axis_;
  int factor = factor_;

  scale(bottom_tensor.data<T>(), top_tensor.data<T>(), bottom_tensor_dim[0], bottom_tensor_dim[1],
        axis, factor, get_gpu().get_stream(), false);
}

template class ScaleLayer<float>;
// template class ScaleLayer<__half>;

}  // namespace HugeCTR
