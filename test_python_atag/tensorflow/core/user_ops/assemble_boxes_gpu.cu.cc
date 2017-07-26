#ifdef GOOGLE_CUDA

#define EIGEN_USE_GPU
#define EIGEN_USE_THREADS

#include "tensorflow/core/util/cuda_kernel_helper.h"
#include "assemble_boxes_gpu.h"

#include <stdio.h>
#include <stdlib.h>

using namespace tensorflow;

#define EIGEN_USE_GPU

// Define the CUDA kernel.
template <typename T>
__global__ void AssembleBoxesCudaKernel(const int size, const T* in, T* out,int shape_x, int shape_y) {
  //for (int i = blockIdx.x * blockDim.x + threadIdx.x; i < shape_y ; i += blockDim.x * gridDim.x) {
	  
	int i = blockIdx.x * blockDim.x + threadIdx.x;
	
	if (i * COLUMN_TOT + 0 >= size - 2 ) return;//* COLUMN_TOT + COLUMN_TOT >= shape_y * shape_x) return;
	  
    out[i * COLUMN_TOT] = 2 * (in[i * COLUMN_TOT] + i);
    for (int j = 1; j < COLUMN_TOT; j ++) {
    	out[i * COLUMN_TOT + j] = in[i * COLUMN_TOT + j];
    }
    out[size - 2] = in[size - 2];
    out[size - 1] = in[size - 1];
    //
    
    //////////////test box /////////////////////
    if ( isTop(in[i * COLUMN_TOT + COLUMN_BOX ]) ) {
    	out[i * COLUMN_TOT + COLUMN_Y] = 55;
    }
    if ( isBottom(in[i * COLUMN_TOT + COLUMN_BOX ]) ) {
        out[i * COLUMN_TOT + COLUMN_W] = 66;
    }
    if ( isLeft(in[i * COLUMN_TOT + COLUMN_BOX ]) ) {
		out[i * COLUMN_TOT + COLUMN_H] = 77;
	}
	if ( isRight(in[i * COLUMN_TOT + COLUMN_BOX ]) ) {
		out[i * COLUMN_TOT + COLUMN_X] = 88;
	}
	setTop( out, i * COLUMN_TOT + COLUMN_BOX );
	setBottom(out, i * COLUMN_TOT + COLUMN_BOX);
	
	clearTop(out, i * COLUMN_TOT + COLUMN_BOX);
	clearBottom(out, i * COLUMN_TOT + COLUMN_BOX);
	clearLeft(out, i * COLUMN_TOT + COLUMN_BOX);
	clearRight(out, i * COLUMN_TOT + COLUMN_BOX);
    ////////////////////////////////////////////
  
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
    
	int block_count = 1024;
	int thread_per_block = 20;
	//printf("shapes %i \n", size);
	int num_columns = COLUMN_TOT ;
	int num_rows = (size - 2) / num_columns;
	int shape_x = num_columns;
	int shape_y = num_rows;
	
	// must remember that at this point 'in' is already a pointer to
	// a cuda/gpu memory array!!
	
	getLaunchConfiguration(AssembleBoxesCudaKernel<T>, num_rows, &block_count, &thread_per_block);
    
    AssembleBoxesCudaKernel<T>
        <<<block_count, thread_per_block, 0, d.stream()>>>(size, in, out, shape_x, shape_y);
	
  }
};

__device__ bool isTop(uint16 input) {if ((input & BIT_TOP) >> 0 == 1) return true; return false;}
__device__ bool isBottom(uint16 input) {if ((input & BIT_BOTTOM) >> 1 == 1) return true; return false;}
__device__ bool isLeft(uint16 input) {if ((input & BIT_LEFT) >> 2 == 1) return true; return false;}
__device__ bool isRight(uint16 input) {if ((input & BIT_RIGHT) >> 3 == 1) return true; return false;}

//set
__device__ void setTop(uint16 * input, int i) { (input[i]) |= 1 << 0; }
__device__ void setBottom(uint16 * input, int i) { (input[i]) |= 1 << 1; }
__device__ void setLeft(uint16 * input, int i) { (input[i]) |= 1 << 2; }
__device__ void setRight(uint16 * input, int i) { (input[i]) |= 1 << 3; }

__device__ void setTop(int32 * input, int i) { (input[i]) |= 1 << 0; }
__device__ void setBottom(int32 * input, int i) { (input[i]) |= 1 << 1; }
__device__ void setLeft(int32 * input, int i) { (input[i]) |= 1 << 2; }
__device__ void setRight(int32 * input, int i) { (input[i]) |= 1 << 3; }

//clear
__device__ void clearTop(uint16 * input, int i) {if (input[i] >= BIT_TOP) input[i] = input[i] - BIT_TOP; }
__device__ void clearBottom(uint16 * input, int i) {if (input[i] >= BIT_BOTTOM) input[i] = input[i] - BIT_BOTTOM; }
__device__ void clearLeft(uint16 * input, int i) {if (input[i] >= BIT_LEFT) input[i] = input[i] - BIT_LEFT; }
__device__ void clearRight(uint16 * input, int i) {if (input[i] >= BIT_RIGHT) input[i] = input[i] - BIT_RIGHT; }

__device__ void clearTop(int32 * input, int i) {if (input[i] >= BIT_TOP) input[i] = input[i] - BIT_TOP; }
__device__ void clearBottom(int32 * input, int i) {if (input[i] >= BIT_BOTTOM) input[i] = input[i] - BIT_BOTTOM; }
__device__ void clearLeft(int32 * input, int i) {if (input[i] >= BIT_LEFT) input[i] = input[i] - BIT_LEFT; }
__device__ void clearRight(int32 * input, int i) {if (input[i] >= BIT_RIGHT) input[i] = input[i] - BIT_RIGHT; }


// Instantiate functors for the types of OpKernels registered.
typedef Eigen::GpuDevice GPUDevice;
template struct AssembleBoxesFunctor<GPUDevice, uint16>;
template struct AssembleBoxesFunctor<GPUDevice, int32>;

#endif  // GOOGLE_CUDA