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
//#define COLUMN_SHAPE_X 6
//#define COLUMN_SHAPE_Y 7
#define COLUMN_TOT 6



#endif //KERNEL_ASSEMBLE_BOXES_H_