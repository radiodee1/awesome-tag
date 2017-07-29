#ifdef GOOGLE_CUDA

#define EIGEN_USE_GPU
#define EIGEN_USE_THREADS

#include "tensorflow/core/util/cuda_kernel_helper.h"
#include "assemble_boxes_gpu.h"

#include <stdio.h>
#include <stdlib.h>

using namespace tensorflow;

#define EIGEN_USE_GPU

__device__ bool dimensionPass(uint16 locy, uint16 loch, uint16 fory, uint16 forh) {
	//return false;
	if (forh > loch * 2.5) return false;
	return not ((locy + loch < fory + forh && locy < fory + forh) || ( locy + loch > fory && locy > fory));
}

__device__ bool dimensionPass(int32 locy, int32 loch, int32 fory, int32 forh) {
	if (forh  > loch * 2.5) return false;
	return not ((locy + loch < fory + forh && locy < fory + forh) || ( locy + loch > fory && locy > fory));
}



// Define the CUDA kernel.
template <typename T>
__global__ void AssembleBoxesCudaKernel(const int size, const T* in, T* out,int shape_x, int shape_y) {
	  
	bool change_wh = true;
	//uint16 initial_w = in[0 * COLUMN_TOT + COLUMN_W];
	//uint16 initial_h = in[0 * COLUMN_TOT + COLUMN_H];
	
	int i = blockIdx.x * blockDim.x + threadIdx.x;
	
	if (i * COLUMN_TOT + 0 >= size - 2 ) return;
	  
    for (int j = 0; j < COLUMN_TOT; j ++) {
    	out[i * COLUMN_TOT + j] = in[i * COLUMN_TOT + j];
    }
    int size_img_x = size;
    out[i * COLUMN_TOT + COLUMN_NUM] = size_img_x * out[i * COLUMN_TOT + COLUMN_Y] + out[ i * COLUMN_TOT + COLUMN_X];
    
    int count = 0;
    
	while(count < 15 ) { //15 // shape_y
		uint16 local_x = out[i * COLUMN_TOT + COLUMN_X];
		uint16 local_y = out[i * COLUMN_TOT + COLUMN_Y];
		uint16 local_w = out[i * COLUMN_TOT + COLUMN_W];
		uint16 local_h = out[i * COLUMN_TOT + COLUMN_H];
		//uint16 local_box = out[i * COLUMN_TOT + COLUMN_BOX];
		
		if (local_w == 0 || local_h == 0 ){//|| local_box == 0) {
			//count ++;
			//continue;
		}
		
		for (int j = 0; j < shape_y; j ++) {
			if( i != j ) {
				// check against all others for common boundaries
				uint16 foreign_x = out[j * COLUMN_TOT + COLUMN_X];
				uint16 foreign_y = out[j * COLUMN_TOT + COLUMN_Y];
				uint16 foreign_w = out[j * COLUMN_TOT + COLUMN_W];
				uint16 foreign_h = out[j * COLUMN_TOT + COLUMN_H];
				//uint16 foreign_box = out[j * COLUMN_TOT + COLUMN_BOX];
	
				if (true ) {
					if (local_x + local_w == foreign_x && (local_y == foreign_y || dimensionPass(local_y, local_h, foreign_y, foreign_h)) ){
						//remove box walls
						if (true) {
							if (isLeft(out[j * COLUMN_TOT + COLUMN_BOX] ) ) clearLeft(out, j * COLUMN_TOT + COLUMN_BOX);
							if (isRight (out[i * COLUMN_TOT + COLUMN_BOX] )) clearRight(out, i * COLUMN_TOT + COLUMN_BOX);
							
							if (change_wh) {
								out[i * COLUMN_TOT + COLUMN_W] = out[j * COLUMN_TOT + COLUMN_W] + local_w;
								
								//setBoxPattern(out, i * COLUMN_TOT + COLUMN_BOX, out[j * COLUMN_TOT + COLUMN_BOX]);
								//out[j * COLUMN_TOT + COLUMN_X] = 0;
								//out[j * COLUMN_TOT + COLUMN_Y] = 0;
								//out[j * COLUMN_TOT + COLUMN_NUM] = 0;

							}
						}
						if (true){
							if ( out[j * COLUMN_TOT + COLUMN_NUM] > out[i * COLUMN_TOT + COLUMN_NUM]) {
								out[j * COLUMN_TOT + COLUMN_NUM] = out[i * COLUMN_TOT + COLUMN_NUM];


							}
							manipulateBoxes(in,out,i,j);
							
							
						}
					}
					
					
				}
				
				//foreign_box = out[j * COLUMN_TOT + COLUMN_BOX];
				//local_box = out[i * COLUMN_TOT + COLUMN_BOX];
				
				if( true ) {
					
					
					if ((local_x == foreign_x || dimensionPass(local_x, local_w, foreign_x, foreign_w)) && local_y + local_h == foreign_y ){
						if(true) {
							if (isTop(out[j * COLUMN_TOT + COLUMN_BOX] ) ) clearTop(out, j * COLUMN_TOT + COLUMN_BOX);
							if (isBottom(out[i * COLUMN_TOT + COLUMN_BOX] ) ) clearBottom(out, i * COLUMN_TOT + COLUMN_BOX);
							
							if (change_wh) {
								//out[i * COLUMN_TOT + COLUMN_H] = out[j * COLUMN_TOT + COLUMN_H] + local_h;
								out[i * COLUMN_TOT + COLUMN_H] = out[j * COLUMN_TOT + COLUMN_H] + local_h;
								
								//setBoxPattern(out, i * COLUMN_TOT + COLUMN_BOX, out[j * COLUMN_TOT + COLUMN_BOX]);
								//out[j * COLUMN_TOT + COLUMN_X] = 0;
								//out[j * COLUMN_TOT + COLUMN_Y] = 0;
								//out[j * COLUMN_TOT + COLUMN_NUM] = 0;
							}
							
						}
						if ( true){
							if (  out[j * COLUMN_TOT + COLUMN_NUM] > out[i * COLUMN_TOT + COLUMN_NUM]) {
								out[j * COLUMN_TOT + COLUMN_NUM] = out[i * COLUMN_TOT + COLUMN_NUM];
								//manipulateBoxes(in,out,i,j);
								
							}
							manipulateBoxes(in,out,i,j);

							
						}
					}
				}
				///////
				if (out[i* COLUMN_TOT + COLUMN_NUM] == out[j * COLUMN_TOT + COLUMN_NUM] && true) {
					
					if(out[i * COLUMN_TOT + COLUMN_BOX] == 0) {
						//out[i * COLUMN_TOT + COLUMN_NUM] = 0;
					}	
					
				}
				///////
			}
		}
		/*
		if (out[i * COLUMN_TOT + COLUMN_W] >  in[i * COLUMN_TOT + COLUMN_W] && (out[i * COLUMN_TOT + COLUMN_X] == 0 || out[i * COLUMN_TOT + COLUMN_Y] == 0)) {
			//out[i * COLUMN_TOT + COLUMN_X] = 0;
			//out[i * COLUMN_TOT + COLUMN_Y] = 0;
			//out[i * COLUMN_TOT + COLUMN_W] = 0;
			//out[i * COLUMN_TOT + COLUMN_H] = 0;
			out[i * COLUMN_TOT + COLUMN_NUM] = 0;

		}
		*/
		
		count ++;
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
__device__ void clearTop(uint16 * input, int i) {input[i] &= ~(1 << 0);}//{if (input[i] >= BIT_TOP)  input[i] = input[i] - BIT_TOP; }
__device__ void clearBottom(uint16 * input, int i) {input[i] &= ~(1 << 1);}// {if (input[i] >= BIT_BOTTOM) input[i] = input[i] - BIT_BOTTOM; }
__device__ void clearLeft(uint16 * input, int i) {input[i] &= ~(1 << 2);} //{if (input[i] >= BIT_LEFT) input[i] = input[i] - BIT_LEFT; }
__device__ void clearRight(uint16 * input, int i) {input[i] &= ~(1 << 3);} //{if (input[i] >= BIT_RIGHT) input[i] = input[i] - BIT_RIGHT; }

__device__ void clearTop(int32 * input, int i) {input[i] &= ~(1 << 0);}//{if (input[i] >= BIT_TOP)  input[i] = input[i] - BIT_TOP; }
__device__ void clearBottom(int32 * input, int i) {input[i] &= ~(1 << 1);}// {if (input[i] >= BIT_BOTTOM) input[i] = input[i] - BIT_BOTTOM; }
__device__ void clearLeft(int32 * input, int i) {input[i] &= ~(1 << 2);} //{if (input[i] >= BIT_LEFT) input[i] = input[i] - BIT_LEFT; }
__device__ void clearRight(int32 * input, int i) {input[i] &= ~(1 << 3);} //{if (input[i] >= BIT_RIGHT) input[i] = input[i] - BIT_RIGHT; }


__device__ void setBoxPattern(uint16 * out , int i, uint16 box) {
	
	out[i] = out[i] & box;
	return;
}

__device__ void setBoxPattern(int32 * out , int i, int32 box) {
	
	out[i] = out[i] & box;
	return;
}



__device__  void manipulateBoxes(const uint16 * in, uint16 * out, int i, int j) {
	///////////////
	return;
	if (  out[j * COLUMN_TOT + COLUMN_W] > out[i * COLUMN_TOT + COLUMN_W]) {
		out[j * COLUMN_TOT + COLUMN_W] = out[i * COLUMN_TOT + COLUMN_W];
		
	}
	if (  out[j * COLUMN_TOT + COLUMN_H] > out[i * COLUMN_TOT + COLUMN_H]) {
		out[j * COLUMN_TOT + COLUMN_H] = out[i * COLUMN_TOT + COLUMN_H];
		
	}
	if (  out[j * COLUMN_TOT + COLUMN_X] < out[i * COLUMN_TOT + COLUMN_X]) {
		out[j * COLUMN_TOT + COLUMN_X] = out[i * COLUMN_TOT + COLUMN_X];
		
	}
	if (  out[j * COLUMN_TOT + COLUMN_Y] < out[i * COLUMN_TOT + COLUMN_Y]) {
		out[j * COLUMN_TOT + COLUMN_Y] = out[i * COLUMN_TOT + COLUMN_Y];
		
	}
	//////////////
	
	return;
	if (  in[j * COLUMN_TOT + COLUMN_X] > in[i * COLUMN_TOT + COLUMN_X]) {
		out[i * COLUMN_TOT + COLUMN_W] = in[j * COLUMN_TOT + COLUMN_X] - in[i * COLUMN_TOT + COLUMN_X] + in[j * COLUMN_TOT + COLUMN_W];
		//out[j * COLUMN_TOT + COLUMN_W] = 0;
																												
	}
	if (  in[j * COLUMN_TOT + COLUMN_Y] > in[i * COLUMN_TOT + COLUMN_Y]) {
		out[i * COLUMN_TOT + COLUMN_H] = in[j * COLUMN_TOT + COLUMN_Y] - in[i * COLUMN_TOT + COLUMN_Y] + in[j * COLUMN_TOT + COLUMN_H];
		//out[j * COLUMN_TOT + COLUMN_H] = 0;
																																	
	}
	
	if (  in[j * COLUMN_TOT + COLUMN_X] < in[i * COLUMN_TOT + COLUMN_X]) {
		out[i * COLUMN_TOT + COLUMN_X] = in[j * COLUMN_TOT + COLUMN_X];
		//out[j * COLUMN_TOT + COLUMN_X] = 0;
															
	}
	if (  in[j * COLUMN_TOT + COLUMN_Y] < in[i * COLUMN_TOT + COLUMN_Y]) {
		out[i * COLUMN_TOT + COLUMN_Y] = in[j * COLUMN_TOT + COLUMN_Y];
		//out[j * COLUMN_TOT + COLUMN_Y] = 0;
																				
	}
	if(out[i * COLUMN_TOT + COLUMN_BOX] == 0) {
		out[i * COLUMN_TOT + COLUMN_NUM] = 0;
	}
}

__device__ void manipulateBoxes(const int32 * in, int32 * out, int i, int j) {};

// Instantiate functors for the types of OpKernels registered.
typedef Eigen::GpuDevice GPUDevice;
template struct AssembleBoxesFunctor<GPUDevice, uint16>;
template struct AssembleBoxesFunctor<GPUDevice, int32>;

#endif  // GOOGLE_CUDA