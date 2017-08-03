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
	//if (forh > loch * CUDA_SHAPE_FLOAT ) return false;
	return not ((locy + loch < fory + forh && locy < fory + forh) || ( locy + loch > fory && locy > fory));
}

__device__ bool dimensionPass(int32 locy, int32 loch, int32 fory, int32 forh) {
	//if (forh  > loch * CUDA_SHAPE_FLOAT ) return false;
	return not ((locy + loch < fory + forh && locy < fory + forh) || ( locy + loch > fory && locy > fory));
}



// Define the CUDA kernel.
template <typename T>
__global__ void AssembleBoxesCudaKernel(const int size, const T* in, T* out,int shape_x, int shape_y) {
	  
	bool change_wh = false;
	
	int i = blockIdx.x * blockDim.x + threadIdx.x;
	
	if (i * COLUMN_TOT + 0 >= size - ARRAY_END_TOT ) return;
	  
	// read init vars from end of array
	int end_base_size = (size / COLUMN_TOT ) * COLUMN_TOT;
	int end_shape_x =  COLUMN_TOT;
	int end_shape_y = size / (int) COLUMN_TOT;
	int end_change_wh = 1;
	int end_loop_max = CUDA_LOOP_TOT;
	
	if (size >= end_base_size + ARRAY_END_SHAPE_X) end_shape_x = in[ end_base_size + ARRAY_END_SHAPE_X];
	if (size >= end_base_size + ARRAY_END_SHAPE_Y) end_shape_y = in[ end_base_size + ARRAY_END_SHAPE_Y];
	if (size >= end_base_size + ARRAY_END_CHANGE_WH) end_change_wh = in[ end_base_size + ARRAY_END_CHANGE_WH];
	if (size >= end_base_size + ARRAY_END_LOOP_MAX && in [end_base_size + ARRAY_END_LOOP_MAX] > 0) end_loop_max = in[ end_base_size + ARRAY_END_LOOP_MAX];
	
	// round-trip the array vars
	out[end_base_size + ARRAY_END_SHAPE_X] = end_shape_x;
	out[end_base_size + ARRAY_END_SHAPE_Y] = end_shape_y;
	out[end_base_size + ARRAY_END_CHANGE_WH] = end_change_wh;
	out[end_base_size + ARRAY_END_LOOP_MAX] = end_loop_max;
	
	if (end_change_wh > 0) change_wh = true;
	
    for (int j = 0; j < COLUMN_TOT; j ++) {
    	out[i * COLUMN_TOT + j] = in[i * COLUMN_TOT + j];
    }
    
    int size_img_x = size/2;
    out[i * COLUMN_TOT + COLUMN_NUM] = size_img_x * out[i * COLUMN_TOT + COLUMN_Y] + out[ i * COLUMN_TOT + COLUMN_X];
    
    int count = 0;
    
    
	while(count < end_loop_max ) { //15 // shape_y
		uint16 local_x = out[i * COLUMN_TOT + COLUMN_X];
		uint16 local_y = out[i * COLUMN_TOT + COLUMN_Y];
		uint16 local_w = out[i * COLUMN_TOT + COLUMN_W];
		uint16 local_h = out[i * COLUMN_TOT + COLUMN_H];
		//uint16 local_box = out[i * COLUMN_TOT + COLUMN_BOX];
		
		
		
		for (int j = 0; j < shape_y; j ++) {
			if( i != j ) {
				// check against all others for common boundaries
				uint16 foreign_x = out[j * COLUMN_TOT + COLUMN_X];
				uint16 foreign_y = out[j * COLUMN_TOT + COLUMN_Y];
				uint16 foreign_w = out[j * COLUMN_TOT + COLUMN_W];
				uint16 foreign_h = out[j * COLUMN_TOT + COLUMN_H];
				
	
				/////////////////////////////////////////
				
				if (( dimensionPass(foreign_x, foreign_w, local_x, local_w) || dimensionPass(local_x, local_w, foreign_x, foreign_w)) && local_y + local_h >= foreign_y && local_y + local_h <= foreign_y + foreign_h){
					if(true) {
						if (isTop(out[j * COLUMN_TOT + COLUMN_BOX] ) ) clearTop(out, j * COLUMN_TOT + COLUMN_BOX);
						if (isBottom(out[i * COLUMN_TOT + COLUMN_BOX] ) ) clearBottom(out, i * COLUMN_TOT + COLUMN_BOX);
						
						if (change_wh) {
							int difference = (in[i * COLUMN_TOT + COLUMN_H] - CUDA_BASE_WH) / 2;
							out[i * COLUMN_TOT + COLUMN_H] = out[j * COLUMN_TOT + COLUMN_H] + out[j * COLUMN_TOT + COLUMN_Y] -  out[i * COLUMN_TOT + COLUMN_Y] + difference;
							
							

						}
						
					}
					if (change_wh) manipulateBoxes(in, out, i , j);


					if ( true){
						if (  out[j * COLUMN_TOT + COLUMN_NUM] > out[i * COLUMN_TOT + COLUMN_NUM] && out[i * COLUMN_TOT + COLUMN_NUM] != 0) {
							out[j * COLUMN_TOT + COLUMN_NUM] = out[i * COLUMN_TOT + COLUMN_NUM];
							
							
						}
						else{
							
						}

						
					}
				}				
				
				else if (local_x + local_w >= foreign_x && local_x + local_w <= foreign_x + foreign_w && (dimensionPass(foreign_y, foreign_h, local_y, local_h) || dimensionPass(local_y, local_h, foreign_y, foreign_h)) ){
					//remove box walls
					if (true) {
						if (isLeft(out[j * COLUMN_TOT + COLUMN_BOX] ) ) clearLeft(out, j * COLUMN_TOT + COLUMN_BOX);
						if (isRight (out[i * COLUMN_TOT + COLUMN_BOX] )) clearRight(out, i * COLUMN_TOT + COLUMN_BOX);
						
						if (change_wh) {
							int difference = (in[i * COLUMN_TOT + COLUMN_W] - CUDA_BASE_WH) /2;
							out[i * COLUMN_TOT + COLUMN_W] = out[j * COLUMN_TOT + COLUMN_W] + out[j * COLUMN_TOT + COLUMN_X] -  out[i * COLUMN_TOT + COLUMN_X] + difference;
							
							
							
						}
					}
					if (change_wh) manipulateBoxes(in, out, i , j);

					if (true){
						if ( out[j * COLUMN_TOT + COLUMN_NUM] > out[i * COLUMN_TOT + COLUMN_NUM] && out[i * COLUMN_TOT + COLUMN_NUM] != 0) {
							out[j * COLUMN_TOT + COLUMN_NUM] = out[i * COLUMN_TOT + COLUMN_NUM];
							
						}
						else {
							
						}
						
						
					}
				}
					
					
				
					
				
				///////////////////////////////////////////
				else {
					// small boxes alone
					if (change_wh) smallBoxes(in, out, i, j, count);
					//if (change_wh) pruneBoxes(in,out, i, j, count);
					
				}
				
				if (change_wh) pruneBoxes(in,out, i, j, count);
				
			}
		}
		
		
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
__device__ void clearTop(uint16 * input, int i) {input[i] &= ~(1 << 0);}
__device__ void clearBottom(uint16 * input, int i) {input[i] &= ~(1 << 1);}
__device__ void clearLeft(uint16 * input, int i) {input[i] &= ~(1 << 2);} 
__device__ void clearRight(uint16 * input, int i) {input[i] &= ~(1 << 3);} 

__device__ void clearTop(int32 * input, int i) {input[i] &= ~(1 << 0);}
__device__ void clearBottom(int32 * input, int i) {input[i] &= ~(1 << 1);}
__device__ void clearLeft(int32 * input, int i) {input[i] &= ~(1 << 2);} 
__device__ void clearRight(int32 * input, int i) {input[i] &= ~(1 << 3);} 


__device__ void setBoxPattern(uint16 * out , int i, uint16 box) {
	
	out[i] = out[i] & box;
	return;
}

__device__ void setBoxPattern(int32 * out , int i, int32 box) {
	
	out[i] = out[i] & box;
	return;
}



__device__  void manipulateBoxes(const uint16 * in, uint16 * out, int i, int j) {
	
	int jj = j;
	//bool auto_remove = false;
	if(out[i * COLUMN_TOT + COLUMN_X] == 0 || out[i * COLUMN_TOT + COLUMN_Y] == 0) {
		jj = i;
		//return;// auto_remove = true;
		out[jj * COLUMN_TOT + COLUMN_X] = 0;
		out[jj * COLUMN_TOT + COLUMN_Y] = 0;
		out[jj * COLUMN_TOT + COLUMN_W] = 0;
		out[jj * COLUMN_TOT + COLUMN_H] = 0;
		out[jj * COLUMN_TOT + COLUMN_NUM] = 0;
		
	}
	
	if(out[j * COLUMN_TOT + COLUMN_X] == 0 || out[j * COLUMN_TOT + COLUMN_Y] == 0) {
		jj = j;
		out[jj * COLUMN_TOT + COLUMN_X] = 0;
		out[jj * COLUMN_TOT + COLUMN_Y] = 0;
		out[jj * COLUMN_TOT + COLUMN_W] = 0;
		out[jj * COLUMN_TOT + COLUMN_H] = 0;
		out[jj * COLUMN_TOT + COLUMN_NUM] = 0;
	}
	
	if (not( true && (out[i * COLUMN_TOT + COLUMN_X] <=  out[j * COLUMN_TOT + COLUMN_X] && out[i * COLUMN_TOT + COLUMN_Y] <=  out[j * COLUMN_TOT + COLUMN_Y] 
		&& out[i * COLUMN_TOT + COLUMN_W] + out[i * COLUMN_TOT + COLUMN_X] >=  out[j * COLUMN_TOT + COLUMN_W] + out[j * COLUMN_TOT + COLUMN_X] && 
		out[i * COLUMN_TOT + COLUMN_H] + out[i * COLUMN_TOT + COLUMN_Y]  >=  out[j * COLUMN_TOT + COLUMN_H] + out[j * COLUMN_TOT + COLUMN_Y] )) ) return;//&&
		
	if (not (out[i * COLUMN_TOT + COLUMN_NUM ] == out[j * COLUMN_TOT + COLUMN_NUM] ) ) return;
	jj = j;
	
	///////////////
	out[jj * COLUMN_TOT + COLUMN_X] = 0;
	out[jj * COLUMN_TOT + COLUMN_Y] = 0;
	out[jj * COLUMN_TOT + COLUMN_W] = 0;
	out[jj * COLUMN_TOT + COLUMN_H] = 0;
	out[jj * COLUMN_TOT + COLUMN_NUM] = 0;
	return;
	
	
}

__device__ void manipulateBoxes(const int32 * in, int32 * out, int i, int j) {

	int jj = j;
	//bool auto_remove = false;
	if(out[i * COLUMN_TOT + COLUMN_X] == 0 || out[i * COLUMN_TOT + COLUMN_Y] == 0) {
		jj = i;
		//return;// auto_remove = true;
		out[jj * COLUMN_TOT + COLUMN_X] = 0;
		out[jj * COLUMN_TOT + COLUMN_Y] = 0;
		out[jj * COLUMN_TOT + COLUMN_W] = 0;
		out[jj * COLUMN_TOT + COLUMN_H] = 0;
		out[jj * COLUMN_TOT + COLUMN_NUM] = 0;
		
	}
	
	if(out[j * COLUMN_TOT + COLUMN_X] == 0 || out[j * COLUMN_TOT + COLUMN_Y] == 0) {
		jj = j;
		out[jj * COLUMN_TOT + COLUMN_X] = 0;
		out[jj * COLUMN_TOT + COLUMN_Y] = 0;
		out[jj * COLUMN_TOT + COLUMN_W] = 0;
		out[jj * COLUMN_TOT + COLUMN_H] = 0;
		out[jj * COLUMN_TOT + COLUMN_NUM] = 0;
	}
	
	if (not( true && (out[i * COLUMN_TOT + COLUMN_X] <=  out[j * COLUMN_TOT + COLUMN_X] && out[i * COLUMN_TOT + COLUMN_Y] <=  out[j * COLUMN_TOT + COLUMN_Y] 
		&& out[i * COLUMN_TOT + COLUMN_W] + out[i * COLUMN_TOT + COLUMN_X] >=  out[j * COLUMN_TOT + COLUMN_W] + out[j * COLUMN_TOT + COLUMN_X] && 
		out[i * COLUMN_TOT + COLUMN_H] + out[i * COLUMN_TOT + COLUMN_Y]  >=  out[j * COLUMN_TOT + COLUMN_H] + out[j * COLUMN_TOT + COLUMN_Y] )) ) return;//&&
		
	if (not (out[i * COLUMN_TOT + COLUMN_NUM ] == out[j * COLUMN_TOT + COLUMN_NUM] ) ) return;
	jj = j;
	
	///////////////
	out[jj * COLUMN_TOT + COLUMN_X] = 0;
	out[jj * COLUMN_TOT + COLUMN_Y] = 0;
	out[jj * COLUMN_TOT + COLUMN_W] = 0;
	out[jj * COLUMN_TOT + COLUMN_H] = 0;
	out[jj * COLUMN_TOT + COLUMN_NUM] = 0;
	return;	
	
};

__device__  void pruneBoxes(const uint16 * in, uint16 * out, int i, int j, int count) {
	
	
	int jj = j;
	
	int width_i = out[i * COLUMN_TOT + COLUMN_W] ; 
	int height_i =  out[i * COLUMN_TOT + COLUMN_H] ;
			
	int difference = in[i * COLUMN_TOT + COLUMN_W] - CUDA_BASE_WH ;
	if (difference <= 1 ) difference = 1;

	bool bad_size = ((width_i > height_i * difference * 2) or ( width_i * difference * 2 < height_i));
	
	if(bad_size) {
		jj = i;
		out[jj * COLUMN_TOT + COLUMN_X] = 0;
		out[jj * COLUMN_TOT + COLUMN_Y] = 0;
		out[jj * COLUMN_TOT + COLUMN_W] = 0;
		out[jj * COLUMN_TOT + COLUMN_H] = 0;
		out[jj * COLUMN_TOT + COLUMN_NUM] = 0;
	}
	
	if ((not (out[i * COLUMN_TOT + COLUMN_NUM ] == out[j * COLUMN_TOT + COLUMN_NUM]   ))  ) return;
	
	
	int area_i = out[i * COLUMN_TOT + COLUMN_W] * out[i * COLUMN_TOT + COLUMN_H]; 
	int area_j = out[j * COLUMN_TOT + COLUMN_W] * out[j * COLUMN_TOT + COLUMN_H]; 

	
	if (area_i < area_j || count < CUDA_LOOP_TOT - 2) return;
	
	//if ( count < CUDA_LOOP_TOT - 2) return;
	

	jj = j;
	
	///////////////
	out[jj * COLUMN_TOT + COLUMN_X] = 0;
	out[jj * COLUMN_TOT + COLUMN_Y] = 0;
	out[jj * COLUMN_TOT + COLUMN_W] = 0;
	out[jj * COLUMN_TOT + COLUMN_H] = 0;
	out[jj * COLUMN_TOT + COLUMN_NUM] = 0;
	return;
	
	
}

__device__ void pruneBoxes(const int32 * in, int32 * out, int i, int j, int count) {
	
	int jj = j;
	
	int width_i = out[i * COLUMN_TOT + COLUMN_W] ; 
	int height_i =  out[i * COLUMN_TOT + COLUMN_H] ;
		
	int difference = in[i * COLUMN_TOT + COLUMN_W] - CUDA_BASE_WH ;
	if (difference <= 1 ) difference = 1;

	bool bad_size = ((width_i > height_i * difference * 2) or ( width_i * difference * 2 < height_i));
		
	//bool bad_size = ((width_i > height_i * 2) or ( width_i * 2 < height_i));
	
	if(bad_size) {
		jj = i;
		out[jj * COLUMN_TOT + COLUMN_X] = 0;
		out[jj * COLUMN_TOT + COLUMN_Y] = 0;
		out[jj * COLUMN_TOT + COLUMN_W] = 0;
		out[jj * COLUMN_TOT + COLUMN_H] = 0;
		out[jj * COLUMN_TOT + COLUMN_NUM] = 0;
	}
	
	if ((not (out[i * COLUMN_TOT + COLUMN_NUM ] == out[j * COLUMN_TOT + COLUMN_NUM]   ))  ) return;
	
	
	int area_i = out[i * COLUMN_TOT + COLUMN_W] * out[i * COLUMN_TOT + COLUMN_H]; 
	int area_j = out[j * COLUMN_TOT + COLUMN_W] * out[j * COLUMN_TOT + COLUMN_H]; 

	
	if (area_i < area_j || count < CUDA_LOOP_TOT - 2) return;
	
	//if ( count < CUDA_LOOP_TOT - 2) return;
	

	jj = j;
	
	///////////////
	out[jj * COLUMN_TOT + COLUMN_X] = 0;
	out[jj * COLUMN_TOT + COLUMN_Y] = 0;
	out[jj * COLUMN_TOT + COLUMN_W] = 0;
	out[jj * COLUMN_TOT + COLUMN_H] = 0;
	out[jj * COLUMN_TOT + COLUMN_NUM] = 0;
	return;
		
	
};

__device__  void smallBoxes(const uint16 * in, uint16 * out, int i, int j, int count) {
	
	int jj = j;
	//float mult_w = 2.5;
	//float mult_h = 2.5;
	
	//int width_i = out[i * COLUMN_TOT + COLUMN_W] ; 
	//int height_i = (int) out[i * COLUMN_TOT + COLUMN_H] ;
		
	
	int area_out = out[i * COLUMN_TOT + COLUMN_W] * out[i * COLUMN_TOT + COLUMN_H]; 
	int area_in = in[i * COLUMN_TOT + COLUMN_W] * in[i * COLUMN_TOT + COLUMN_H]; 

	if ( count < CUDA_LOOP_TOT -2 ) return;// * 3 / 4) return;
	
	//if ((area_out > area_in * CUDA_SHAPE_FLOAT * count / 2  ) && (width_i * mult_w > height_i && width_i < mult_h * height_i)) return;
	
	if ((area_out > area_in * CUDA_SHAPE_FLOAT * count / 2  ) ) return;
		

	jj = i;
	
	out[jj * COLUMN_TOT + COLUMN_X] = 0;
	out[jj * COLUMN_TOT + COLUMN_Y] = 0;
	out[jj * COLUMN_TOT + COLUMN_W] = 0;
	out[jj * COLUMN_TOT + COLUMN_H] = 0;
	out[jj * COLUMN_TOT + COLUMN_NUM] = 0;
	return;
	
	
}

__device__ void smallBoxes(const int32 * in, int32 * out, int i, int j, int count) {
	
	

	int jj = j;
	//float mult_w = 2.5;
	//float mult_h = 2.5;
	
	//int width_i = out[i * COLUMN_TOT + COLUMN_W] ; 
	//int height_i = (int) out[i * COLUMN_TOT + COLUMN_H] ;
		
	
	int area_out = out[i * COLUMN_TOT + COLUMN_W] * out[i * COLUMN_TOT + COLUMN_H]; 
	int area_in = in[i * COLUMN_TOT + COLUMN_W] * in[i * COLUMN_TOT + COLUMN_H]; 

	if ( count < CUDA_LOOP_TOT -2 ) return;// * 3 / 4) return;
	
	//if ((area_out > area_in * CUDA_SHAPE_FLOAT * count / 2  ) && (width_i * mult_w > height_i && width_i < mult_h * height_i)) return;
	
	if ((area_out > area_in * CUDA_SHAPE_FLOAT * count / 2  ) ) return;
		

	jj = i;
	
	out[jj * COLUMN_TOT + COLUMN_X] = 0;
	out[jj * COLUMN_TOT + COLUMN_Y] = 0;
	out[jj * COLUMN_TOT + COLUMN_W] = 0;
	out[jj * COLUMN_TOT + COLUMN_H] = 0;
	out[jj * COLUMN_TOT + COLUMN_NUM] = 0;
	return;
	
	//////////////////////////////
		
};

// Instantiate functors for the types of OpKernels registered.
typedef Eigen::GpuDevice GPUDevice;
template struct AssembleBoxesFunctor<GPUDevice, uint16>;
template struct AssembleBoxesFunctor<GPUDevice, int32>;

#endif  // GOOGLE_CUDA