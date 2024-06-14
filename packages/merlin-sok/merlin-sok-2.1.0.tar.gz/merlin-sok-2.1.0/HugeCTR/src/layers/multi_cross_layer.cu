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

#include <cublas_v2.h>
#include <linalg/gemv.h>

#include <cuda/std/array>
#include <layers/multi_cross_layer.hpp>
#include <linalg/binary_op.cuh>
#include <linalg/matrix_vector_op.cuh>
#include <linalg/reduce.cuh>
#include <prims/cuda_utils.cuh>
#include <prims/linalg/matrix_multiplication.cuh>
#include <utils.cuh>
#include <utils.hpp>
#include <vector>

/** Overload of built-in atomicAdd for support on Pascal architectures */
#if defined(__CUDA_ARCH__) && __CUDA_ARCH__ >= 600 && __CUDA_ARCH__ < 700

__inline__ __device__ __half atomicAdd(__half* address, __half val) {
  size_t base_offset = ((size_t)address & 2);
  uint32_t* base_address = (uint32_t*)((char*)(address)-base_offset);

  uint32_t old = *base_address, assumed;
  do {
    assumed = old;
    {
      __half assumed_f16 = __ushort_as_half((uint16_t)(assumed >> (base_offset << 3)));
      uint32_t new_val = assumed;
      ((uint16_t*)(&new_val))[base_offset >> 1] = __half_as_ushort(__hadd(assumed_f16, val));
      old = atomicCAS(base_address, assumed, new_val);
    }
  } while (assumed != old);
  return __ushort_as_half((uint16_t)(old >> (base_offset << 3)));
}

#endif  // defined(__CUDA_ARCH__) && __CUDA_ARCH__ >= 600 && __CUDA_ARCH__ < 700

namespace HugeCTR {
struct alignas(8) half2x4 : public cuda::std::array<__half2, 4> {};
// kernels
namespace {

inline int calc_grid(int t, int b) { return (t - 1) / b + 1; }

template <typename T>
__global__ void vector_fma4(T* pout, const T* pvec_a, const T* pvec_b, const T* pvec_c,
                            const int len) {
  const int gtid = blockDim.x * blockIdx.x + threadIdx.x;
  if (gtid < len) pout[gtid] = pvec_a[gtid] * pvec_b[gtid] + pvec_c[gtid];
}
template <typename T>
__global__ void vector_fma4_align8(T* pout, const T* pvec_a, const T* pvec_b, const T* pvec_c,
                                   const int len) {
  const int gtid = (blockDim.x * blockIdx.x + threadIdx.x) << 3;
  if (gtid >= len) {
    return;
  }
#pragma unroll
  for (int i = 0; i < 8; i++) {
    pout[gtid + i] = pvec_a[gtid + i] * pvec_b[gtid + i] + pvec_c[gtid + i];
  }
}

template <typename T>
__global__ void vector_fma3_align8(T* __restrict__ pout, const T* __restrict__ pvec_a,
                                   const T* __restrict__ pvec_b, const int len) {
  const int gtid = blockDim.x * blockIdx.x + threadIdx.x;
  if (gtid < len) pout[gtid] += pvec_a[gtid] * pvec_b[gtid];
}
// out0 = a * b
// out1 += a * c
template <typename T, int VecLen = 1, int SHT = 0>
__global__ void vector_mul_fma3_align(T* __restrict__ pout0, T* __restrict__ pout1,
                                      const T* __restrict__ pvec_a, const T* __restrict__ pvec_b,
                                      const T* __restrict__ pvec_c, const int len) {
  const int gtid = (blockDim.x * blockIdx.x + threadIdx.x) << SHT;
  if (gtid >= len) {
    return;
  }
  const T* pA = pvec_a + gtid;
  const T* pB = pvec_b + gtid;
  const T* pC = pvec_c + gtid;
  T* out1 = pout1 + gtid;
  T* out0 = pout0 + gtid;
  T regA[VecLen], regB[VecLen], regC[VecLen];
  T mul[VecLen];
  T acc[VecLen];

// load
#pragma unroll
  for (int i = 0; i < VecLen; i++) {
    regA[i] = pA[i];
    regB[i] = pB[i];
    regC[i] = pC[i];
    acc[i] = out1[i];
  }
// mul & fma
#pragma unroll
  for (int i = 0; i < VecLen; i++) {
    mul[i] = regA[i] * regB[i];
    acc[i] += regA[i] * regC[i];
  }
// store
#pragma unroll
  for (int i = 0; i < VecLen; i++) {
    out0[i] = mul[i];
    out1[i] = acc[i];
  }
}
// out0 = a * b
// out1 += a * c
template <>
__global__ void vector_mul_fma3_align<__half, 8, 3>(
    __half* __restrict__ pout0, __half* __restrict__ pout1, const __half* __restrict__ pvec_a,
    const __half* __restrict__ pvec_b, const __half* __restrict__ pvec_c, const int len) {
  const int start = (blockDim.x * blockIdx.x + threadIdx.x) << 3;
  if (start >= len) {
    return;
  }
  float4 a_8, b_8, c_8, acc_8;
  half2x4 out0, out1;
  half2x4 *out0_ptr, *out1_ptr;
  for (int gtid = start; gtid < len; gtid += blockDim.x * gridDim.x * 8) {
    out0_ptr = reinterpret_cast<half2x4*>(pout0 + gtid);
    out1_ptr = reinterpret_cast<half2x4*>(pout1 + gtid);
    // load
    a_8 = *reinterpret_cast<const float4*>(pvec_a + gtid);
    b_8 = *reinterpret_cast<const float4*>(pvec_b + gtid);
    c_8 = *reinterpret_cast<const float4*>(pvec_c + gtid);
    acc_8 = *reinterpret_cast<const float4*>(pout1 + gtid);
    // mul
    out0[0] = __hmul2(*reinterpret_cast<half2*>(&a_8.x), *reinterpret_cast<half2*>(&b_8.x));
    out0[1] = __hmul2(*reinterpret_cast<half2*>(&a_8.y), *reinterpret_cast<half2*>(&b_8.y));
    out0[2] = __hmul2(*reinterpret_cast<half2*>(&a_8.z), *reinterpret_cast<half2*>(&b_8.z));
    out0[3] = __hmul2(*reinterpret_cast<half2*>(&a_8.w), *reinterpret_cast<half2*>(&b_8.w));
    *out0_ptr = out0;
    // add
    out1[0] = __hfma2(*reinterpret_cast<half2*>(&a_8.x), *reinterpret_cast<half2*>(&c_8.x),
                      *reinterpret_cast<half2*>(&acc_8.x));
    out1[1] = __hfma2(*reinterpret_cast<half2*>(&a_8.y), *reinterpret_cast<half2*>(&c_8.y),
                      *reinterpret_cast<half2*>(&acc_8.y));
    out1[2] = __hfma2(*reinterpret_cast<half2*>(&a_8.z), *reinterpret_cast<half2*>(&c_8.z),
                      *reinterpret_cast<half2*>(&acc_8.z));
    out1[3] = __hfma2(*reinterpret_cast<half2*>(&a_8.w), *reinterpret_cast<half2*>(&c_8.w),
                      *reinterpret_cast<half2*>(&acc_8.w));
    // store
    *out1_ptr = out1;
  }
}
// d = a * b + c
template <>
__global__ void vector_fma4_align8(__half* pout, const __half* pvec_a, const __half* pvec_b,
                                   const __half* pvec_c, const int len) {
  const int gtid = (blockDim.x * blockIdx.x + threadIdx.x) << 3;
  if (gtid >= len) {
    return;
  }
  float4 a_8, b_8, c_8;
  half2x4 d_8;
  half2x4* out_ptr;
  out_ptr = reinterpret_cast<half2x4*>(pout + gtid);
  // load
  a_8 = *reinterpret_cast<const float4*>(pvec_a + gtid);
  b_8 = *reinterpret_cast<const float4*>(pvec_b + gtid);
  c_8 = *reinterpret_cast<const float4*>(pvec_c + gtid);
  // fma
  d_8[0] = __hfma2(*reinterpret_cast<half2*>(&a_8.x), *reinterpret_cast<half2*>(&b_8.x),
                   *reinterpret_cast<half2*>(&c_8.x));
  d_8[1] = __hfma2(*reinterpret_cast<half2*>(&a_8.y), *reinterpret_cast<half2*>(&b_8.y),
                   *reinterpret_cast<half2*>(&c_8.y));
  d_8[2] = __hfma2(*reinterpret_cast<half2*>(&a_8.z), *reinterpret_cast<half2*>(&b_8.z),
                   *reinterpret_cast<half2*>(&c_8.z));
  d_8[3] = __hfma2(*reinterpret_cast<half2*>(&a_8.w), *reinterpret_cast<half2*>(&b_8.w),
                   *reinterpret_cast<half2*>(&c_8.w));
  // store
  *out_ptr = d_8;
}
// c = a * b + c
template <>
__global__ void vector_fma3_align8(__half* __restrict__ pout, const __half* __restrict__ pvec_a,
                                   const __half* __restrict__ pvec_b, const int len) {
  const int gtid = (blockDim.x * blockIdx.x + threadIdx.x) << 3;
  if (gtid >= len) {
    return;
  }
  float4 a_8, b_8, c_8;
  half2x4 d_8;
  half2x4* out_ptr;
  out_ptr = reinterpret_cast<half2x4*>(pout + gtid);
  // load
  a_8 = *reinterpret_cast<const float4*>(pvec_a + gtid);
  b_8 = *reinterpret_cast<const float4*>(pvec_b + gtid);
  c_8 = *reinterpret_cast<const float4*>(pout + gtid);
  // fma
  d_8[0] = __hfma2(*reinterpret_cast<half2*>(&a_8.x), *reinterpret_cast<half2*>(&b_8.x),
                   *reinterpret_cast<half2*>(&c_8.x));
  d_8[1] = __hfma2(*reinterpret_cast<half2*>(&a_8.y), *reinterpret_cast<half2*>(&b_8.y),
                   *reinterpret_cast<half2*>(&c_8.y));
  d_8[2] = __hfma2(*reinterpret_cast<half2*>(&a_8.z), *reinterpret_cast<half2*>(&b_8.z),
                   *reinterpret_cast<half2*>(&c_8.z));
  d_8[3] = __hfma2(*reinterpret_cast<half2*>(&a_8.w), *reinterpret_cast<half2*>(&b_8.w),
                   *reinterpret_cast<half2*>(&c_8.w));
  // store
  *out_ptr = d_8;
}
/**
 * compute dot product for each pair of the rows in the two matrix,
 */
template <typename T>
__global__ void matrix_pair_mul_kernel(T* o_vec, const T* mat_a, int h, int w, const T* mat_b) {
  const int tid = blockDim.x * blockIdx.x + threadIdx.x;
  const int wtid = tid % WARP_SIZE;  // thread id in warp
  const int wid = tid / WARP_SIZE;   // warp id
  const T* mat_a_with_offset = mat_a + wid * w;
  const T* mat_b_with_offset = mat_b + wid * w;
  if (wid < h) {
    T accum = 0.f;
    for (int i = wtid; i < w; i += WARP_SIZE) {
      accum += mat_a_with_offset[i] * mat_b_with_offset[i];
    }
    T val = warpReduceSum(accum);
    if (wtid == 0) {
      o_vec[wid] = val;
    }
  }
}

template <typename T>
__global__ void mm_1d(T* out_mat, const T* vec_a, int h, const T* vec_b, int w) {
  const int tid = blockDim.x * blockIdx.x + threadIdx.x;
  if (tid < h * w) {
    const int col = tid % w;
    const int row = tid / w;
    out_mat[tid] = vec_a[row] * vec_b[col];
  }
}

/**
 * Each row in `mat` scale with the corresponding element in vec. and accum across rows
 * The length of vec should be h.
 * @param o_mat: hxw
 * @param mat: hxw
 * @param vec: hx1
 */
template <typename T>
__global__ void row_scaling_sum_kernel(T* out, const T* mat, int h, int w, const T* vec) {
  const int tid = blockDim.x * blockIdx.x + threadIdx.x;
  const int wtid = tid % WARP_SIZE;  // thread id in warp
  const int wid = tid / WARP_SIZE;   // warp id
  if (wid < w) {
    T accum = 0.f;
    for (int i = wtid; i < h; i += WARP_SIZE) {
      const int col = wid;
      const int idx = i * w + col;
      accum += mat[idx] * vec[i];
    }
    T val = warpReduceSum(accum);
    if (wtid == 0) {
      out[wid] += val;  // using += here to enable regularization
    }
  }
}

template <typename T>
void matrix_vec_mul(core23::Tensor& out, const core23::Tensor& mat, const core23::Tensor& vec,
                    cublasHandle_t cublas_handle, cudaStream_t stream);

template <>
void matrix_vec_mul<float>(core23::Tensor& out, const core23::Tensor& mat,
                           const core23::Tensor& vec, cublasHandle_t cublas_handle,
                           cudaStream_t stream) {
  float* pout = out.data<float>();
  const float* pmat = mat.data<float>();
  const float* pvec = vec.data<float>();

  const auto& dim = out.shape();
  const auto& idim = mat.shape();
  assert(dim.dims() == 2 && idim.dims() == 2 && idim.size(1) == vec.shape().size(1) &&
         vec.shape().size(0) == 1);
  assert(idim.size(0) == dim.size(0));

  const int h = idim.size(0);
  const int w = idim.size(1);
  const float alpha = 1.0f;
  const float beta = 0.0f;

  CUBLAS_CHECK(cublasSetStream(cublas_handle, stream));
  CUBLAS_CHECK(cublasSgemm(cublas_handle, CUBLAS_OP_T, CUBLAS_OP_N, h, 1, w, &alpha, pmat, w, pvec,
                           w, &beta, pout, h));
}

template <>
void matrix_vec_mul<__half>(core23::Tensor& out, const core23::Tensor& mat,
                            const core23::Tensor& vec, cublasHandle_t cublas_handle,
                            cudaStream_t stream) {
  __half* pout = out.data<__half>();
  const __half* pmat = mat.data<__half>();
  const __half* pvec = vec.data<__half>();

  const auto& dim = out.shape();
  const auto& idim = mat.shape();
  assert(dim.dims() == 2 && idim.dims() == 2 && idim.size(1) == vec.shape().size(1) &&
         vec.shape().size(0) == 1);
  assert(idim.size(0) == dim.size(0));

  const int h = idim.size(0);
  const int w = idim.size(1);
  const __half alpha = 1.0f;
  const __half beta = 0.0f;

  CUBLAS_CHECK(cublasSetStream(cublas_handle, stream));
  CUBLAS_CHECK(cublasHgemm(cublas_handle, CUBLAS_OP_T, CUBLAS_OP_N, h, 1, w, &alpha, pmat, w, pvec,
                           w, &beta, pout, h));
}

template <typename T>
void row_scaling(core23::Tensor& o_mat, const core23::Tensor& mat, const core23::Tensor& vec,
                 cudaStream_t stream) {
  T* pout = o_mat.data<T>();
  const T* pmat = mat.data<T>();
  const T* pvec = vec.data<T>();

  const auto& dim = o_mat.shape();
  const auto& idim = mat.shape();
  assert(dim.dims() == 2 && idim.dims() == 2 && dim.size(0) == vec.shape().size(0) &&
         vec.shape().size(1) == 1);
  assert(idim.size(0) == dim.size(0) && idim.size(1) == dim.size(1));

  const int h = dim.size(0);
  const int w = dim.size(1);

  MLCommon::LinAlg::matrixVectorOp(
      pout, pmat, pvec, h, w, false, true, [] __device__(T a, T b) { return a * b; }, stream);
}

template <typename T>
void matrix_vec_add(core23::Tensor& o_mat, const core23::Tensor& mat, const core23::Tensor& vec,
                    cudaStream_t stream) {
  T* pout = o_mat.data<T>();
  const T* pmat = mat.data<T>();
  const T* pvec = vec.data<T>();

  const auto& dim = o_mat.shape();
  const auto& idim = mat.shape();
  assert(dim.dims() == 2 && idim.dims() == 2 && dim.size(1) == vec.shape().size(1) &&
         vec.shape().size(0) == 1);
  assert(idim.size(0) == dim.size(0) && idim.size(1) == dim.size(1));

  const int h = dim.size(0);
  const int w = dim.size(1);

  MLCommon::LinAlg::matrixVectorOp(
      pout, pmat, pvec, h, w, false, false, [] __device__(T a, T b) { return a + b; }, stream);
}

template <typename T>
void matrix_add(core23::Tensor& out_mat, const core23::Tensor& mat_a, const core23::Tensor& mat_b,
                cudaStream_t stream) {
  T* pout = out_mat.data<T>();
  const T* pmat_a = mat_a.data<T>();
  const T* pmat_b = mat_b.data<T>();

  const auto& dim = out_mat.shape();
  const auto& idim1 = mat_a.shape();
  const auto& idim2 = mat_b.shape();
  assert(idim1.size(0) == dim.size(0) && idim1.size(1) == dim.size(1));
  assert(idim2.size(0) == dim.size(0) && idim2.size(1) == dim.size(1));

  const int h = dim.size(0);
  const int w = dim.size(1);

  MLCommon::LinAlg::binaryOp(
      pout, pmat_a, pmat_b, h * w, [] __device__(T a, T b) { return a + b; }, stream);
}

template <typename T>
void fused_mul_fma3(core23::Tensor& Y0, core23::Tensor& Y1, const core23::Tensor& A,
                    const core23::Tensor& B, const core23::Tensor& C, cudaStream_t stream) {
  const T* pmat_a = A.data<T>();
  const T* pmat_b = B.data<T>();
  const T* pmat_c = C.data<T>();
  T* pmat_o0 = Y0.data<T>();
  T* pmat_o1 = Y1.data<T>();
  const auto& idima = A.shape();
  const auto& idimb = B.shape();
  const auto& idimc = C.shape();
  const auto& idimc0 = Y0.shape();
  const auto& idimc1 = Y1.shape();

  assert(idima.size(0) == idimb.size(0) && idima.size(1) == idimb.size(1) &&
         idimc.size(0) == idimb.size(0) && idimc0.size(1) == idimb.size(1) &&
         idimc.size(0) == idima.size(0) && idimc.size(1) == idima.size(1));
  assert(idimc1.size(0) == idimc.size(0) && idimc1.size(1) == idimc0.size(1));
  const int h = idima.size(0);
  const int w = idima.size(1);
  const int len = h * w;
  constexpr int warp_per_sm = 8;
  constexpr int warp_size = 32;
  const int BLOCK_DIM = warp_size * warp_per_sm;  // 8 warps per block
  int GRID_DIM = (len + BLOCK_DIM - 1) / BLOCK_DIM;
  if (len % 8 == 0 && std::is_same<T, __half>::value) {
    GRID_DIM = (len / 8 + BLOCK_DIM - 1) / BLOCK_DIM;
    vector_mul_fma3_align<T, 8, 3>
        <<<GRID_DIM, BLOCK_DIM, 0, stream>>>(pmat_o0, pmat_o1, pmat_a, pmat_b, pmat_c, len);
  } else {
    vector_mul_fma3_align<T>
        <<<GRID_DIM, BLOCK_DIM, 0, stream>>>(pmat_o0, pmat_o1, pmat_a, pmat_b, pmat_c, len);
  }
}
// perform out_mat = mat_a * mat_b + mat_c
template <typename T>
void fused_matrix_elementwise_dot_add(core23::Tensor& out_mat, const core23::Tensor& mat_a,
                                      const core23::Tensor& mat_b, const core23::Tensor& mat_c,
                                      cudaStream_t stream) {
  T* pout = out_mat.data<T>();
  const T* pmat_a = mat_a.data<T>();
  const T* pmat_b = mat_b.data<T>();
  const T* pmat_c = mat_c.data<T>();
  const auto& dim = out_mat.shape();
  const auto& idima = mat_a.shape();
  const auto& idimb = mat_b.shape();
  const auto& idimc = mat_c.shape();
  assert(idima.size(0) == dim.size(0) && idima.size(1) == dim.size(1) &&
         idimc.size(0) == dim.size(0));
  assert(idimb.size(0) == dim.size(0) && idimb.size(1) == dim.size(1) &&
         idimc.size(1) == dim.size(1));

  const int h = dim.size(0);
  const int w = dim.size(1);

  constexpr int sm_count = 108;
  constexpr int warp_per_sm = 8;
  constexpr int warp_size = 32;
  constexpr int kNumWaves = 32;
  const int BLOCK_DIM = warp_size * warp_per_sm;  // 8 warps per block
  const int GRID_DIM = (h * w + BLOCK_DIM - 1) / BLOCK_DIM;
  if (h * w % 8 == 0 && std::is_same<T, __half>::value) {
    int num_items = h * w / 8;
    const int GRID_DIM_h4 = (num_items + BLOCK_DIM - 1) / BLOCK_DIM;
    if (pout == pmat_c) {
      vector_fma3_align8<<<GRID_DIM_h4, BLOCK_DIM, 0, stream>>>(pout, pmat_a, pmat_b, h * w);
    } else {
      vector_fma4_align8<<<GRID_DIM_h4, BLOCK_DIM, 0, stream>>>(pout, pmat_a, pmat_b, pmat_c,
                                                                h * w);
    }
  } else {
    vector_fma4<<<GRID_DIM, BLOCK_DIM, 0, stream>>>(pout, pmat_a, pmat_b, pmat_c, h * w);
  }
}
// c = a * b => 3
template <typename T>
void matrix_elementwise_dot(core23::Tensor& out_mat, const core23::Tensor& mat_a,
                            const core23::Tensor& mat_b, cudaStream_t stream) {
  T* pout = out_mat.data<T>();
  const T* pmat_a = mat_a.data<T>();
  const T* pmat_b = mat_b.data<T>();

  const auto& dim = out_mat.shape();
  const auto& idim1 = mat_a.shape();
  const auto& idim2 = mat_b.shape();
  assert(idim1[0] == dim.size(0) && idim1[1] == dim.size(1));
  assert(idim2[0] == dim.size(0) && idim2[1] == dim.size(1));

  const int h = dim.size(0);
  const int w = dim.size(1);

  MLCommon::LinAlg::binaryOp(
      pout, pmat_a, pmat_b, h * w, [] __device__(T a, T b) { return a * b; }, stream);
}

template <typename T>
void matrix_pair_mul(core23::Tensor& o_vec, const core23::Tensor& mat_a,
                     const core23::Tensor& mat_b, cudaStream_t stream) {
  T* pout = o_vec.data<T>();
  const T* pmat_a = mat_a.data<T>();
  const T* pmat_b = mat_b.data<T>();

  const auto& dim = mat_a.shape();

  const int h = dim.size(0);
  const int w = dim.size(1);
  assert(h == mat_b.shape().size(0) && w == mat_a.shape().size(1) && h == o_vec.shape().size(0) &&
         1 == o_vec.shape().size(1));

  const int BLOCK_DIM = 256;
  const int GRID_DIM = calc_grid(h * WARP_SIZE, BLOCK_DIM);
  matrix_pair_mul_kernel<<<GRID_DIM, BLOCK_DIM, 0, stream>>>(pout, pmat_a, h, w, pmat_b);
}

template <typename T>
void out_product(core23::Tensor& out_mat, const core23::Tensor& vec_a, const core23::Tensor& vec_b,
                 cudaStream_t stream) {
  T* pout = out_mat.data<T>();
  const T* pvec_a = vec_a.data<T>();
  const T* pvec_b = vec_b.data<T>();
  const auto& dim = out_mat.shape();

  const int h = dim.size(0);
  const int w = dim.size(1);

  assert(h == vec_a.shape().size(0) && w == vec_b.shape().size(1) && vec_a.shape().size(1) == 1 &&
         vec_b.shape().size(0) == 1);

  const int BLOCK_DIM = 256;
  const int GRID_DIM = calc_grid(h * w, BLOCK_DIM);
  mm_1d<<<GRID_DIM, BLOCK_DIM, 0, stream>>>(pout, pvec_a, h, pvec_b, w);
}

template <typename T>
void row_scaling_sum(core23::Tensor& out, const core23::Tensor& mat, const core23::Tensor& vec,
                     cudaStream_t stream) {
  T* pout = out.data<T>();
  const T* pmat = mat.data<T>();
  const T* pvec = vec.data<T>();

  const auto& dim = out.shape();
  const auto& idim = mat.shape();
  assert(dim.dims() == 2 && idim.dims() == 2 && idim.size(0) == vec.shape().size(0) &&
         vec.shape().size(1) == 1);
  assert(idim.size(1) == dim.size(1));

  const int h = idim.size(0);
  const int w = idim.size(1);

  const int BLOCK_DIM = 256;
  const int GRID_DIM = calc_grid(w * WARP_SIZE, BLOCK_DIM);  // each col one warp

  row_scaling_sum_kernel<<<GRID_DIM, BLOCK_DIM, 0, stream>>>(pout, pmat, h, w, pvec);
}

template <typename T>
void rows_sum(core23::Tensor& out, const core23::Tensor& mat, cudaStream_t stream) {
  T* pout = out.data<T>();
  const T* pmat = mat.data<T>();

  const auto& dim = out.shape();
  const auto& idim = mat.shape();
  assert(dim.dims() == 2 && idim.dims() == 2);
  assert(idim.size(1) == dim.size(1));

  const int h = idim.size(0);
  const int w = idim.size(1);

  MLCommon::LinAlg::reduce(pout, pmat, h, w, (T)0, false, true, stream, false,
                           [] __device__(T in, int i) { return in; });
}

}  // namespace

/*
 * Equivalent TensorFlow Code:
 *
def forward(x, k, b, layers):
  y = []
  h = []
  for i in range(layers):
    v = tf.linalg.matvec(x if i == 0 else y[i - 1], k[i])
    v = tf.transpose(v)
    h.append(v)
    m = tf.multiply(x, v)
    m = tf.add(m, x if i == 0 else y[i - 1])
    m = tf.add(m, b[i])
    y.append(m)
  return y, h
 *
 */
template <typename T>
void MultiCrossForwardFunctor<T>::operator()(cudaStream_t stream, cublasHandle_t cublas_handle,
                                             const core23::Tensor& input_tensor,
                                             const std::vector<core23::Tensor>& kernel_tensors,
                                             const std::vector<core23::Tensor>& bias_tensors,
                                             std::vector<core23::Tensor>& layer_output_tensors,
                                             std::vector<core23::Tensor>& layer_hidden_tensors,
                                             int num_layers) const {
  for (int i = 0; i < num_layers; i++) {
    // weight: kernel_tensors[i] is a row vector
    // layer_hidden_tensors[i] is a row vector
    matrix_vec_mul<T>(layer_hidden_tensors[i], i == 0 ? input_tensor : layer_output_tensors[i - 1],
                      kernel_tensors[i], cublas_handle, stream);
    row_scaling<T>(layer_output_tensors[i], input_tensor, layer_hidden_tensors[i], stream);
    matrix_add<T>(layer_output_tensors[i], layer_output_tensors[i],
                  i == 0 ? input_tensor : layer_output_tensors[i - 1], stream);
    matrix_vec_add<T>(layer_output_tensors[i], layer_output_tensors[i], bias_tensors[i], stream);
  }
}

//
/*
  output is x_{l+1} =  x_0 \. (w * x_l + b) + x_l , where
  input is
    input_tensor : x_0
    kernel_tensors : w
    bias_tensors   : n
    layer_output_tensors : x_l


  output is
    layer_output_tensors : x_l

  intermediate tensor:
    layer_hidden_tensors : w * x_l

h_i = gemv(x_i,w_i) ,
o_i = row_scaling(h_i,x),
o_i = matrix_vec_add(o_i,bias)
o_i = matrix_add(o_i,o_{i-1})

*
*/
template <typename T>

void MultiCrossForwardFunctorv2<T>::operator()(
    cudaStream_t stream, const core23::Tensor& input_tensor,
    const std::vector<core23::Tensor>& kernel_tensors,
    const std::vector<core23::Tensor>& bias_tensors, std::vector<core23::Tensor>& XU_tensors,
    std::vector<core23::Tensor>& layer_output_tensors,
    std::vector<core23::Tensor>& layer_hidden_tensors, int num_layers,
    const std::vector<CublasDesc<T>>& xu_descr_, const std::vector<CublasDesc<T>>& xuvb_descr_,
    const std::vector<CublasAlgo<T>>& xu_fprop_algo_,
    const std::vector<CublasAlgo<T>>& xuvb_fprop_algo_, cublasLtHandle_t cublaslt_handle) {
  auto batchsize = input_tensor.shape().size(0);
  auto projection_dim = kernel_tensors[0].shape().size(1);
  auto vec_length = input_tensor.shape().size(1);
  auto U_row = kernel_tensors[0].shape().size(0);
  auto V_col = kernel_tensors[1].shape().size(1);
  float alpha = 1.0f;
  float beta = 0.0f;
  if (vec_length != U_row || vec_length != V_col) {
    HCTR_LOG(INFO, WORLD, "vec_length %ld U_row %ld V_col %ld\n", vec_length, U_row, V_col);
    HCTR_OWN_THROW(Error_t::WrongInput, "input or output tensor dimensions not matches");
  }
  for (int i = 0; i < num_layers; i++) {
    const auto& tensor_input = i == 0 ? input_tensor : layer_output_tensors[i - 1];
    // gemm with functor
    // x_i * u
    {
      const T* mat_a = tensor_input.data<T>();
      const T* mat_b = kernel_tensors[2 * i].data<T>();
      T* mat_c = XU_tensors[i].data<T>();
      this->gemm_functor_(alpha, mat_a, mat_b, beta, mat_c, mat_c, xu_descr_[i], xu_fprop_algo_[i],
                          cublaslt_handle, stream);
    }

    // gemm + bias with functor
    // x_i * u * v + b
    {
      const T* mat_a = XU_tensors[i].data<T>();
      const T* mat_b = kernel_tensors[2 * i + 1].data<T>();
      T* mat_c = layer_hidden_tensors[i].data<T>();
      this->gemm_functor_(alpha, mat_a, mat_b, beta, mat_c, mat_c, xuvb_descr_[i],
                          xuvb_fprop_algo_[i], cublaslt_handle, stream);
    }
    // x_0 .* (x_i * u * v + b) + x_i
    fused_matrix_elementwise_dot_add<T>(
        layer_output_tensors[i], layer_hidden_tensors[i], input_tensor,
        i == 0 ? input_tensor : layer_output_tensors[i - 1], stream);
  }
}

/*
 * Equivalent TensorFlow Code:
 *
def backward(x, k, y, h, dy, layers):
  dx = tf.zeros(x.shape)
  dk = []
  db = []
  for i in reversed(range(layers)):
    dx = tf.add(dx, tf.multiply(dy, h[i]))
    dv = tf.expand_dims(tf.reduce_sum(tf.multiply(dy, x), 1), 1)
    dk.insert(0, tf.linalg.matvec(x if i == 0 else y[i - 1], tf.transpose(dv), transpose_a=True))
    db.insert(0, tf.expand_dims(tf.reduce_sum(dy, 0), 0))
    dy = tf.add(dy, tf.matmul(dv, k[i]))
  dx = tf.add(dx, dy)
  return dx, dk, db
grad_tensor : dy
one multi-cross contains multiple cell:

tmp_mat_tensors[0] : dy * h[i]
tmp_mat_tensors[1] : tmp data gradient to current multicross cell
tmp_mat_tensors[2]: sum(dy/dh * h[i])
 *
 */
template <typename T>
void MultiCrossBackwardFunctor<T>::operator()(
    cudaStream_t stream, const core23::Tensor& input_tensor,
    const std::vector<core23::Tensor>& kernel_tensors,
    const std::vector<core23::Tensor>& layer_output_tensors,
    const std::vector<core23::Tensor>& layer_hidden_tensors, const core23::Tensor& grad_tensor,
    core23::Tensor& output_tensor, std::vector<core23::Tensor>& kernel_output_tensors,
    std::vector<core23::Tensor>& bias_output_tensors, core23::Tensor& tmp_vec_tensor,
    core23::Tensor tmp_mat_tensors[], int num_layers) const {
  cudaMemsetAsync(tmp_mat_tensors[2].data(), 0, tmp_mat_tensors[2].num_bytes(), stream);
  for (int i = num_layers - 1; i >= 0; i--) {
    // tmp_mat_tensors[0] = dy * h_i (h_i = gemv(x_i , w_i))
    row_scaling<T>(tmp_mat_tensors[0], i == num_layers - 1 ? grad_tensor : tmp_mat_tensors[1],
                   layer_hidden_tensors[i], stream);
    // dx
    matrix_add<T>(tmp_mat_tensors[2], tmp_mat_tensors[2], tmp_mat_tensors[0], stream);
    // tmp_vec_tensor : {batchsize , 1}
    matrix_pair_mul<T>(tmp_vec_tensor, i == num_layers - 1 ? grad_tensor : tmp_mat_tensors[1],
                       input_tensor, stream);

    // gemv(layer_output_tensors^T, tmp_vec_tensor)
    // gradient WRT weight
    row_scaling_sum<T>(kernel_output_tensors[i],
                       i == 0 ? input_tensor : layer_output_tensors[i - 1], tmp_vec_tensor, stream);
    // dbias
    rows_sum<T>(bias_output_tensors[i], i == num_layers - 1 ? grad_tensor : tmp_mat_tensors[1],
                stream);

    out_product<T>(tmp_mat_tensors[0], tmp_vec_tensor, kernel_tensors[i], stream);
    matrix_add<T>(tmp_mat_tensors[1], i == num_layers - 1 ? grad_tensor : tmp_mat_tensors[1],
                  tmp_mat_tensors[0], stream);
  }
  matrix_add<T>(output_tensor, tmp_mat_tensors[2], tmp_mat_tensors[1], stream);
}

template <typename T>
void MultiCrossBackwardFunctorv2<T>::operator()(
    cudaStream_t dgrad_stream, cudaStream_t wgrad_stream, bool async_wgrad,
    cudaEvent_t& event_overlap, const core23::Tensor& input_tensor,
    const std::vector<core23::Tensor>& kernel_tensors,
    const std::vector<core23::Tensor>& layer_output_tensors,
    const std::vector<core23::Tensor>& layer_hidden_tensors,
    std::vector<core23::Tensor>& kernel_output_tensors, std::vector<core23::Tensor>& grad_tensors,
    std::vector<core23::Tensor>& bias_output_tensors, std::vector<core23::Tensor>& XU_tensors,
    core23::Tensor accum_dx_tensor_, std::vector<core23::Tensor> bprop_bottoms, int num_layers,
    const std::vector<CublasDesc<T>>& xu_descr_, const std::vector<CublasDesc<T>>& xuvb_descr_,
    const std::vector<CublasDesc<T>>& du_descrs_bprop_,
    const std::vector<CublasDesc<T>>& dhidden_descrs_bprop_,
    const std::vector<CublasAlgo<T>>& xu_bprop_algo_,
    const std::vector<CublasAlgo<T>>& xuvb_bprop_algo_,
    const std::vector<CublasAlgo<T>>& du_bprop_algos_,
    const std::vector<CublasAlgo<T>>& dhidden_bprop_algos_, cublasLtHandle_t cublaslt_handle) {
  cudaMemsetAsync(accum_dx_tensor_.data(), 0, accum_dx_tensor_.num_bytes(), dgrad_stream);
  auto batchsize = input_tensor.shape()[0];
  auto projection_dim = kernel_tensors[0].shape()[1];
  auto vec_length = input_tensor.shape()[1];
  auto U_row = kernel_tensors[0].shape()[0];
  auto V_col = kernel_tensors[1].shape()[1];
  bool dgrad_act_shared = grad_tensors[0].data() == input_tensor.data();
  for (int i = num_layers - 1; i >= 0; i--) {
    // S0 = dY_i .* X , shape: (batchsize, w)
    // dX += dY_i .* H , shape: (batchsize, w)
    fused_mul_fma3<T>(bprop_bottoms[2 * i], accum_dx_tensor_, grad_tensors[i + 1], input_tensor,
                      layer_hidden_tensors[i], dgrad_stream);

    {
      if (async_wgrad) {
        HCTR_LIB_THROW(cudaEventRecord(event_overlap, dgrad_stream));
        HCTR_LIB_THROW(cudaStreamWaitEvent(wgrad_stream, event_overlap));
      }
      // 2 dH = S1 = S0 * V^T shape: (batchsize, project_dim)
      const T* mat_a = bprop_bottoms[2 * i].data<T>();
      const T* mat_b = kernel_tensors[2 * i + 1].data<T>();
      T* mat_c = bprop_bottoms[1 + 2 * i].data<T>();
      this->gemm_functor_(1.0f, mat_a, mat_b, 0.0f, mat_c, mat_c, xuvb_descr_[i],
                          xuvb_bprop_algo_[i], cublaslt_handle, dgrad_stream);

      // 1 db, dV = XU_{i}^T * S0 shape: (project_dim, w)
      mat_a = XU_tensors[i].data<T>();
      mat_b = bprop_bottoms[2 * i].data<T>();
      mat_c = kernel_output_tensors[2 * i + 1].data<T>();
      this->gemm_functor_(1.0f, mat_a, mat_b, 1.0f, mat_c, mat_c, xu_descr_[i], xu_bprop_algo_[i],
                          cublaslt_handle, async_wgrad ? wgrad_stream : dgrad_stream);
      if (async_wgrad) {
        HCTR_LIB_THROW(cudaEventRecord(event_overlap, dgrad_stream));
        HCTR_LIB_THROW(cudaStreamWaitEvent(wgrad_stream, event_overlap));
      }
      // 3  dU = X_{i-1} ^T * S1 shape: (w, project_dim)
      mat_a = i == 0 ? input_tensor.data<T>() : layer_output_tensors[i - 1].data<T>();
      mat_b = bprop_bottoms[1 + 2 * i].data<T>();
      mat_c = kernel_output_tensors[2 * i].data<T>();
      this->gemm_functor_(1.0f, mat_a, mat_b, 1.0f, mat_c, mat_c, du_descrs_bprop_[i],
                          du_bprop_algos_[i], cublaslt_handle,
                          async_wgrad ? wgrad_stream : dgrad_stream);
      if (!i && async_wgrad && dgrad_act_shared) {
        HCTR_LIB_THROW(cudaEventRecord(event_overlap, wgrad_stream));
        HCTR_LIB_THROW(cudaStreamWaitEvent(dgrad_stream, event_overlap));
      }

      // 4 dY_{i-1} = S1 * U^T + dY_{i} shape: (batchsize, w)
      mat_a = bprop_bottoms[1 + 2 * i].data<T>();
      mat_b = kernel_tensors[i * 2].data<T>();
      mat_c = grad_tensors[i + 1].data<T>();
      T* mat_d = grad_tensors[i].data<T>();
      // gemm: mat_d = mat_a * mat_b + mat_c
      this->gemm_functor_(1.0f, mat_a, mat_b, 1.0f, mat_c, mat_d, dhidden_descrs_bprop_[i],
                          dhidden_bprop_algos_[i], cublaslt_handle, dgrad_stream);
    }
  }
  matrix_add<T>(grad_tensors[0], accum_dx_tensor_, grad_tensors[0], dgrad_stream);
  if (async_wgrad) {
    HCTR_LIB_THROW(cudaEventRecord(event_overlap, wgrad_stream));
    HCTR_LIB_THROW(cudaStreamWaitEvent(dgrad_stream, event_overlap));
  }
}

template <typename T>
MultiCrossLayer<T>::MultiCrossLayer(const std::vector<core23::Tensor>& in_tensors,
                                    const std::vector<core23::Tensor>& out_tensors,
                                    const std::shared_ptr<GPUResource>& gpu_resource,
                                    int num_layers, int64_t projection_dim,
                                    std::vector<Initializer_t> initializer_types,
                                    bool enable_tf32_compute, bool async_wgrad)
    : TrainableLayer<T>(in_tensors, out_tensors, gpu_resource, initializer_types),
      num_layers_(num_layers),
      projection_dim_(projection_dim),
      enable_tf32_compute_(enable_tf32_compute),
      async_wgrad_(async_wgrad) {
  try {
    // check the in_tensor and out_tensor
    const auto& in_tensor = in_tensors[0];
    const auto& out_tensor = out_tensors[0];

    const auto& in_tensor_dim = in_tensor.shape();
    const auto& out_tensor_dim = out_tensor.shape();
    int64_t vec_length = in_tensor_dim.size(1);
    int64_t batchsize = in_tensor_dim.size(0);
    if (projection_dim_ == 0) {
      HCTR_LOG(WARNING, ROOT, "using multi-cross v1\n");
    }
    CudaDeviceContext context(this->get_device_id());
    wgrad_stream_ = gpu_resource->get_stream("cross_layer_wgrad");
    event_fork_ = gpu_resource->get_event("cross_layer_overlap");
    // 1. two dim?
    if (in_tensor_dim.dims() != 2 || out_tensor_dim.dims() != 2) {
      HCTR_OWN_THROW(Error_t::WrongInput, "input or output tensor doesn't has two dimensions");
    }
    // 2. same dim?
    for (int i = 0; i < 2; i++) {
      if (in_tensor_dim.size(i) != out_tensor_dim.size(i)) {
        HCTR_OWN_THROW(Error_t::WrongInput, "input and output tensor doesn't match");
      }
    }

    // check num_lyaers
    if (num_layers < 1) {
      HCTR_OWN_THROW(Error_t::WrongInput, "num_layers < 1");
    }

    core23::Shape bias_dim = {1, vec_length};
    core23::Shape weight_dim = {vec_length, vec_length};
    core23::Shape U_dim = {vec_length, this->projection_dim_};
    core23::Shape V_dim = {this->projection_dim_, vec_length};
    if (!this->projection_dim_) {
      weight_dim = {1ul, weight_dim.size(1)};
    }
    for (int i = 0; i < num_layers; i++) {
      // setup weights and bias
      {
        // dcnv2
        if (this->projection_dim_) {
          this->set_weight(3 * i, U_dim);
          this->set_weight(3 * i + 1, V_dim);
          this->set_weight(3 * i + 2, bias_dim);
          // dcnv1
        } else {
          this->set_weight(2 * i, weight_dim);
          this->set_weight(2 * i + 1, bias_dim);
        }
      }
      // setup weight gradient
      // dcnv2
      if (this->projection_dim_) {
        this->set_wgrad(3 * i, U_dim);
        this->set_wgrad(3 * i + 1, V_dim);
        this->set_wgrad(3 * i + 2, bias_dim);
        // dcnv1
      } else {
        this->set_wgrad(2 * i, weight_dim);
        this->set_wgrad(2 * i + 1, bias_dim);
      }

      if (this->projection_dim_) {
        xu_descrs_fprop_.emplace_back();
        xuvb_descrs_fprop_.emplace_back();
        xu_descrs_bprop_.emplace_back();
        xuvb_descrs_bprop_.emplace_back();
        du_descrs_bprop_.emplace_back();
        dhidden_descrs_bprop_.emplace_back();

        xu_fprop_algos_.emplace_back();
        xuvb_fprop_algos_.emplace_back();
        xu_bprop_algos_.emplace_back();
        xuvb_bprop_algos_.emplace_back();
        du_bprop_algos_.emplace_back();
        dhidden_bprop_algos_.emplace_back();
      }
    }

    in_tensors_ = in_tensors;
    out_tensors_ = out_tensors;
    // setup blobs

    core23::Shape blob_dim = {batchsize, vec_length};

    core23::BufferParams blobs_buffer_params = {};
    blobs_buffer_params.channel = GetBlobsBufferChannel();
    core23::Device device(core23::DeviceType::GPU, gpu_resource->get_device_id());

    // input
    activation_tensors_.push_back(in_tensor);
    // intermediate output
    for (int i = 0; i < num_layers - 1; i++) {
      core23::Tensor tensor = core23::Tensor(core23::TensorParams()
                                                 .data_type(core23::ToScalarType<T>::value)
                                                 .shape(blob_dim)
                                                 .device(device)
                                                 .buffer_params(blobs_buffer_params));
      activation_tensors_.push_back(tensor);
    }
    // output
    activation_tensors_.push_back(out_tensor);
    accum_dx_tensor_ = core23::Tensor(core23::TensorParams()
                                          .data_type(core23::ToScalarType<T>::value)
                                          .shape(blob_dim)
                                          .device(device)
                                          .buffer_params(blobs_buffer_params));

    for (int i = 0; i < 3; i++) {
      tmp_mat_tensors_[i] = core23::Tensor(core23::TensorParams()
                                               .data_type(core23::ToScalarType<T>::value)
                                               .shape(blob_dim)
                                               .device(device)
                                               .buffer_params(blobs_buffer_params));
    }
    if (projection_dim_) {
      tmp_mat_tensors_[3] = core23::Tensor(core23::TensorParams()
                                               .data_type(core23::ToScalarType<T>::value)
                                               .shape({batchsize, projection_dim_})
                                               .device(device)
                                               .buffer_params(blobs_buffer_params));
    }

    core23::Shape tmp_vec_dim = {batchsize, 1};
    core23::Shape hidden_dim = {batchsize, weight_dim.size(0)};

    tmp_vec_tensor_ = core23::Tensor(core23::TensorParams()
                                         .data_type(core23::ToScalarType<T>::value)
                                         .shape(tmp_vec_dim)
                                         .device(device)
                                         .buffer_params(blobs_buffer_params));
    if (this->projection_dim_) {
      core23::Shape XU_dim = {batchsize, this->projection_dim_};
      for (int i = 0; i < num_layers; i++) {
        core23::Tensor tensor = core23::Tensor(core23::TensorParams()
                                                   .data_type(core23::ToScalarType<T>::value)
                                                   .shape(XU_dim)
                                                   .device(device)
                                                   .buffer_params(blobs_buffer_params));
        XU_tensors_.push_back(tensor);
      }
    }
    for (int i = 0; i < num_layers; i++) {
      core23::Tensor tensor = core23::Tensor(core23::TensorParams()
                                                 .data_type(core23::ToScalarType<T>::value)
                                                 .shape(hidden_dim)
                                                 .device(device)
                                                 .buffer_params(blobs_buffer_params));
      hidden_tensors_.push_back(tensor);
    }
    // bprop buffer
    /*
      bottom[ 2*i ] => dY .* X (elementwise dot)
      bottom[ 2*i+1] => dH
    */
    if (this->projection_dim_) {
      for (int i = 0; i < num_layers; i++) {
        bprop_bottom_.emplace_back(core23::TensorParams()
                                       .data_type(core23::ToScalarType<T>::value)
                                       .shape(blob_dim)
                                       .device(device)
                                       .buffer_params(blobs_buffer_params));
        bprop_bottom_.emplace_back(core23::TensorParams()
                                       .data_type(core23::ToScalarType<T>::value)
                                       .shape({batchsize, projection_dim_})
                                       .device(device)
                                       .buffer_params(blobs_buffer_params));
      }
      // backward output
      if (in_tensors.size() == 2) {
        dgrads_.push_back(in_tensors[1]);
      } else {
        dgrads_.push_back(in_tensors[0]);
      }
      for (int i = 0; i < num_layers - 1; i++) {
        dgrads_.push_back(core23::Tensor(core23::TensorParams()
                                             .data_type(core23::ToScalarType<T>::value)
                                             .shape(blob_dim)
                                             .device(device)
                                             .buffer_params(blobs_buffer_params)));
      }
      // backward input
      if (out_tensors.size() == 2) {
        dgrads_.push_back(out_tensors[1]);
      } else {
        dgrads_.push_back(out_tensors[0]);
      }
    }

  } catch (const std::runtime_error& rt_err) {
    HCTR_LOG_S(ERROR, WORLD) << rt_err.what() << std::endl;
    throw;
  }
}

template <typename T>
void MultiCrossLayer<T>::fprop(bool is_train) {
  CudaDeviceContext context(this->get_device_id());
  std::vector<core23::Tensor> kernel_tensors;
  std::vector<core23::Tensor> bias_tensors;
  std::vector<core23::Tensor> output_tensors;
  std::vector<core23::Tensor> hidden_tensors;

  if (this->projection_dim_) {
    for (int i = 0; i < num_layers_; i++) {
      kernel_tensors.push_back(this->get_weight(3 * i));
      kernel_tensors.push_back(this->get_weight(3 * i + 1));
      bias_tensors.push_back(this->get_weight(3 * i + 2));
    }
  } else {
    for (int i = 0; i < num_layers_; i++) {
      kernel_tensors.push_back(this->get_weight(2 * i));
      bias_tensors.push_back(this->get_weight(2 * i + 1));
    }
  }
  for (int i = 0; i < num_layers_; i++) {
    output_tensors.push_back(activation_tensors_[i + 1]);
    hidden_tensors.push_back(hidden_tensors_[i]);
  }
  if (this->projection_dim_ == 0) {
    // dcn v1
    MultiCrossForwardFunctor<T>()(this->get_gpu().get_stream(), this->get_gpu().get_cublas_handle(),
                                  activation_tensors_[0], kernel_tensors, bias_tensors,
                                  output_tensors, hidden_tensors, num_layers_);
  } else {
    // dcn v2
    this->dcnv2_forward_functor_(this->get_gpu().get_stream(), activation_tensors_[0],
                                 kernel_tensors, bias_tensors, XU_tensors_, output_tensors,
                                 hidden_tensors, num_layers_, xu_descrs_fprop_, xuvb_descrs_fprop_,
                                 xu_fprop_algos_, xuvb_fprop_algos_,
                                 this->get_gpu().get_cublaslt_handle());
  }
}

template <typename T>
void MultiCrossLayer<T>::bprop() {
  CudaDeviceContext context(this->get_device_id());
  std::vector<core23::Tensor> kernel_tensors;
  std::vector<core23::Tensor> kernel_output_tensors;
  std::vector<core23::Tensor> bias_output_tensors;
  std::vector<core23::Tensor> forward_output_tensors;
  std::vector<core23::Tensor> forward_hidden_tensors;
  // dcnv2
  if (this->projection_dim_) {
    for (int i = 0; i < num_layers_; i++) {
      // U
      kernel_tensors.push_back(this->get_weight(3 * i));
      // V
      kernel_tensors.push_back(this->get_weight(3 * i + 1));
      // dU
      kernel_output_tensors.push_back(this->get_wgrad(3 * i));
      // dV
      kernel_output_tensors.push_back(this->get_wgrad(3 * i + 1));
      // db
      bias_output_tensors.push_back(this->get_wgrad(3 * i + 2));
      // intermediate output
      forward_hidden_tensors.push_back(hidden_tensors_[i]);
    }
  } else {
    for (int i = 0; i < num_layers_; i++) {
      kernel_tensors.push_back(this->get_weight(2 * i));
      kernel_output_tensors.push_back(this->get_wgrad(2 * i));
      bias_output_tensors.push_back(this->get_wgrad(2 * i + 1));
      forward_hidden_tensors.push_back(hidden_tensors_[i]);
    }
  }

  for (int i = 0; i < num_layers_ - 1; i++) {
    forward_output_tensors.push_back(activation_tensors_[i + 1]);
  }
  if (this->projection_dim_ == 0) {
    // dcn v1
    MultiCrossBackwardFunctor<T>()(this->get_gpu().get_stream(), activation_tensors_[0],
                                   kernel_tensors, forward_output_tensors, forward_hidden_tensors,
                                   activation_tensors_[num_layers_], activation_tensors_[0],
                                   kernel_output_tensors, bias_output_tensors, tmp_vec_tensor_,
                                   tmp_mat_tensors_, num_layers_);
  } else {
    // dcn v2
    this->dcnv2_backward_functor_(
        this->get_gpu().get_stream(), this->wgrad_stream_, this->async_wgrad_, this->event_fork_,
        activation_tensors_[0], kernel_tensors, forward_output_tensors, forward_hidden_tensors,
        kernel_output_tensors, this->dgrads_, bias_output_tensors, this->XU_tensors_,
        accum_dx_tensor_, bprop_bottom_, num_layers_, xu_descrs_bprop_, xuvb_descrs_bprop_,
        du_descrs_bprop_, dhidden_descrs_bprop_, xu_bprop_algos_, xuvb_bprop_algos_,
        du_bprop_algos_, dhidden_bprop_algos_, this->get_gpu().get_cublaslt_handle());
  }
}
template <typename T>
void MultiCrossLayer<T>::search_algorithm() {
  // dcnv1 no search_algorithm
  CudaDeviceContext context(this->get_device_id());
  auto cublaslt_handle = this->get_gpu().get_cublaslt_handle();
  auto stream = this->get_gpu().get_stream();
  if (this->projection_dim_) {
    // setting up for fprop()
    {
      for (int i = 0; i < num_layers_; i++) {
        const auto& tensor_input = activation_tensors_[i];
        const T* mat_a = tensor_input.data<T>();
        const T* mat_b = this->get_weight(3 * i).template data<T>();
        T* mat_c = XU_tensors_[i].data<T>();

        this->xu_fprop_algos_[i].search_algorithm(1.0f, mat_a, mat_b, 0.f, mat_c, mat_c,
                                                  xu_descrs_fprop_[i], cublaslt_handle, stream);
        mat_a = XU_tensors_[i].data<T>();
        mat_b = this->get_weight(3 * i + 1).template data<T>();
        mat_c = hidden_tensors_[i].data<T>();
        this->xuvb_fprop_algos_[i].search_algorithm(1.0f, mat_a, mat_b, 0.f, mat_c, mat_c,
                                                    xuvb_descrs_fprop_[i], cublaslt_handle, stream);
      }
    }

    // setting up for bprop()
    {
      for (int i = 0; i < num_layers_; i++) {
        // 1
        const T* mat_a = XU_tensors_[i].data<T>();
        const T* mat_b = bprop_bottom_[2 * i].data<T>();
        T* mat_c = this->get_wgrad(3 * i + 1).template data<T>();
        this->xu_bprop_algos_[i].search_algorithm(1.0, mat_a, mat_b, 1.0, mat_c, mat_c,
                                                  xu_descrs_bprop_[i], cublaslt_handle, stream);
        // 2
        mat_a = bprop_bottom_[2 * i].data<T>();
        mat_b = this->get_wgrad(3 * i + 1).template data<T>();
        mat_c = bprop_bottom_[1 + 2 * i].data<T>();
        this->xuvb_bprop_algos_[i].search_algorithm(1.0, mat_a, mat_b, 0.0, mat_c, mat_c,
                                                    xuvb_descrs_bprop_[i], cublaslt_handle, stream);
        // 3
        mat_a = activation_tensors_[i].data<T>();
        mat_b = bprop_bottom_[1 + 2 * i].data<T>();
        mat_c = this->get_wgrad(3 * i).template data<T>();
        this->du_bprop_algos_[i].search_algorithm(1.0, mat_a, mat_b, 1.0, mat_c, mat_c,
                                                  du_descrs_bprop_[i], cublaslt_handle, stream);

        // 4

        mat_a = bprop_bottom_[1 + 2 * i].data<T>();
        mat_b = this->get_weight(3 * i).template data<T>();
        mat_c = this->dgrads_[i + 1].data<T>();
        T* mat_d = this->dgrads_[i].data<T>();
        this->dhidden_bprop_algos_[i].search_algorithm(1.0, mat_a, mat_b, 1.0, mat_c, mat_d,
                                                       dhidden_descrs_bprop_[i], cublaslt_handle,
                                                       stream);
      }
    }
  }
}
template <typename T>
void MultiCrossLayer<T>::initialize() {
  auto cublaslt_handle = this->get_gpu().get_cublaslt_handle();
  auto stream = this->get_gpu().get_stream();
  auto shape_to_vector = [](const core23::Shape shape) {
    std::vector<size_t> vec;
    for (int64_t i = 0; i < shape.dims(); i++) {
      vec.push_back(shape.size(i));
    }
    return vec;
  };

  if (this->projection_dim_) {
    // setting up for fprop()
    {
      for (int i = 0; i < num_layers_; i++) {
        const auto& tensor_input = activation_tensors_[i];
        std::vector<size_t> dims_a = shape_to_vector(tensor_input.shape());
        std::vector<size_t> dims_b = shape_to_vector(this->get_weight(3 * i).shape());
        this->xu_descrs_fprop_[i].set_fprop_attr(dims_a, dims_b, CUBLAS_OP_N, CUBLAS_OP_N,
                                                 CUBLASLT_ORDER_ROW, this->enable_tf32_compute_,
                                                 nullptr);
        this->xu_fprop_algos_[i].init_algorithm(this->xu_descrs_fprop_[i], cublaslt_handle);

        dims_a = shape_to_vector(XU_tensors_[i].shape());
        dims_b = shape_to_vector(this->get_weight(3 * i + 1).shape());
        T* bias = this->get_weight(3 * i + 2).template data<T>();

        this->xuvb_descrs_fprop_[i].set_fprop_attr(dims_a, dims_b, CUBLAS_OP_N, CUBLAS_OP_N,
                                                   CUBLASLT_ORDER_ROW, this->enable_tf32_compute_,
                                                   bias);
        this->xuvb_fprop_algos_[i].init_algorithm(this->xuvb_descrs_fprop_[i], cublaslt_handle);
      }
    }
    // setting up for bprop()
    {
      for (int i = 0; i < num_layers_; i++) {
        // 1
        std::vector<size_t> dims_a = shape_to_vector(XU_tensors_[i].shape());
        std::vector<size_t> dims_b = shape_to_vector(tmp_mat_tensors_[0].shape());
        T* dbias = this->get_wgrad(3 * i + 2).template data<T>();
        this->xu_descrs_bprop_[i].set_bprop_attr(dims_a, dims_b, CUBLAS_OP_T, CUBLAS_OP_N,
                                                 CUBLASLT_ORDER_ROW, this->enable_tf32_compute_,
                                                 dbias);
        this->xu_bprop_algos_[i].init_algorithm(this->xu_descrs_bprop_[i], cublaslt_handle);

        // 2
        dims_a = shape_to_vector(tmp_mat_tensors_[0].shape());
        dims_b = shape_to_vector(this->get_weight(3 * i + 1).shape());
        this->xuvb_descrs_bprop_[i].set_bprop_attr(dims_a, dims_b, CUBLAS_OP_N, CUBLAS_OP_T,
                                                   CUBLASLT_ORDER_ROW, this->enable_tf32_compute_);
        this->xuvb_bprop_algos_[i].init_algorithm(this->xuvb_descrs_bprop_[i], cublaslt_handle);

        // 3
        dims_a = shape_to_vector(activation_tensors_[i].shape());
        dims_b = shape_to_vector(XU_tensors_[i].shape());
        this->du_descrs_bprop_[i].set_bprop_attr(dims_a, dims_b, CUBLAS_OP_T, CUBLAS_OP_N,
                                                 CUBLASLT_ORDER_ROW, this->enable_tf32_compute_);
        this->du_bprop_algos_[i].init_algorithm(this->du_descrs_bprop_[i], cublaslt_handle);

        // 4
        dims_a = shape_to_vector(XU_tensors_[i].shape());
        dims_b = shape_to_vector(this->get_weight(3 * i).shape());
        this->dhidden_descrs_bprop_[i].set_bprop_attr(dims_a, dims_b, CUBLAS_OP_N, CUBLAS_OP_T,
                                                      CUBLASLT_ORDER_ROW,
                                                      this->enable_tf32_compute_);
        this->dhidden_bprop_algos_[i].init_algorithm(this->dhidden_descrs_bprop_[i],
                                                     cublaslt_handle);
      }
    }
  }
  HCTR_LIB_THROW(cudaDeviceSynchronize());
}
template <typename T>
std::unique_ptr<DataSimulator> MultiCrossLayer<T>::get_default_initializer(const int index) {
  const core23::Tensor& in_tensor = this->input_tensors_[0];
  const core23::Tensor& out_tensor = this->output_tensors_[0];
  float bottom_dim = in_tensor.shape().size(1);
  float top_dim = out_tensor.shape().size(1);
  assert(bottom_dim == top_dim);
  std::unique_ptr<DataSimulator> simu(nullptr);
  int idx = -1;
  // each dcn2 layer has one more weight tensor (U and V)
  // U V shares the same initializer, U (bottom_dim, projection_dim), V (projection_dim, top_dim)
  if (this->projection_dim_) {
    idx = index % 3;
    // U;
    if (0 == idx) {
      simu.reset(new VarianceScalingSimulator(1.f, data_simu::Mode_t::Fan_avg,
                                              data_simu::Distribution_t::Norm, bottom_dim,
                                              this->projection_dim_, false));
    }
    // V;
    else if (1 == idx) {
      simu.reset(new VarianceScalingSimulator(1.f, data_simu::Mode_t::Fan_avg,
                                              data_simu::Distribution_t::Norm,
                                              this->projection_dim_, top_dim, false));
    } else if (2 == idx) {
      simu.reset(new ConstantDataSimulator(0.0f));
    } else {
      HCTR_OWN_THROW(Error_t::OutOfBound, "index != {0, 1}.");
    }
  } else {
    idx = index % 2;
    if (0 == idx) {
      simu.reset(new VarianceScalingSimulator(1.f, data_simu::Mode_t::Fan_avg,
                                              data_simu::Distribution_t::Norm, bottom_dim, top_dim,
                                              false));
    } else if (1 == idx) {
      simu.reset(new ConstantDataSimulator(0.0f));
    } else {
      HCTR_OWN_THROW(Error_t::OutOfBound, "index != {0, 1}.");
    }
  }
  return simu;
}

template class MultiCrossLayer<float>;
template class MultiCrossLayer<__half>;

}  // namespace HugeCTR
