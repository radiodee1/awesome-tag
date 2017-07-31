// example.h
#ifndef KERNEL_ASSEMBLE_BOXES_H_
#define KERNEL_ASSEMBLE_BOXES_H_



template <typename Device, typename T>
struct AssembleBoxesFunctor {
  void operator()(const Device& d, int size, const T* in, T* out);
};



#define COLUMN_X 0
#define COLUMN_Y 1
#define COLUMN_W 2
#define COLUMN_H 3
#define COLUMN_NUM 4
#define COLUMN_BOX 5
#define COLUMN_TOT 6

#define BIT_TOP  0x0001
#define BIT_BOTTOM  0x0002
#define BIT_LEFT 0x0004
#define BIT_RIGHT 0x0008

#define ARRAY_END_SHAPE_X 0
#define ARRAY_END_SHAPE_Y 1
#define ARRAY_END_CHANGE_WH 2
#define ARRAY_END_LOOP_MAX 3
#define ARRAY_END_TOT 4

// something divisible by 4!
#define CUDA_LOOP_TOT 16 
#define CUDA_SHAPE_FLOAT 3.5

#endif //KERNEL_ASSEMBLE_BOXES_H_