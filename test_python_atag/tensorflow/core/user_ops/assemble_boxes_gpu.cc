// AssembleBoxes.cc
#define EIGEN_USE_THREADS
#include "assemble_boxes_gpu.h"
#include "tensorflow/core/framework/op_kernel.h"

using namespace tensorflow;


REGISTER_OP("AssembleBoxesGpu")
    .Input("in: uint16")
    .Output("out: uint16");
    


using CPUDevice = Eigen::ThreadPoolDevice;
using GPUDevice = Eigen::GpuDevice;

// CPU specialization of actual computation.

template <typename T>
struct AssembleBoxesFunctor<CPUDevice, T> {
  void operator()(const CPUDevice& d, int size, const T* in, T* out) {
    for (int i = 0; i < size; ++i) {
      out[i] = 2 * in[i];
    }
  }
};


// OpKernel definition.
// template parameter <T> is the datatype of the tensors.
template <typename Device, typename T>
class AssembleBoxesOp : public OpKernel {
 public:
  explicit AssembleBoxesOp(OpKernelConstruction* context) : OpKernel(context) {}

  void Compute(OpKernelContext* context) override {
    // Grab the input tensor
    const Tensor& input_tensor = context->input(0);

    // Create an output tensor
    Tensor* output_tensor = NULL;
    OP_REQUIRES_OK(context, context->allocate_output(0, input_tensor.shape(),
                                                     &output_tensor));

    // Do the computation.
    //OP_REQUIRES(context, input_tensor.NumElements() <= tensorflow::kint32max,
    //            errors::InvalidArgument("Too many elements in tensor"));
    
    AssembleBoxesFunctor<Device, T>()(
        context->eigen_device<Device>(),
        static_cast<int>(input_tensor.NumElements()),
        input_tensor.flat<T>().data(),
        output_tensor->flat<T>().data());
  }
};



// Register the CPU kernels.
/*
#define REGISTER_CPU(T)                                          \
  REGISTER_KERNEL_BUILDER(                                       \
      Name("AssembleBoxesCpu").Device(DEVICE_CPU).TypeConstraint<T>("T"), \
      AssembleBoxes<CPUDevice, T>);
//REGISTER_CPU(float);
REGISTER_CPU(uint16);
*/

// Register the GPU kernels.
#ifdef GOOGLE_CUDA
#define REGISTER_GPU(T)                                          \
  REGISTER_KERNEL_BUILDER(                                       \
      Name("AssembleBoxesGpu").Device(DEVICE_GPU).TypeConstraint<T>("T"), \
      AssembleBoxesOp<GPUDevice, T>);
//REGISTER_GPU(float);
REGISTER_GPU(uint16);
#endif  // GOOGLE_CUDA