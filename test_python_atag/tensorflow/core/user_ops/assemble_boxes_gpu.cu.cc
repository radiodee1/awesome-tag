#ifdef GOOGLE_CUDA

#define EIGEN_USE_GPU
#define EIGEN_USE_THREADS

#include "assemble_boxes_gpu.h"
#include "tensorflow/core/util/cuda_kernel_helper.h"
#include <stdio.h>
#include <stdlib.h>

using namespace tensorflow;

#define EIGEN_USE_GPU

// Define the CUDA kernel.
template <typename T>
__global__ void AssembleBoxesCudaKernel(const int size, const T* in, T* out,int shape_x, int shape_y) {
  for (int i = blockIdx.x * blockDim.x + threadIdx.x; i < size;
       i += blockDim.x * gridDim.x) {
    out[i] = 2 * ldg(in + i);
  }
}

template <class T>
__host__ void getLaunchConfiguration(T t, int n, int *blocks, int *threads) {
  cudaOccupancyMaxPotentialBlockSize(blocks, threads, t, 0, n);
  *blocks = (n + *threads - 1) / *threads;
}

// Define the GPU implementation that launches the CUDA kernel.
template <typename T>
struct AssembleBoxesFunctor<GPUDevice, T> {
  void operator()(const GPUDevice& d, int size, const T* in, T* out) {
    // Launch the cuda kernel.
    //
    // See core/util/cuda_kernel_helper.h for AssembleBoxes of computing
    // block count and thread_per_block count.
	int block_count = 1024;
	int thread_per_block = 20;
	  
	int num_columns = COLUMN_TOT;
	int num_rows = (size - 2) / num_columns;
	int shape_x = in[size - 2];
	int shape_y = in[size - 1];
	
	if (num_rows != shape_y) {
		printf("shape problem!");
		exit(0);
	}
	
	getLaunchConfiguration(AssembleBoxesCudaKernel<T>, num_rows, &block_count, &thread_per_block);
    
    AssembleBoxesCudaKernel<T>
        <<<block_count, thread_per_block, 0, d.stream()>>>(size, in, out, shape_x, shape_y);
  }
};

// Instantiate functors for the types of OpKernels registered.
typedef Eigen::GpuDevice GPUDevice;
//template struct AssembleBoxesFunctor<GPUDevice, float>;
template struct AssembleBoxesFunctor<GPUDevice, uint16>;

#endif  // GOOGLE_CUDA