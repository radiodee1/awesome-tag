cd tensorflow/core/user_ops

TF_INC=$(python -c 'import tensorflow as tf; print(tf.sysconfig.get_include())')

g++-5 -std=c++11 -shared assemble_boxes.cc -o assemble_boxes.so -fPIC -I $TF_INC -O2 -D_GLIBCXX_USE_CXX11_ABI=0


