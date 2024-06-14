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

// clang-format off
#include "tensorflow/core/framework/op_kernel.h"
#include "tensorflow/core/framework/register_types.h"
#include "tensorflow/core/framework/resource_mgr.h"

#include "variable/kernels/dummy_var.h"
// clang-format on

namespace stream_executor {
namespace gpu {
cudaStream_t AsGpuStreamValue(Stream* stream);
}  // namespace gpu
}  // namespace stream_executor

namespace tensorflow {

// -----------------------------------------------------------------------------------------------
// DummyVarAssign
// -----------------------------------------------------------------------------------------------
template <typename KeyType, typename ValueType>
class DummyVarAssignOp : public OpKernel {
 public:
  explicit DummyVarAssignOp(OpKernelConstruction* ctx) : OpKernel(ctx) {}

  void Compute(OpKernelContext* ctx) override {
    // Get DummyVar
    core::RefCountPtr<DummyVar<KeyType, ValueType>> var;
    OP_REQUIRES_OK(ctx, LookupResource(ctx, HandleFromInput(ctx, 0), &var));

    tf_shared_lock ml(*var->mu());

    const Tensor* indices = nullptr;
    OP_REQUIRES_OK(ctx, ctx->input("indices", &indices));
    const Tensor* values = nullptr;
    OP_REQUIRES_OK(ctx, ctx->input("values", &values));

    // Get num of indices
    int64_t N = indices->NumElements();

    // Get cuda stream of tensorflow
    auto device_ctx = ctx->op_device_context();
    OP_REQUIRES(ctx, device_ctx != nullptr, errors::Aborted("No valid device context."));
    cudaStream_t stream = stream_executor::gpu::AsGpuStreamValue(device_ctx->stream());

    var->Assign(indices->data(), values->data(), N, stream);
  }
};

#define REGISTER_GPU_KERNELS(key_type_tf, key_type, dtype_tf, dtype)   \
  REGISTER_KERNEL_BUILDER(Name("DummyVarAssign")                       \
                              .Device(DEVICE_GPU)                      \
                              .HostMemory("resource")                  \
                              .HostMemory("indices")                   \
                              .HostMemory("values")                    \
                              .TypeConstraint<key_type_tf>("key_type") \
                              .TypeConstraint<dtype_tf>("dtype"),      \
                          DummyVarAssignOp<key_type, dtype>)
#if TF_VERSION_MAJOR == 1
REGISTER_GPU_KERNELS(int64, int64_t, float, float);
REGISTER_GPU_KERNELS(int32, int32_t, float, float);
#else
REGISTER_GPU_KERNELS(int64_t, int64_t, float, float);
REGISTER_GPU_KERNELS(int32_t, int32_t, float, float);
#endif
#undef REGISTER_GPU_KERNELS

// -----------------------------------------------------------------------------------------------
// DummyVarExport
// -----------------------------------------------------------------------------------------------
template <typename KeyType, typename ValueType>
class DummyVarExportOp : public OpKernel {
 public:
  explicit DummyVarExportOp(OpKernelConstruction* ctx) : OpKernel(ctx) {}

  void Compute(OpKernelContext* ctx) override {
    // Get DummyVar
    core::RefCountPtr<DummyVar<KeyType, ValueType>> var;
    OP_REQUIRES_OK(ctx, LookupResource(ctx, HandleFromInput(ctx, 0), &var));

    tf_shared_lock ml(*var->mu());

    // Get shape
    int64_t rows = var->rows();
    int64_t cols = var->cols();

    // Allocate output
    Tensor* indices = nullptr;
    OP_REQUIRES_OK(ctx, ctx->allocate_output(0, {rows}, &indices));
    Tensor* values = nullptr;
    OP_REQUIRES_OK(ctx, ctx->allocate_output(1, {rows, cols}, &values));

    // Get cuda stream of tensorflow
    auto device_ctx = ctx->op_device_context();
    OP_REQUIRES(ctx, device_ctx != nullptr, errors::Aborted("No valid device context."));
    cudaStream_t stream = stream_executor::gpu::AsGpuStreamValue(device_ctx->stream());

    var->Export(indices->data(), values->data(), stream);
  }
};

#define REGISTER_GPU_KERNELS(key_type_tf, key_type, dtype_tf, dtype)   \
  REGISTER_KERNEL_BUILDER(Name("DummyVarExport")                       \
                              .Device(DEVICE_GPU)                      \
                              .HostMemory("resource")                  \
                              .HostMemory("indices")                   \
                              .HostMemory("values")                    \
                              .TypeConstraint<key_type_tf>("key_type") \
                              .TypeConstraint<dtype_tf>("dtype"),      \
                          DummyVarExportOp<key_type, dtype>)
#if TF_VERSION_MAJOR == 1
REGISTER_GPU_KERNELS(int64, int64_t, float, float);
REGISTER_GPU_KERNELS(int32, int32_t, float, float);
#else
REGISTER_GPU_KERNELS(int64_t, int64_t, float, float);
REGISTER_GPU_KERNELS(int32_t, int32_t, float, float);
#endif
#undef REGISTER_GPU_KERNELS

// -----------------------------------------------------------------------------------------------
// DummyVarExportIf
// -----------------------------------------------------------------------------------------------
template <typename KeyType, typename ValueType>
class DummyVarExportIfOp : public OpKernel {
 public:
  explicit DummyVarExportIfOp(OpKernelConstruction* ctx) : OpKernel(ctx) {}

  void Compute(OpKernelContext* ctx) override {
    // Get DummyVar
    core::RefCountPtr<DummyVar<KeyType, ValueType>> var;
    OP_REQUIRES_OK(ctx, LookupResource(ctx, HandleFromInput(ctx, 0), &var));

    tf_shared_lock ml(*var->mu());

    // Get shape
    int64_t rows = var->rows();
    int64_t cols = var->cols();

    const Tensor* threshold_tensor = nullptr;
    OP_REQUIRES_OK(ctx, ctx->input("threshold", &threshold_tensor));

    AllocatorAttributes alloc_attr;
    alloc_attr.set_on_host(true); 
    // temp buffer
    Tensor tmp_indices;
    OP_REQUIRES_OK(ctx, ctx->allocate_temp(DT_INT64, {rows}, &tmp_indices, alloc_attr));

    Tensor tmp_values;
    OP_REQUIRES_OK(ctx, ctx->allocate_temp(DataTypeToEnum<ValueType>::v(), {rows*cols}, &tmp_values, alloc_attr));

    Tensor counter;
    OP_REQUIRES_OK(ctx, ctx->allocate_temp(DT_UINT64, {1}, &counter, alloc_attr));
    // Get cuda stream of tensorflow
    auto device_ctx = ctx->op_device_context();
    OP_REQUIRES(ctx, device_ctx != nullptr, errors::Aborted("No valid device context."));
    cudaStream_t stream = stream_executor::gpu::AsGpuStreamValue(device_ctx->stream());
    var->ExportIf(tmp_indices.data(), tmp_values.data(),(size_t*)counter.data(),((uint64_t*)threshold_tensor->data())[0], stream);
    // Allocate output
    Tensor* indices = nullptr;
    OP_REQUIRES_OK(ctx, ctx->allocate_output(0, {((size_t*)counter.data())[0]}, &indices));
    Tensor* values = nullptr;
    OP_REQUIRES_OK(ctx, ctx->allocate_output(1, {((size_t*)counter.data())[0], cols}, &values));
    
    std::memcpy(indices->data(), tmp_indices.data(), sizeof(KeyType) * ((size_t*)counter.data())[0]);
    std::memcpy(values->data(), tmp_values.data(), sizeof(ValueType) * ((size_t*)counter.data())[0] * cols);
  }
};

#define REGISTER_GPU_KERNELS(key_type_tf, key_type, dtype_tf, dtype)   \
  REGISTER_KERNEL_BUILDER(Name("DummyVarExportIf")                     \
                              .Device(DEVICE_GPU)                      \
                              .HostMemory("resource")                  \
                              .HostMemory("threshold")                 \
                              .HostMemory("indices")                   \
                              .HostMemory("values")                    \
                              .TypeConstraint<key_type_tf>("key_type") \
                              .TypeConstraint<dtype_tf>("dtype"),      \
                          DummyVarExportIfOp<key_type, dtype>)
#if TF_VERSION_MAJOR == 1
REGISTER_GPU_KERNELS(int64, int64_t, float, float);
REGISTER_GPU_KERNELS(int32, int32_t, float, float);
#else
REGISTER_GPU_KERNELS(int64_t, int64_t, float, float);
REGISTER_GPU_KERNELS(int32_t, int32_t, float, float);
#endif
#undef REGISTER_GPU_KERNELS


// -----------------------------------------------------------------------------------------------
// DummyVarSparseRead
// -----------------------------------------------------------------------------------------------
template <typename KeyType, typename ValueType>
class DummyVarSparseReadOp : public OpKernel {
 public:
  explicit DummyVarSparseReadOp(OpKernelConstruction* ctx) : OpKernel(ctx) {}

  void Compute(OpKernelContext* ctx) override {
    core::RefCountPtr<DummyVar<KeyType, ValueType>> var;
    OP_REQUIRES_OK(ctx, LookupResource(ctx, HandleFromInput(ctx, 0), &var));

    tf_shared_lock ml(*var->mu());

    const Tensor* indices = nullptr;
    OP_REQUIRES_OK(ctx, ctx->input("indices", &indices));

    // Allocate output
    int64_t N = indices->NumElements();
    Tensor* output = nullptr;
    OP_REQUIRES_OK(ctx, ctx->allocate_output(0, {N, var->cols()}, &output));

    // Get cuda stream of tensorflow
    auto device_ctx = ctx->op_device_context();
    OP_REQUIRES(ctx, device_ctx != nullptr, errors::Aborted("No valid device context."));
    cudaStream_t stream = stream_executor::gpu::AsGpuStreamValue(device_ctx->stream());

    var->SparseRead(indices->data(), output->data(), N, stream);
  }
};

#define REGISTER_GPU_KERNELS(key_type_tf, key_type, dtype_tf, dtype)   \
  REGISTER_KERNEL_BUILDER(Name("DummyVarSparseRead")                   \
                              .Device(DEVICE_GPU)                      \
                              .HostMemory("resource")                  \
                              .TypeConstraint<key_type_tf>("key_type") \
                              .TypeConstraint<dtype_tf>("dtype"),      \
                          DummyVarSparseReadOp<key_type, dtype>)
#if TF_VERSION_MAJOR == 1
REGISTER_GPU_KERNELS(int64, int64_t, float, float);
REGISTER_GPU_KERNELS(int32, int32_t, float, float);
// REGISTER_GPU_KERNELS(int64, int64_t, Eigen::half, __half);
// REGISTER_GPU_KERNELS(int32, int32_t, Eigen::half, __half);
#else
REGISTER_GPU_KERNELS(int64_t, int64_t, float, float);
REGISTER_GPU_KERNELS(int32_t, int32_t, float, float);
// REGISTER_GPU_KERNELS(int64_t, int64_t, Eigen::half, __half);
// REGISTER_GPU_KERNELS(int32_t, int32_t, Eigen::half, __half);
#endif
#undef REGISTER_GPU_KERNELS

// -----------------------------------------------------------------------------------------------
// DummyVarSparseReadEvict
// -----------------------------------------------------------------------------------------------
template <typename KeyType, typename ValueType>
class DummyVarSparseReadEvictOp : public OpKernel {
 public:
  explicit DummyVarSparseReadEvictOp(OpKernelConstruction* ctx) : OpKernel(ctx) {}

  void Compute(OpKernelContext* ctx) override {
    core::RefCountPtr<DummyVar<KeyType, ValueType>> var;
    OP_REQUIRES_OK(ctx, LookupResource(ctx, HandleFromInput(ctx, 0), &var));

    tf_shared_lock ml(*var->mu());

    const Tensor* indices = nullptr;
    OP_REQUIRES_OK(ctx, ctx->input("indices", &indices));

    int64_t cols = var->cols();
    int64_t rows = indices->NumElements();

    AllocatorAttributes alloc_attr;
    alloc_attr.set_on_host(true); 
    // temp buffer
    Tensor tmp_indices;
    OP_REQUIRES_OK(ctx, ctx->allocate_temp(DT_INT64, {rows}, &tmp_indices));


    Tensor tmp_values;
    OP_REQUIRES_OK(ctx, ctx->allocate_temp(DataTypeToEnum<ValueType>::v(), {rows*cols}, &tmp_values));

    Tensor tmp_evict_num;
    OP_REQUIRES_OK(ctx, ctx->allocate_temp(DT_UINT64, {1}, &tmp_evict_num, alloc_attr));

    Tensor* output = nullptr;
    OP_REQUIRES_OK(ctx, ctx->allocate_output(0, {rows, cols}, &output));

    // Get cuda stream of tensorflow
    auto device_ctx = ctx->op_device_context();
    OP_REQUIRES(ctx, device_ctx != nullptr, errors::Aborted("No valid device context."));
    cudaStream_t stream = stream_executor::gpu::AsGpuStreamValue(device_ctx->stream());

    var->SparseReadEvict(indices->data(),tmp_indices.data(),tmp_values.data(), output->data(),(uint64_t*)tmp_evict_num.data(), rows, stream);
    size_t evict_num = ((size_t*)tmp_evict_num.data())[0];
    Tensor* output_evict_keys = nullptr;
    OP_REQUIRES_OK(ctx, ctx->allocate_output(1, {evict_num}, &output_evict_keys));

    Tensor* output_evict_value = nullptr;
    OP_REQUIRES_OK(ctx, ctx->allocate_output(2, {evict_num, cols}, &output_evict_value));
    if (evict_num > 0){
    var->CopyEvictKeys(tmp_indices.data(),tmp_values.data(),evict_num,cols,output_evict_keys->data(),output_evict_value->data(),stream);
    }

  }
};

#define REGISTER_GPU_KERNELS(key_type_tf, key_type, dtype_tf, dtype)   \
  REGISTER_KERNEL_BUILDER(Name("DummyVarSparseReadEvict")                   \
                              .Device(DEVICE_GPU)                      \
                              .HostMemory("resource")                  \
                              .TypeConstraint<key_type_tf>("key_type") \
                              .TypeConstraint<dtype_tf>("dtype"),      \
                          DummyVarSparseReadEvictOp<key_type, dtype>)
#if TF_VERSION_MAJOR == 1
REGISTER_GPU_KERNELS(int64, int64_t, float, float);
REGISTER_GPU_KERNELS(int32, int32_t, float, float);
// REGISTER_GPU_KERNELS(int64, int64_t, Eigen::half, __half);
// REGISTER_GPU_KERNELS(int32, int32_t, Eigen::half, __half);
#else
REGISTER_GPU_KERNELS(int64_t, int64_t, float, float);
REGISTER_GPU_KERNELS(int32_t, int32_t, float, float);
// REGISTER_GPU_KERNELS(int64_t, int64_t, Eigen::half, __half);
// REGISTER_GPU_KERNELS(int32_t, int32_t, Eigen::half, __half);
#endif
#undef REGISTER_GPU_KERNELS


// -----------------------------------------------------------------------------------------------
// DummyVarScatterAdd
// -----------------------------------------------------------------------------------------------
template <typename KeyType, typename ValueType>
class DummyVarScatterAddOp : public OpKernel {
 public:
  explicit DummyVarScatterAddOp(OpKernelConstruction* ctx) : OpKernel(ctx) {}

  void Compute(OpKernelContext* ctx) override {
    core::RefCountPtr<DummyVar<KeyType, ValueType>> var;
    OP_REQUIRES_OK(ctx, LookupResource(ctx, HandleFromInput(ctx, 0), &var));

    tf_shared_lock ml(*var->mu());

    const Tensor* indices = nullptr;
    OP_REQUIRES_OK(ctx, ctx->input("indices", &indices));
    const Tensor* updates = nullptr;
    OP_REQUIRES_OK(ctx, ctx->input("updates", &updates));

    auto device_ctx = ctx->op_device_context();
    OP_REQUIRES(ctx, device_ctx != nullptr, errors::Aborted("No valid device context."));
    cudaStream_t stream = stream_executor::gpu::AsGpuStreamValue(device_ctx->stream());

    // Do scatter add
    int64_t N = indices->NumElements();
    var->ScatterAdd(indices->data(), updates->data(), N, stream);
  }
};

#define REGISTER_GPU_KERNELS(key_type_tf, key_type, dtype_tf, dtype)   \
  REGISTER_KERNEL_BUILDER(Name("DummyVarScatterAdd")                   \
                              .Device(DEVICE_GPU)                      \
                              .HostMemory("resource")                  \
                              .TypeConstraint<key_type_tf>("key_type") \
                              .TypeConstraint<dtype_tf>("dtype"),      \
                          DummyVarScatterAddOp<key_type, dtype>)
#if TF_VERSION_MAJOR == 1
REGISTER_GPU_KERNELS(int64, int64_t, float, float);
REGISTER_GPU_KERNELS(int32, int32_t, float, float);
#else
REGISTER_GPU_KERNELS(int64_t, int64_t, float, float);
REGISTER_GPU_KERNELS(int32_t, int32_t, float, float);
#endif
#undef REGISTER_GPU_KERNELS

// -----------------------------------------------------------------------------------------------
// DummyVarScatterUpdate
// -----------------------------------------------------------------------------------------------
template <typename KeyType, typename ValueType>
class DummyVarScatterUpdateOp : public OpKernel {
 public:
  explicit DummyVarScatterUpdateOp(OpKernelConstruction* ctx) : OpKernel(ctx) {}

  void Compute(OpKernelContext* ctx) override {
    core::RefCountPtr<DummyVar<KeyType, ValueType>> var;
    OP_REQUIRES_OK(ctx, LookupResource(ctx, HandleFromInput(ctx, 0), &var));

    tf_shared_lock ml(*var->mu());

    const Tensor* indices = nullptr;
    OP_REQUIRES_OK(ctx, ctx->input("indices", &indices));
    const Tensor* updates = nullptr;
    OP_REQUIRES_OK(ctx, ctx->input("updates", &updates));

    auto device_ctx = ctx->op_device_context();
    OP_REQUIRES(ctx, device_ctx != nullptr, errors::Aborted("No valid device context."));
    cudaStream_t stream = stream_executor::gpu::AsGpuStreamValue(device_ctx->stream());

    // Do scatter add
    int64_t N = indices->NumElements();
    var->ScatterUpdate(indices->data(), updates->data(), N, stream);
  }
};

#define REGISTER_GPU_KERNELS(key_type_tf, key_type, dtype_tf, dtype)   \
  REGISTER_KERNEL_BUILDER(Name("DummyVarScatterUpdate")                \
                              .Device(DEVICE_GPU)                      \
                              .HostMemory("resource")                  \
                              .TypeConstraint<key_type_tf>("key_type") \
                              .TypeConstraint<dtype_tf>("dtype"),      \
                          DummyVarScatterUpdateOp<key_type, dtype>)
#if TF_VERSION_MAJOR == 1
REGISTER_GPU_KERNELS(int64, int64_t, float, float);
REGISTER_GPU_KERNELS(int32, int32_t, float, float);
#else
REGISTER_GPU_KERNELS(int64_t, int64_t, float, float);
REGISTER_GPU_KERNELS(int32_t, int32_t, float, float);
#endif
#undef REGISTER_GPU_KERNELS

}  // namespace tensorflow
