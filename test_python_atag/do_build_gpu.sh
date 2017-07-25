export CC=gcc-5
export CXX=g++-5

cd tensorflow/core/user_ops

TF_INC=$(python -c 'import tensorflow as tf; print(tf.sysconfig.get_include())')


nvcc  -std=c++11 -c -o assemble_boxes_gpu.cu.o assemble_boxes_gpu.cu.cc \
-I $TF_INC -D GOOGLE_CUDA=1 -x cu -Xcompiler -fPIC --expt-relaxed-constexpr  


g++-5 -std=c++11 -shared -o assemble_boxes_gpu.so assemble_boxes_gpu.cc \
assemble_boxes_gpu.cu.o -I $TF_INC -fPIC -lcudart -D_GLIBCXX_USE_CXX11_ABI=0 -L /usr/lib/nvidia-375/


#  /usr/lib/nvidia-cuda-toolkit
