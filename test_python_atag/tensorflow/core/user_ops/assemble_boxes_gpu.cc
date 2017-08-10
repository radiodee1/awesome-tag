// AssembleBoxes.cc
#define EIGEN_USE_THREADS
#include "assemble_boxes_gpu.h"
#include "tensorflow/core/framework/op_kernel.h"

#include <stdio.h>
#include <stdlib.h>

using namespace tensorflow;


REGISTER_OP("AssembleBoxesOp")
	.Attr("T: {int32, uint16}")
    .Input("input: T")
    .Output("out: T");

REGISTER_OP("AssembleBoxesCpu")
	.Attr("T: { uint16}")
    .Input("input: T")
    .Output("out: T");
    


using CPUDevice = Eigen::ThreadPoolDevice;
using GPUDevice = Eigen::GpuDevice;

// CPU specialization of actual computation.

class AssembleBoxesCpu : public OpKernel {
 public:
  explicit AssembleBoxesCpu(OpKernelConstruction* context) : OpKernel(context) {}

  void Compute(OpKernelContext* context) override {
    // Grab the input tensor
    const Tensor& input_tensor = context->input(0);
    auto input = input_tensor.flat<uint16>();

    // Create an output tensor
    Tensor* output_tensor = NULL;
    OP_REQUIRES_OK(context, context->allocate_output(0, input_tensor.shape(),
                                                     &output_tensor));
    auto output_flat = output_tensor->flat<uint16>();

    int num_columns = COLUMN_TOT ;
    int num_rows = (input.size() - ARRAY_END_TOT ) / num_columns;
    int shape_x = num_columns;
    int shape_y = num_rows;
    
    // Set all but the first element of the output tensor to 0.
    const int N = input.size();
    for (int i = 0; i < N / COLUMN_TOT; i++) {
      //output_flat(i) = 10;
      AssembleBoxesCpuKernel(N, input.data(), output_flat.data() , shape_x,  shape_y, i) ;
    }

    // Preserve the first input value if possible.
    //if (N > 0) output_flat(0) = input(0);
  }
};

// OpKernel definition.
// template parameter <T> is the datatype of the tensors.
template <typename Device, typename T>
class AssembleBoxesOp : public OpKernel {
 public:
  explicit AssembleBoxesOp(OpKernelConstruction* context) : OpKernel(context) {}

  void Compute(OpKernelContext* context) override {
	//printf("get here.1\n");

    // Grab the input tensor
    const Tensor& input_tensor = context->input(0);

    // Create an output tensor
    Tensor* output_tensor = NULL;
    OP_REQUIRES_OK(context, context->allocate_output(0, input_tensor.shape(), &output_tensor));

    // Do the computation.
    OP_REQUIRES(context, input_tensor.NumElements() <= tensorflow::kint32max, errors::InvalidArgument("Too many elements in tensor"));
    
    //printf("get here.2\n");
    
    AssembleBoxesFunctor<Device, T>()(
        context->eigen_device<Device>(),
        static_cast<int>(input_tensor.NumElements()),
        input_tensor.flat<T>().data(),
        output_tensor->flat<T>().data());
     
  }
};



// Register the CPU kernels.
REGISTER_KERNEL_BUILDER(Name("AssembleBoxesCpu").Device(DEVICE_CPU), AssembleBoxesCpu);



// Register the GPU kernels.
#ifdef GOOGLE_CUDA
#define REGISTER_GPU(T)                                          \
  REGISTER_KERNEL_BUILDER(                                       \
      Name("AssembleBoxesOp").Device(DEVICE_GPU).TypeConstraint<T>("T"), \
      AssembleBoxesOp<GPUDevice, T>);
REGISTER_GPU(int32);
REGISTER_GPU(uint16);


#endif  // GOOGLE_CUDA