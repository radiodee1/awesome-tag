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


#endif //KERNEL_ASSEMBLE_BOXES_H_