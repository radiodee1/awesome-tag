#!/usr/bin/python
import os
import sys
from PIL import Image, ImageDraw, ImageFont
import math
from tensorflow.examples.tutorials.mnist import input_data
#mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

import tensorflow as tf
#import atag_dotfolder as aa
import atag_csv as enum
import nn_dim as dim

class NN(enum.Enum, dim.Dimension):
    def __init__(self, atag):
        enum.Enum.__init__(self)
        dim.Dimension.__init__(self)

        self.a = atag
        self.ckpt_folder = atag.VAR_LOCAL_DATABASE
        self.ckpt_name = atag.VAR_BASE_NAME
        self.train = False
        self.test = True
        self.load_ckpt = True
        self.save_ckpt = True

        #self.sess = tf.InteractiveSession()
        self.mnist = []
        self.mnist_train = []
        self.mnist_test = []

        self.loader = None # []
        self.use_loader = False

        self.cursor = 0
        self.cursor_tot = 0
        self.batchsize = 100
        self.dat_len = 0
        self.save_name = ""
        self.start_train = 1

        self.assemble_module = None
        self.dat = []
        self.r = []

        self.predict_skintone = False
        self.predict_softmax = False
        self.predict_conv = False
        self.predict_dot = False
        self.predict_eye = False

        self.dat_remove = []
        self.dat_best = []
        self.dat_eye = []
        self.mc_score_eyes = - 10.0

        self.dot_only = False
        self.conv_only = False
        self.eye_only = False

        self.nn_out_skintone = None
        self.nn_out_softmax = None
        self.nn_out_conv = None

        #self.key = self.a.VAR_DIM_CONFIG

        self.group_initialize = False
        self.predict_remove_symbol = 1 ## 1 or 0 ??

        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True

        self.sess = tf.InteractiveSession()

        self.load_eye_only = True

        self.load_dot_only = self.DIMENSIONS[self.key][self.COLUMN_LOAD_DOT_CONV][0]
        self.load_conv_only = self.DIMENSIONS[self.key][self.COLUMN_LOAD_DOT_CONV][1]
        print self.load_dot_only, self.load_conv_only

        if self.load_dot_only: self.nn_configure_dot()
        if self.load_conv_only: self.nn_configure_conv()

        if self.load_dot_only and self.load_conv_only:
            init = tf.global_variables_initializer().run()

        #if not self.load_conv_only and not self.load_dot_only:
        #    tf.global_variables_initializer().run()

    def nn_configure_dot(self):

        self.group_initialize = True
        #self.sess = tf.Session()

        #self.save_string = tf.Variable("load random normal", validate_shape=False)

        ''' DOT FIRST '''

        mid_num = self.DIMENSIONS[self.key][self.COLUMN_MID_DOT]
        ## DIM BLOCK ##
        input_num = self.DIMENSIONS[self.key][self.COLUMN_IN_OUT_DOT][0]
        output_num = self.DIMENSIONS[self.key][self.COLUMN_IN_OUT_DOT][1]

        if mid_num > 0:
            self.d_keep = tf.placeholder(tf.float32)
            self.d_W_2 = tf.Variable(tf.random_normal([mid_num, output_num], stddev=0.0001))
            self.d_b_2 = tf.Variable(tf.random_normal([output_num], stddev=0.001))

            self.d_x = tf.placeholder(tf.float32, [None, input_num])
            self.d_W_1 = tf.Variable(tf.random_normal([input_num, mid_num], stddev=0.0001))  # 0.0001
            self.d_b_1 = tf.Variable(tf.random_normal([mid_num], stddev=0.001))

            self.d_y_ = tf.placeholder(tf.float32, [None, output_num])

            #self.d_bump = tf.Variable(0.5)
            #self.d_x_drop = tf.nn.dropout(self.d_x, self.d_keep)

            self.d_y_logits_1 = tf.matmul(self.d_x, self.d_W_1) + self.d_b_1
            self.d_y_mid = tf.nn.relu(self.d_y_logits_1) # relu
            #self.d_y_mid = self.d_y_logits_1
            self.d_y_mid_drop = tf.nn.dropout(self.d_y_mid, self.d_keep)

            self.d_y_logits_2 = tf.matmul(self.d_y_mid_drop, self.d_W_2) + self.d_b_2
            self.d_y = tf.nn.softmax(self.d_y_logits_2 )# + self.d_cross_entropy

            self.d_y_softmax = tf.nn.softmax_cross_entropy_with_logits(logits=self.d_y_logits_2, labels=self.d_y_)

            #self.d_cross_entropy = self.d_y_softmax
            self.d_cross_entropy = tf.reduce_mean(self.d_y_softmax)

            self.d_train_step = tf.train.AdamOptimizer(0.1).minimize(self.d_cross_entropy)  # 0.0001

            # train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy) #0.5


            self.d_y_out = tf.argmax(self.d_y , 1)  ## for prediction
            #self.d_y_out_ = tf.cast(tf.ceil(tf.nn.relu(self.d_y_softmax - self.d_cross_entropy)), tf.int64)
            #self.d_y_out = tf.cast(tf.logical_not(tf.cast(tf.ceil(tf.nn.relu(self.d_y_softmax - self.d_cross_entropy)), tf.bool)),tf.int64)

        else:
            self.d_keep = tf.placeholder(tf.float32)

            self.d_x = tf.placeholder(tf.float32, [None, input_num])
            self.d_W_1 = tf.Variable(tf.random_normal([input_num, output_num], stddev=0.0001))  # 0.0004
            self.d_b_1 = tf.Variable(tf.random_normal([output_num], stddev=0.001))


            self.d_y_logits = tf.matmul(self.d_x, self.d_W_1) + self.d_b_1
            #self.d_y = self.d_y_logits #tf.nn.softmax(self.d_y_logits)
            self.d_y = tf.nn.softmax(self.d_y_logits)

            self.d_y_ = tf.placeholder(tf.float32, [None, output_num])
            self.d_y_softmax = tf.nn.softmax_cross_entropy_with_logits(logits=self.d_y_logits, labels=self.d_y_)

            self.d_cross_entropy = tf.reduce_mean(self.d_y_softmax )

            self.d_train_step = tf.train.AdamOptimizer(0.001).minimize(self.d_cross_entropy)  # 0.0001
            # train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy) #0.5

            #self.d_y_out_ = tf.cast(tf.ceil(tf.nn.relu(self.d_y_softmax - self.d_cross_entropy)), tf.int64)
            #self.d_y_out = tf.cast(tf.logical_not(tf.cast(tf.ceil(tf.nn.relu(self.d_y_softmax - self.d_cross_entropy)), tf.bool)),tf.int64)

            self.d_y_out = tf.argmax(self.d_y, 1)  ## for prediction
        #init = tf.global_variables_initializer().run()


    def nn_configure_conv(self):

        ''' CONVOLUTION NEXT '''
        #c_output = 2
        #c_input = 784 * 3

        ## DIM BLOCK ##
        c_input = self.DIMENSIONS[self.key][self.COLUMN_IN_OUT_CONV][0]
        c_output = self.DIMENSIONS[self.key][self.COLUMN_IN_OUT_CONV][1]
        c_dimx = self.DIMENSIONS[self.key][self.COLUMN_XY_CONV][0]
        c_dimy = self.DIMENSIONS[self.key][self.COLUMN_XY_CONV][1]
        c_weight_dim_1 = self.DIMENSIONS[self.key][self.COLUMN_CWEIGHT_1]
        c_bias_dim_1 = self.DIMENSIONS[self.key][self.COLUMN_CBIAS_1]
        c_weight_dim_2 = self.DIMENSIONS[self.key][self.COLUMN_CWEIGHT_2]
        c_bias_dim_2 = self.DIMENSIONS[self.key][self.COLUMN_CBIAS_2]
        c_reshape_dim_1 = self.DIMENSIONS[self.key][self.COLUMN_RESHAPE_1]
        c_reshape_dim_2 = self.DIMENSIONS[self.key][self.COLUMN_RESHAPE_2]
        c_fc_weight_dim_1 = self.DIMENSIONS[self.key][self.COLUMN_FULL_CONNECTED_W1]
        c_fc_bias_dim_1 = self.DIMENSIONS[self.key][self.COLUMN_FULL_CONNECTED_B1]
        c_fc_weight_dim_2 = self.DIMENSIONS[self.key][self.COLUMN_FULL_CONNECTED_W2]
        c_fc_bias_dim_2 = self.DIMENSIONS[self.key][self.COLUMN_FULL_CONNECTED_B2]

        def weight_variable(shape):
            initial = tf.truncated_normal(shape, stddev=0.0001) #0.1
            return tf.Variable(initial)

        def bias_variable(shape):
            initial = tf.constant(0.1, shape=shape)
            return tf.Variable(initial)

        def conv2d(x, W):
            return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

        def max_pool_2x2(x):
            return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                                  strides=[1, 2, 2, 1], padding='SAME')

        self.c_x = tf.placeholder(tf.float32, shape=[None, c_input])
        self.c_y_ = tf.placeholder(tf.float32, shape=[None, c_output])

        self.W_conv1 = weight_variable(c_weight_dim_1)
        #self.W_conv1 = weight_variable([5, 5, 3, 32])

        self.b_conv1 = bias_variable(c_bias_dim_1)
        #self.b_conv1 = bias_variable([32])

        self.x_image = tf.reshape(self.c_x, c_reshape_dim_1)
        #self.x_image = tf.reshape(self.c_x, [-1, 28, 28  , 3])

        self.h_conv1 = tf.nn.relu(conv2d(self.x_image, self.W_conv1) + self.b_conv1)
        self.h_pool1 = max_pool_2x2(self.h_conv1)

        self.W_conv2 = weight_variable(c_weight_dim_2)
        self.b_conv2 = bias_variable(c_bias_dim_2)

        #self.W_conv2 = weight_variable([5, 5, 32, 64])
        #self.b_conv2 = bias_variable([64])

        self.h_conv2 = tf.nn.relu(conv2d(self.h_pool1, self.W_conv2) + self.b_conv2)
        self.h_pool2 = max_pool_2x2(self.h_conv2)

        self.W_fc1 = weight_variable(c_fc_weight_dim_1)
        self.b_fc1 = bias_variable(c_fc_bias_dim_1)

        #self.W_fc1 = weight_variable([7 * 7 * 64, 1024])
        #self.b_fc1 = bias_variable([1024])

        self.h_pool2_flat = tf.reshape(self.h_pool2, c_reshape_dim_2)
        #self.h_pool2_flat = tf.reshape(self.h_pool2, [-1, 7 * 7 * 64 ])

        self.h_fc1 = tf.nn.relu(tf.matmul(self.h_pool2_flat, self.W_fc1) + self.b_fc1)

        self.keep_prob = tf.placeholder(tf.float32)
        self.h_fc1_drop = tf.nn.dropout(self.h_fc1, self.keep_prob)

        self.W_fc2 = weight_variable(c_fc_weight_dim_2)
        self.b_fc2 = bias_variable(c_fc_bias_dim_2)

        #self.W_fc2 = weight_variable([1024, c_output])
        #self.b_fc2 = bias_variable([c_output])

        self.y_conv = tf.matmul(self.h_fc1_drop, self.W_fc2) + self.b_fc2

        self.c_cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.y_conv, labels=self.c_y_))
        self.c_train_step = tf.train.AdamOptimizer(1e-4).minimize(self.c_cross_entropy)
        self.c_correct_prediction = tf.equal(tf.argmax(self.y_conv, 1), tf.argmax(self.c_y_, 1))
        self.c_accuracy = tf.reduce_mean(tf.cast(self.c_correct_prediction, tf.float32))

        self.c_y_out = tf.argmax(self.y_conv, 1)  ## for prediction

        #init = tf.global_variables_initializer().run()
        #self.sess.run(init)

        #summary_writer = tf.train.SummaryWriter(self.ckpt_folder + os.sep + "logs" + os.sep, self.sess.graph)

    def nn_configure_assemble(self):
        with tf.Session() as self.sess:
            self.assemble_module = tf.load_op_library('tensorflow/core/user_ops/assemble_boxes_gpu.so')
        pass

    def nn_configure_eyes(self):

        ''' CONVOLUTION EYES NEXT '''
        #c_output = 2
        #c_input = 784 * 3

        ## DIM BLOCK ##
        c_input = self.DIMENSIONS[self.key][self.COLUMN_IN_OUT_CONV][0]
        c_output = self.DIMENSIONS[self.key][self.COLUMN_IN_OUT_CONV][1]
        c_dimx = self.DIMENSIONS[self.key][self.COLUMN_XY_CONV][0]
        c_dimy = self.DIMENSIONS[self.key][self.COLUMN_XY_CONV][1]
        c_weight_dim_1 = self.DIMENSIONS[self.key][self.COLUMN_CWEIGHT_1]
        c_bias_dim_1 = self.DIMENSIONS[self.key][self.COLUMN_CBIAS_1]
        c_weight_dim_2 = self.DIMENSIONS[self.key][self.COLUMN_CWEIGHT_2]
        c_bias_dim_2 = self.DIMENSIONS[self.key][self.COLUMN_CBIAS_2]
        c_reshape_dim_1 = self.DIMENSIONS[self.key][self.COLUMN_RESHAPE_1]
        c_reshape_dim_2 = self.DIMENSIONS[self.key][self.COLUMN_RESHAPE_2]
        c_fc_weight_dim_1 = self.DIMENSIONS[self.key][self.COLUMN_FULL_CONNECTED_W1]
        c_fc_bias_dim_1 = self.DIMENSIONS[self.key][self.COLUMN_FULL_CONNECTED_B1]
        c_fc_weight_dim_2 = self.DIMENSIONS[self.key][self.COLUMN_FULL_CONNECTED_W2]
        c_fc_bias_dim_2 = self.DIMENSIONS[self.key][self.COLUMN_FULL_CONNECTED_B2]

        def weight_variable(shape):
            initial = tf.truncated_normal(shape, stddev=0.0001) #0.1
            return tf.Variable(initial)

        def bias_variable(shape):
            initial = tf.constant(0.1, shape=shape)
            return tf.Variable(initial)

        def conv2d(x, W):
            return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

        def max_pool_2x2(x):
            return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                                  strides=[1, 2, 2, 1], padding='SAME')

        self.e_x = tf.placeholder(tf.float32, shape=[None, c_input])
        self.e_y_ = tf.placeholder(tf.float32, shape=[None, c_output])

        self.W_eye1 = weight_variable(c_weight_dim_1)
        #self.W_conv1 = weight_variable([5, 5, 3, 32])

        self.b_eye1 = bias_variable(c_bias_dim_1)
        #self.b_conv1 = bias_variable([32])

        self.x_image_eye = tf.reshape(self.e_x, c_reshape_dim_1)
        #self.x_image = tf.reshape(self.c_x, [-1, 28, 28  , 3])

        self.h_eye1 = tf.nn.relu(conv2d(self.x_image_eye, self.W_eye1) + self.b_eye1)
        self.h_pool1_eye = max_pool_2x2(self.h_eye1)

        self.W_eye2 = weight_variable(c_weight_dim_2)
        self.b_eye2 = bias_variable(c_bias_dim_2)

        #self.W_conv2 = weight_variable([5, 5, 32, 64])
        #self.b_conv2 = bias_variable([64])

        self.h_eye2 = tf.nn.relu(conv2d(self.h_pool1_eye, self.W_eye2) + self.b_eye2)
        self.h_pool2_eye = max_pool_2x2(self.h_eye2)

        self.W_fc1_eye = weight_variable(c_fc_weight_dim_1)
        self.b_fc1_eye = bias_variable(c_fc_bias_dim_1)

        #self.W_fc1 = weight_variable([7 * 7 * 64, 1024])
        #self.b_fc1 = bias_variable([1024])

        self.h_pool2_flat_eye = tf.reshape(self.h_pool2_eye, c_reshape_dim_2)
        #self.h_pool2_flat = tf.reshape(self.h_pool2, [-1, 7 * 7 * 64 ])

        self.h_fc1_eye = tf.nn.relu(tf.matmul(self.h_pool2_flat_eye, self.W_fc1_eye) + self.b_fc1_eye)

        self.keep_prob_eye = tf.placeholder(tf.float32)
        self.h_fc1_drop_eye = tf.nn.dropout(self.h_fc1_eye, self.keep_prob_eye)

        self.W_fc2_eye = weight_variable(c_fc_weight_dim_2)
        self.b_fc2_eye = bias_variable(c_fc_bias_dim_2)

        #self.W_fc2 = weight_variable([1024, c_output])
        #self.b_fc2 = bias_variable([c_output])

        self.y_conv_eye = tf.matmul(self.h_fc1_drop_eye, self.W_fc2_eye) + self.b_fc2_eye

        self.e_cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.y_conv_eye, labels=self.e_y_))
        self.e_train_step = tf.train.AdamOptimizer(1e-4).minimize(self.e_cross_entropy)
        self.e_correct_prediction = tf.equal(tf.argmax(self.y_conv_eye, 1), tf.argmax(self.e_y_, 1))
        self.e_accuracy = tf.reduce_mean(tf.cast(self.e_correct_prediction, tf.float32))

        self.e_y_out = tf.argmax(self.y_conv_eye, 1)  ## for prediction

        #init = tf.global_variables_initializer().run()
        #self.sess.run(init)

        #summary_writer = tf.train.SummaryWriter(self.ckpt_folder + os.sep + "logs" + os.sep, self.sess.graph)


    def nn_clear_and_reset(self):
        tf.reset_default_graph()
        #tf.contrib.keras.backend.clear_session()
        self.sess = tf.InteractiveSession()

    def nn_global_var_init(self):
        tf.global_variables_initializer().run()

    def dot_setup(self, mid_num = 0):
        mid_num = 3

        name = "dot"
        if self.load_conv_only == True and self.load_dot_only == True: name = ""
        if self.load_ckpt : self.load_group(graph_name=name)

        if self.train :
            self.dot_only = True
            self.cursor = self.load_cursor(self.a.FOLDER_SAVED_CURSOR_DOT)

            for i in range(self.start_train,self.cursor_tot): #1000
                batch_xs, batch_ys = self.get_nn_next_train(self.batchsize, self.CONST_DOT)
                self.sess.run(self.d_train_step, feed_dict={self.d_x: batch_xs, self.d_y_: batch_ys, self.d_keep: 1.0})
                if True: #mid_num > 0:
                    cost = self.sess.run([self.d_cross_entropy], feed_dict={self.d_x: batch_xs, self.d_y_: batch_ys, self.d_keep: 1.0})
                    print cost, "cost"
                    '''
                    if (cost[0] < 0.590) and False:
                        self.save_group()
                        print "early exit"
                        exit()
                    '''

        #print name, "name"
        if self.save_ckpt and self.train : self.save_group(graph_name=name)

        if self.test :
            self.cursor = 0

            #d_correct_prediction = tf.equal(tf.round(self.d_y_softmax ), tf.cast(tf.argmax(self.d_y_,1), tf.float32))
            d_correct_prediction = tf.equal(self.d_y_out, tf.argmax(self.d_y_, 1))

            d_accuracy = tf.reduce_mean(tf.cast(d_correct_prediction, tf.float32))

            if self.use_loader : self.get_nn_next_test(self.batchsize, self.CONST_DOT)
            cost = (self.sess.run([d_accuracy], feed_dict={self.d_x: self.mnist_test.images, self.d_y_: self.mnist_test.labels, self.d_keep: 1.0}))
            print cost[0]


        if self.predict_dot :
            self.cursor = 0
            self.dat_remove = []

            if len(self.loader.dat) != self.dat_len:
                print "error"
                sys.exit()

            out = []
            start = 0 # self.start_train
            stop = self.cursor_tot
            if len(self.loader.dat) > self.cursor_tot * self.batchsize:
                stop = self.cursor_tot + 1
                print stop, "stop"

            for i in range(start, stop + 1) :
                #self.cursor = i
                batch_0, batch_1 = self.get_nn_next_predict(self.batchsize, self.CONST_DOT)
                print "batch_0", len(batch_0), self.batchsize
                if len(batch_0) > 0 :
                    out.extend( self.sess.run( self.d_y_out, feed_dict={self.d_x : batch_0, self.d_y_: batch_1, self.d_keep: 1.0}))
                    print "out" , len(out) , i, self.cursor_tot, out[-10:],"..."

            for j in range(len(out)) :
                zz = out[j]
                if int(zz) == int(self.predict_remove_symbol ) : ## 1
                    self.dat_remove.append( j )

            #print "remove dot", len(self.dat_remove), self.dat_remove
            self.loader.record.remove_lines_from_dat(self.dat_remove)
            self.loader.record.renumber_dat_list(self.loader.dat)
            print self.batchsize


    def conv_setup(self, remove_low=False, color_reject=False):

        name = "conv"
        if self.load_conv_only == True and self.load_dot_only == True: name = ""
        if self.load_ckpt : self.load_group(graph_name=name)

        #print self.load_ckpt , "load ckpt"

        if self.train :

            self.cursor = self.load_cursor(self.a.FOLDER_SAVED_CURSOR_CONV)
            print self.cursor , "cursor"
            self.conv_only = True
            for i in range(self.start_train, self.cursor_tot ):
                batch_0, batch_1 = self.get_nn_next_train(self.batchsize, self.CONST_THREE_CHANNEL)

                if i % 100 == 0:
                    train_accuracy = self.c_accuracy.eval(feed_dict={
                        self.c_x: batch_0, self.c_y_: batch_1, self.keep_prob: 1.0})
                    print("step %d, training accuracy %g" % (i, train_accuracy))
                self.c_train_step.run(feed_dict={self.c_x: batch_0, self.c_y_: batch_1, self.keep_prob: 0.5})
                cost = self.sess.run([self.c_cross_entropy], feed_dict={self.c_x: batch_0, self.c_y_: batch_1, self.keep_prob: 1.0})
                print cost, "cost"

        if self.save_ckpt and self.train  : self.save_group(graph_name=name)

        if self.test :
            self.cursor = 0
            if self.use_loader : self.get_nn_next_test(self.batchsize, self.CONST_THREE_CHANNEL)
            print("test accuracy %g" % self.c_accuracy.eval(feed_dict={
                self.c_x: self.mnist_test.images, self.c_y_: self.mnist_test.labels, self.keep_prob: 1.0}))

        if self.predict_conv :
            self.cursor = 0
            self.dat_remove = []

            out = []
            start = 0 # self.start_train
            stop = self.cursor_tot
            if len(self.loader.dat) > self.cursor_tot * self.batchsize :
                stop = self.cursor_tot + 1
                print stop

            for i in range(start, stop ) :
                batch_0, batch_1 = self.get_nn_next_predict(self.batchsize, self.CONST_THREE_CHANNEL)
                #self.c_y_out = tf.argmax(self.y_conv,1) ## 1
                if len(batch_0) > 0  :

                    #print len(batch_0), "len batch_0 2"
                    part = self.sess.run(self.c_y_out, feed_dict={self.c_x : batch_0, self.c_y_: batch_1, self.keep_prob: 1.0})
                    out.extend(part)
                    print part, len(part) , i, self.cursor_tot, "part listing..."


            if not remove_low:
                for j in range(len(out)) :
                    zz = out[j]
                    if int(zz) == int(self.predict_remove_symbol ) : ## 1
                        self.dat_remove.append( j)


            if remove_low:
                pass
                '''
                print "out", len(out)
                numlow = 0.5#0.95
                numhigh = 0.5
                numhigh_index = 0
                for j in range(len(out)) :
                    zz = out[j]
                    print zz, "raw z"
                    if float(zz) < numlow : # int(self.predict_remove_symbol ) : ## 1
                        numlow = zz
                        self.dat_remove.append( j)
                    if float(zz) > numhigh:
                        numhigh = zz
                        numhigh_index = j
                '''

            self.loader.dat = self.loader.record.remove_lines_from_dat(self.dat_remove)
            self.loader.dat = self.loader.record.renumber_dat_list(self.loader.dat)
            print "remove conv", self.dat_remove[:10],"..."

            if color_reject == True:
                self.dat = self.loader.record.recolor_dat_list(self.loader.dat, self.dat_remove,color_string=self.BLUE)
                self.loader.record.save_dat_to_file(self.dat, erase=False)

        #self.sess.close()

    def conv_setup_mc(self, remove_low = False, color_reject=False, original=None):

        name = "conv"
        if self.load_conv_only == True and self.load_dot_only == True: name = ""
        if self.load_ckpt: self.load_group(graph_name=name)

        if self.predict_conv :
            self.cursor = 0
            self.dat_remove = []
            #self.dat_best = []
            mean = 0.95

            out = []
            start = 0 # self.start_train
            stop = self.cursor_tot
            if len(self.loader.dat) > self.cursor_tot * self.batchsize :
                stop = self.cursor_tot + 1
                print stop

            #print start, stop, "start, stop"

            for i in range(start, stop ) :
                batch_0, batch_1 = self.get_nn_next_predict(self.batchsize, self.CONST_THREE_CHANNEL)
                #self.c_y_out = tf.argmax(self.y_conv,1) ## 1
                if len(batch_0) > 0  :
                    #print "show_batch", batch_0
                    #out.extend( self.sess.run(self.y_conv, feed_dict={self.c_x : batch_0, self.c_y_: batch_1, self.keep_prob: 1.0}))
                    part = self.sess.run(self.y_conv, feed_dict={self.c_x : batch_0, self.c_y_: batch_1, self.keep_prob: 1.0})
                    out.extend(part)
                    #print part, len(part) , i, self.cursor_tot
                    mean = self.sess.run(self.c_cross_entropy, feed_dict={self.c_x: batch_0, self.c_y_: batch_1, self.keep_prob: 1.0})
                    #mean = mean * 2 #1.5
                    print mean, "mean"

            if True:
                print "out", len(out)
                numlow = mean # 0.95
                numhigh = mean # 0.95
                numhigh_index = 0
                save_index = False
                for j in range(len(out)) :
                    zz = out[j][0]
                    #print zz, "raw mc", mean
                    if float(zz) < numlow : # int(self.predict_remove_symbol ) : ## 1
                        #print "activity", zz
                        numlow = zz
                        self.dat_remove.append( j )
                        save_index = False
                    elif float(zz) >= numhigh:
                        #print zz, "numhigh"
                        numhigh = zz
                        numhigh_index = j
                        save_index = True

                if save_index or not remove_low: ## or ?
                    print numhigh_index, "index"
                    self.dat_best.append(self.loader.dat[numhigh_index])


            #print out [:3], "..."
            if remove_low:
                print self.dat_remove, "dat_remove"
                #self.loader.dat = self.loader.record.remove_lines_from_dat(self.dat_remove)
                #self.loader.dat = self.loader.record.renumber_dat_list(self.loader.dat)
                #print "remove conv mc", self.dat_remove
                #self.loader.dat = self.loader.record.combine_lists(self.loader.dat, self.dat_best)
                #self.loader.dat = self.loader.record.renumber_dat_list(self.loader.dat)

            #self.loader.dat = self.loader.record.remove_lines_from_dat(self.dat_remove)

            if color_reject and False:
                self.dat = self.loader.record.recolor_dat_list(self.loader.dat, self.dat_remove, color_string=self.GREEN)
                self.loader.record.save_dat_to_file(self.dat, erase=False)
                pass
            #print "best conv mc", self.dat_best[:]

    def eye_setup(self, remove_low = False, color_reject=False, original=None, index=0):

        name = "eye"
        if self.load_conv_only == True and self.load_dot_only == True and self.load_eye_only == True: name = ""
        if self.load_ckpt: self.load_group(graph_name=name)

        if self.train :

            self.cursor = self.load_cursor(self.a.FOLDER_SAVED_CURSOR_CONV)
            print self.cursor , "cursor"
            self.eye_only = True
            for i in range(self.start_train, self.cursor_tot ):
                batch_0, batch_1 = self.get_nn_next_train(self.batchsize, self.CONST_EYES)

                if i % 100 == 0:
                    train_accuracy = self.e_accuracy.eval(feed_dict={
                        self.e_x: batch_0, self.e_y_: batch_1, self.keep_prob_eye: 1.0})
                    print("step %d, training accuracy %g" % (i, train_accuracy))
                self.e_train_step.run(feed_dict={self.e_x: batch_0, self.e_y_: batch_1, self.keep_prob_eye: 0.5})
                cost = self.sess.run([self.e_cross_entropy], feed_dict={self.e_x: batch_0, self.e_y_: batch_1, self.keep_prob_eye: 1.0})
                print cost, "cost"

        if self.save_ckpt and self.train  : self.save_group(graph_name=name)

        if self.test :
            self.cursor = 0
            if self.use_loader : self.get_nn_next_test(self.batchsize, self.CONST_EYES)
            print("test accuracy %g" % self.e_accuracy.eval(feed_dict={
                self.e_x: self.mnist_test.images, self.e_y_: self.mnist_test.labels, self.keep_prob_eye: 1.0}))


        if self.predict_eye :
            self.cursor = 0
            self.dat_remove = []
            #self.dat_best = []
            mean = 0.95

            out = []
            start = 0 # self.start_train
            stop = self.cursor_tot
            if len(self.loader.dat) > self.cursor_tot * self.batchsize :
                stop = self.cursor_tot + 1
                print stop

            #print start, stop, "start, stop"

            out_f = []
            for i in range(start, stop ) :
                batch_0, batch_1 = self.get_nn_next_predict(self.batchsize, self.CONST_EYES)
                #self.c_y_out = tf.argmax(self.y_conv,1) ## 1
                if len(batch_0) > 0  :
                    #print "show_batch", batch_0

                    #part = self.sess.run(self.y_conv_eye, feed_dict={self.e_x : batch_0, self.e_y_: batch_1, self.keep_prob_eye: 1.0})
                    part = self.sess.run(self.e_y_out, feed_dict={self.e_x : batch_0, self.e_y_: batch_1, self.keep_prob_eye: 1.0})

                    out.extend(part)
                    #print part, len(part) , i, self.cursor_tot
                    number = self.sess.run(self.y_conv_eye, feed_dict={self.e_x: batch_0, self.e_y_: batch_1, self.keep_prob_eye: 1.0})
                    #mean = mean * 2 #1.5
                    out_f.append(number)
                    #print number, "number"

            if True:
                print "eye out", len(out), out
                #out = [0 , 0, 0, 1, 1, 1, 0, 0, 0 , 1]

            if True:
                self.predict_remove_symbol = 1
                starteye = False
                mideye = False
                endeye = False
                outputeye = False
                last_i = 0
                num_endeye = len(out) // 2
                for i in range(len(out) // 2):
                    if (i == 0 and out[0] != self.predict_remove_symbol and not starteye):
                        starteye = True
                        #print "start", starteye
                    if (starteye and out[i] == self.predict_remove_symbol and not mideye):
                        mideye = True
                        #print "mid", mideye
                    if ( starteye and mideye and out[i] != self.predict_remove_symbol and not endeye):
                        endeye = True
                        #print "end", endeye
                    if  ( starteye and  mideye and  endeye and out[i] != self.predict_remove_symbol and not outputeye):
                        outputeye = True
                        last_i = i
                        #print "last i here"
                    if (out[last_i] != out[i] and outputeye):
                        outputeye = False
                        starteye = False
                        #print "reset to false"

                print "output",outputeye

                #print len(out), out, outputeye, "output eye", self.predict_remove_symbol
                if len(out_f) > 0: print len(out_f[0]), "len out-f"

                if  outputeye:
                    if len(out_f) > 0 and len(out_f[0]) > 0:
                        self.mc_score_eyes = - 10.0
                        for j in range(len(out_f[0])):
                            zz = out_f[0][j][0]
                            print zz, len(out_f[0]), "zz, len out-f", out_f[0][j]
                            if zz > self.mc_score_eyes:
                                self.mc_score_eyes = zz
                                print "new high", zz
                            pass

                        #print index, "ll.dat/nn.dat_eye", out
                        if not self.dat_eye[index] in self.dat_best:
                            self.dat_best.append(self.dat_eye[index]) ## remove symbol
                        #print self.dat_best, "best", self.mc_score_eyes, "eyes score"
                pass


            if color_reject and False:
                self.dat = self.loader.record.recolor_dat_list(self.loader.dat, self.dat_remove, color_string=self.GREEN)
                self.loader.record.save_dat_to_file(self.dat, erase=False)
                pass
            #print "best conv mc", self.dat_best[:]

    def assemble_setup(self, use_gpu=False):
        test = []
        num = 0
        filename = self.dat[0][self.FILE]
        for l in self.dat:
            line = l #.split(",")
            test.extend([int(line[self.FACE_X]), int(line[self.FACE_Y]),
                int(line[self.FACE_WIDTH]), int(line[self.FACE_HEIGHT]), num, 15])
            num += 1
        test.extend([ self.GPU_TOT, len(l), 1, 15]) # MAGIC NUMBERS
        test = tf.constant(test, dtype=tf.uint16)
        if use_gpu:
            result = self.assemble_module.assemble_boxes_op(test)
        else:
            result = self.assemble_module.assemble_boxes_cpu(test)
        self.r = result.eval()

        s = []
        new_d = []
        for i in range(len(self.r) // 6):
            #print(self.r[i * 6: i * 6 + 6])
            g = self.r[i * 6 + 4]
            if not g in s and g != 0:
                s.append(g)
                new_d.append([0,0,filename, 0,0,0,self.r[i * 6 + self.GPU_X], self.r[i * 6 + self.GPU_Y],
                              self.r[i * 6 + self.GPU_W], self.r[i * 6 + self.GPU_H] , self.RED,
                             0, g ])

        print "simple list:", s
        self.dat = new_d
        pass

    def conv_weight_img(self):
        sl8 = 8
        sl4 = 4
        sl2 = 2

        sl5 = int(self.DIMENSIONS[self.key][self.COLUMN_CWEIGHT_2][0])
        sl8 = int(self.DIMENSIONS[self.key][self.COLUMN_CWEIGHT_1][3] / 4)
        sl4 = int(self.DIMENSIONS[self.key][self.COLUMN_CWEIGHT_1][3] / 8)
        skin2 = int(math.sqrt(self.DIMENSIONS[self.key][self.COLUMN_IN_OUT_DOT][0] / 3))

        if sl4 % 2 == 1: sl4 -= 1

        print sl8, sl4, skin2, sl5

        name = ""
        if self.load_conv_only: name = "conv"
        if self.load_dot_only: name = "dot"
        if self.load_dot_only and self.load_conv_only: name = ""
        if self.load_ckpt : self.load_group(graph_name=name)

        filename2 = self.ckpt_folder + os.sep+ "visualize_weights.bmp"
        filename = self.ckpt_folder + os.sep + "visualize_weights_alternate.bmp"
        filename3 = self.ckpt_folder + os.sep + "visualize_weights_skintone.bmp"
        filename4 = self.ckpt_folder + os.sep + "visualize_weights_eyespots.bmp"


        show1 = False
        show2 = True
        show3 = True

        if self.load_conv_only:
            weights = self.sess.run(self.W_conv1)
            show2 = True
        if self.load_dot_only:
            skin = self.sess.run(self.d_W_1)
            show3 = True

        size = (sl5* sl8 * 10, sl5 * sl4 * sl2 *10)
        size2 = (sl5 * sl8 * 10, sl5 * sl4 * 10)
        size3 = (skin2 * 50 * 3, skin2 * 50)
        img = Image.new("RGBA", size, color=0)
        img2 = Image.new("RGBA", size2, color=0)
        img3 = Image.new("RGBA", size3, color=0)
        img4 = Image.new("RGBA", size2, color=0)
        xy = (0,0)
        xy2 = (0,0)
        xy3 = (0,0)
        rgba = (0,0,0,0)
        rgba2 = (0,0,0,0)
        rgba3 = (0,0,0,0)

        if True: #not self.load_conv_only and not self.load_dot_only:
            self.nn_configure_conv()
            self.nn_global_var_init()
            name = "conv"
            self.load_group(graph_name=name)
            weights = self.sess.run(self.W_conv1)
            show2 = True

        if True: #show1 or show2:
            self.show_weights_1(img2, weights)
            pass

        if self.load_eye_only:
            self.nn_clear_and_reset()
            self.nn_configure_eyes()
            self.nn_global_var_init()
            name = "eye"
            self.load_group(graph_name=name)
            weights2 = self.sess.run(self.W_eye1)
            self.show_weights_1(img4, weights2)

        if True: # not self.load_dot_only and not self.load_conv_only:
            self.nn_clear_and_reset()
            self.nn_configure_dot()
            self.nn_global_var_init()
            name = "dot"
            self.load_group(graph_name=name)
            skin = self.sess.run(self.d_W_1)
            show3 = True
        if show3:
            self.show_weights_2(img3, skin)

        if show1:
            img.show("Conv Weights B")
            img.save(filename)
        if show2:
            img2.show("Conv Weights A")
            img2.save(filename2)
        if show3:
            img3.show("Skintone Weights A")
            #print skin
            img3.save(filename3)
        if True:
            img4.show("Conv Weights Eye")
            img4.save(filename4)

    def show_weights_1(self, img, weights):

        show1 = False
        show2 = True

        sl2 = 2

        sl5 = int(self.DIMENSIONS[self.key][self.COLUMN_CWEIGHT_2][0])
        sl8 = int(self.DIMENSIONS[self.key][self.COLUMN_CWEIGHT_1][3] / 4)
        sl4 = int(self.DIMENSIONS[self.key][self.COLUMN_CWEIGHT_1][3] / 8)
        skin2 = int(math.sqrt(self.DIMENSIONS[self.key][self.COLUMN_IN_OUT_DOT][0] / 3))

        if sl4 % 2 == 1: sl4 -= 1

        for i in range(sl5):
            for j in range(sl5):
                for k in range(sl8 ):
                    for m in range(sl4  ):
                        for n in range(sl2):
                            for p in range(10):
                                for q in range(10):
                                    pass

                                    if show2:

                                        xy2 = ((k * sl5 + i) * 10 + p  , (m*n * sl5 + j) * 10 * n + q )
                                        index = k * 4 + m
                                        index = min(index, sl8 * 4 - 1)

                                        rr = weights[i][j][0][index] * 255.0 * math.pow(10, 3)
                                        gg = weights[i][j][1][index] * 255.0 * math.pow(10, 3)
                                        bb = weights[i][j][2][index] * 255.0 * math.pow(10, 3)
                                        if rr > 255: rr = 255
                                        if gg > 255: gg = 255
                                        if bb > 255: bb = 255
                                        if rr < 0: rr = 0
                                        if gg < 0: gg = 0
                                        if bb < 0: bb = 0
                                        rgba2 = (int(rr),int(gg),int(bb),0)

                                        if (k != 0 and i == 0 and p == 0) or ( m != 0 and j == 0 and q == 0) :
                                            rgba2 = (255,255,255,0)
                                        img.putpixel(xy2, rgba2)


    #print weights
    def show_weights_2(self, img3, skin):
        index = 0

        sl2 = 2

        sl5 = int(self.DIMENSIONS[self.key][self.COLUMN_CWEIGHT_2][0])
        sl8 = int(self.DIMENSIONS[self.key][self.COLUMN_CWEIGHT_1][3] / 4)
        sl4 = int(self.DIMENSIONS[self.key][self.COLUMN_CWEIGHT_1][3] / 8)
        skin2 = int(math.sqrt(self.DIMENSIONS[self.key][self.COLUMN_IN_OUT_DOT][0] / 3))

        if sl4 % 2 == 1: sl4 -= 1

        for index in range(3):
            for i in range(skin2):
                for j in range(skin2):
                    for m in range(50):
                        for n in range(50):
                            xy3 = ((i*1) * 50 + m + index * 50 * skin2, (j * 1) * 50 + n)
                            if index < 2:
                                rr = (skin[(j * skin2 + i) * 3 + 0][index] + 1.0) * 255.0 * math.pow(10, 0)
                                gg = (skin[(j * skin2 + i) * 3 + 1][index] + 1.0) * 255.0 * math.pow(10, 0)
                                bb = (skin[(j * skin2 + i) * 3 + 2][index] + 1.0) * 255.0 * math.pow(10, 0)
                                if m == 0 and n == 0 :print rr,gg,bb
                            else:
                                r1 = (skin[(j * skin2 + i) * 3 + 0][0] + 0.0)# * 255.0 * math.pow(10, 1)
                                g1 = (skin[(j * skin2 + i) * 3 + 1][0] + 0.0)# * 255.0 * math.pow(10, 1)
                                b1 = (skin[(j * skin2 + i) * 3 + 2][0] + 0.0)# * 255.0 * math.pow(10, 1)
                                r2 = (skin[(j * skin2 + i) * 3 + 0][1] + 0.0)# * 255.0 * math.pow(10, 1)
                                g2 = (skin[(j * skin2 + i) * 3 + 1][1] + 0.0)# * 255.0 * math.pow(10, 1)
                                b2 = (skin[(j * skin2 + i) * 3 + 2][1] + 0.0)# * 255.0 * math.pow(10, 1)
                                rr = (r1 + r2) /2.0  * 255.0 * math.pow(10, 4)
                                gg = (g1 + g2) /2.0  * 255.0 * math.pow(10, 4)
                                bb = (b1 + b2) /2.0  * 255.0 * math.pow(10, 4)
                                #print rr, gg, bb
                                pass

                            if rr > 255: rr = 255
                            if gg > 255: gg = 255
                            if bb > 255: bb = 255
                            if rr < 0: rr = 0
                            if gg < 0: gg = 0
                            if bb < 0: bb = 0
                            rgba3 = (int(rr), int(gg), int(bb), 0)

                            if ( m == 0 ) or ( n == 0 ):
                                rgba3 = (255, 255, 255, 0)
                            img3.putpixel(xy3, rgba3)


    def save_group(self, graph_name=""):

        print graph_name, "graph name"

        extraname = self.DIMENSIONS[self.key][self.COLUMN_NAME]
        filename = "group_" + extraname
        if graph_name != "": filename = "group_" + graph_name + "_" + extraname
        meta = True
        folder = self.ckpt_folder + os.sep + "ckpt_" + graph_name + "_" + extraname
        if not os.path.exists(folder) :
            os.makedirs(folder)
        else:
            #meta = False
            pass
        if True: #with tf.Session() as sess:
            saver = tf.train.Saver()
            #with tf.Session() as sess:
            save_path = saver.save(self.sess,  folder + os.sep + self.ckpt_name + "." + filename,
                               write_meta_graph=meta)
        if self.train:
            if self.conv_only:
                self.a.dot_write(self.a.FOLDER_SAVED_CURSOR_CONV,str(self.cursor))
                pass
            elif self.dot_only:
                self.a.dot_write(self.a.FOLDER_SAVED_CURSOR_DOT, str(self.cursor))
                pass

        print ("saved?", filename, save_path)

    def load_group(self, graph_name=""):

        extraname = self.DIMENSIONS[self.key][self.COLUMN_NAME]
        filename = "group_" + extraname
        if graph_name != "": filename = "group_" + graph_name + "_" + extraname
        file2 = self.ckpt_folder + os.sep + "ckpt_" + graph_name + "_" + extraname + os.sep
        ckpt = tf.train.get_checkpoint_state(file2 + ".")

        file = self.ckpt_folder + os.sep + "ckpt_" + graph_name + "_" + extraname + os.sep + self.ckpt_name + "." + filename
        if ckpt and ckpt.model_checkpoint_path: # os.path.isfile(file) or True:

            if True: #with tf.Session() as sess:
                #saver = tf.train.import_meta_graph(file )
                saver = tf.train.Saver()
                saver.restore(self.sess, file)
                #saver.restore(sess, tf.train.latest_checkpoint(file2 + "."))
                #self.sess = sess
            print ("load?", filename, file)
        else :
            print "not loaded -- " + file
            #exit()

    def load_cursor(self, folder):
        default = 0
        if  os.path.isfile(self.a.FOLDER_FULL_DOTFOLDER + os.sep +folder):
            try:
                default = int(self.a.dot_read(folder))
            except:
                default = 0
        return default

    def set_loader(self, load):
        self.loader = load
        self.cursor = 0
        self.use_loader = True

    def set_vars(self, length,  batchsize, start = 1, adjust_x=False):
        self.batchsize = batchsize
        self.dat_len = length
        self.cursor_tot = int(length / batchsize) ## -1
        self.save_name = "group-miss"
        #self.start_train = start
        #self.loader.start_num = start
        self.cursor = start
        #print "vars", self.cursor_tot, self.save_name
        if self.loader != None:
            self.loader.special_horizontal_align = adjust_x

    def get_nn_next_predict(self, batchsize, num_channels = 1):
        print self.cursor, num_channels, "cursor, num-channels"
        images, labels = self.loader.get_nn_next_predict(batchsize, self.cursor, num_channels)
        self.cursor = self.cursor + 1
        return images, labels

    def get_nn_next_train(self, batchsize, num_channels = 1):
        if not self.use_loader :
            images = self.mnist_train.images[self.cursor * batchsize : self.cursor * batchsize + batchsize]
            lables = self.mnist_train.labels[self.cursor * batchsize : self.cursor * batchsize + batchsize]
            self.cursor = self.cursor + 1
            #print ("not use loader")
        else:
            print (len(self.loader.dat), self.cursor_tot, self.cursor, "len,tot,cursor")
            if self.cursor < self.cursor_tot :

                images, lables = self.loader.get_nn_next_train(batchsize, self.cursor, num_channels)
                #print ("next train batch")
            else:
                #self.cursor = 0
                #self.save_group()
                print "exit at end"
                #images, lables = self.loader.get_nn_next_train(batchsize, self.cursor, num_channels)

                if self.dot_only: name = "dot"
                if self.conv_only: name = "conv"
                if self.eye_only: name = "eye"

                self.save_group(graph_name=name)

                sys.exit()
                #self.cursor += 1
                #return images, lables

            self.cursor = self.cursor + 1

        #print lables, "lables"
        return  images, lables

    def get_nn_next_test(self, batchsize, num_channels = 1):
        #print ("test", self.cursor_tot, num_channels)
        self.mnist_test = self.loader.get_nn_next_test(batchsize, num_channels)
