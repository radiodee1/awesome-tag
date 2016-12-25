#!/usr/bin/python
import os
import sys

from tensorflow.examples.tutorials.mnist import input_data
#mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

import tensorflow as tf
#import atag_dotfolder as aa

class NN(object):
    def __init__(self, atag):
        self.ckpt_folder = atag.VAR_LOCAL_DATABASE
        self.ckpt_name = atag.VAR_BASE_NAME
        self.train = False
        self.test = True
        self.load_ckpt = True
        self.save_ckpt = False

        self.sess = tf.InteractiveSession()
        self.mnist = []
        self.mnist_train = []
        self.mnist_test = []

        self.loader = []
        self.use_loader = False

        self.cursor = 0
        self.cursor_tot = 0
        self.batchsize = 100
        self.save_name = ""
        self.start_train = 1

        self.predict_skintone = False
        self.predict_softmax = False
        self.predict_conv = False

        self.dat_remove = []

        self.nn_out_skintone = None
        self.nn_out_softmax = None
        self.nn_out_conv = None

        self.group_initialize = False
        self.predict_remove_symbol = 0 ## 1 or 0 ??

        self.nn_configure()

    def nn_configure(self):

        self.group_initialize = True
        self.sess = tf.InteractiveSession()

        ''' DOT FIRST '''
        input_num = 4 * 3  # like mnist but with three channels
        #mid_num = 5  # 10
        output_num = 2

        self.d_x = tf.placeholder(tf.float32, [None, input_num])
        self.d_W_1 = tf.Variable(tf.random_normal([input_num, output_num], stddev=0.0001))  # 0.0004
        self.d_b_1 = tf.Variable(tf.random_normal([output_num], stddev=0.5))

        # y_mid = tf.nn.relu(tf.matmul(x,W_1) + b_1)
        #self.d_y_mid = tf.nn.relu(tf.matmul(self.d_x, self.d_W_1) + self.d_b_1)

        #self.d_W_2 = tf.Variable(tf.random_normal([mid_num, output_num], stddev=0.0001))
        #self.d_b_2 = tf.Variable(tf.random_normal([output_num], stddev=0.5))

        self.d_y_logits = tf.matmul(self.d_x, self.d_W_1) + self.d_b_1
        self.d_y = tf.nn.softmax(self.d_y_logits)

        self.d_y_ = tf.placeholder(tf.float32, [None, output_num])

        # cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
        self.d_cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(self.d_y_logits, self.d_y_))

        self.d_train_step = tf.train.GradientDescentOptimizer(0.0001).minimize(self.d_cross_entropy)  # 0.0001
        # train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy) #0.5

        self.d_y_out = tf.argmax(self.d_y, 1)  ## for prediction

        ''' SOFTMAX NEXT '''
        input_num = 784 * 3  # like mnist but with three channels
        mid_num = 50  # 10
        output_num = 2

        self.x = tf.placeholder(tf.float32, [None, input_num])
        self.W_1 = tf.Variable(tf.random_normal([input_num, mid_num], stddev=0.0004))  # 0.0004
        self.b_1 = tf.Variable(tf.random_normal([mid_num], stddev=0.5))

        # y_mid = tf.nn.relu(tf.matmul(x,W_1) + b_1)
        self.y_mid = tf.nn.relu(tf.matmul(self.x, self.W_1) + self.b_1)

        self.W_2 = tf.Variable(tf.random_normal([mid_num, output_num], stddev=0.0004))
        self.b_2 = tf.Variable(tf.random_normal([output_num], stddev=0.5))

        self.y_logits = tf.matmul(self.y_mid, self.W_2) + self.b_2
        self.y = tf.nn.softmax(self.y_logits)

        self.y_ = tf.placeholder(tf.float32, [None, output_num])

        # cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
        self.cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(self.y_logits, self.y_))

        self.train_step = tf.train.GradientDescentOptimizer(0.0001).minimize(self.cross_entropy)  # 0.0001
        # train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy) #0.5

        self.y_out = tf.argmax(self.y, 1)  ## for prediction

        ''' CONVOLUTION NEXT '''
        c_output = 2

        def weight_variable(shape):
            initial = tf.truncated_normal(shape, stddev=0.1)
            return tf.Variable(initial)

        def bias_variable(shape):
            initial = tf.constant(0.1, shape=shape)
            return tf.Variable(initial)

        def conv2d(x, W):
            return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

        def max_pool_2x2(x):
            return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                                  strides=[1, 2, 2, 1], padding='SAME')

        self.c_x = tf.placeholder(tf.float32, shape=[None, 784])
        self.c_y_ = tf.placeholder(tf.float32, shape=[None, c_output])

        ###self.sess = tf.InteractiveSession()

        self.W_conv1 = weight_variable([5, 5, 1, 32])
        self.b_conv1 = bias_variable([32])
        self.x_image = tf.reshape(self.c_x, [-1, 28, 28, 1])
        self.h_conv1 = tf.nn.relu(conv2d(self.x_image, self.W_conv1) + self.b_conv1)
        self.h_pool1 = max_pool_2x2(self.h_conv1)

        self.W_conv2 = weight_variable([5, 5, 32, 64])
        self.b_conv2 = bias_variable([64])

        self.h_conv2 = tf.nn.relu(conv2d(self.h_pool1, self.W_conv2) + self.b_conv2)
        self.h_pool2 = max_pool_2x2(self.h_conv2)

        self.W_fc1 = weight_variable([7 * 7 * 64, 1024])
        self.b_fc1 = bias_variable([1024])

        self.h_pool2_flat = tf.reshape(self.h_pool2, [-1, 7 * 7 * 64])
        self.h_fc1 = tf.nn.relu(tf.matmul(self.h_pool2_flat, self.W_fc1) + self.b_fc1)

        self.keep_prob = tf.placeholder(tf.float32)
        self.h_fc1_drop = tf.nn.dropout(self.h_fc1, self.keep_prob)

        self.W_fc2 = weight_variable([1024, c_output])
        self.b_fc2 = bias_variable([c_output])

        self.y_conv = tf.matmul(self.h_fc1_drop, self.W_fc2) + self.b_fc2

        self.c_cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(self.y_conv, self.c_y_))
        self.c_train_step = tf.train.AdamOptimizer(1e-4).minimize(self.c_cross_entropy)
        self.c_correct_prediction = tf.equal(tf.argmax(self.y_conv, 1), tf.argmax(self.c_y_, 1))
        self.c_accuracy = tf.reduce_mean(tf.cast(self.c_correct_prediction, tf.float32))

        self.c_y_out = tf.argmax(self.y_conv, 1)  ## for prediction

        init = tf.initialize_all_variables()
        self.sess.run(init)

        #summary_writer = tf.train.SummaryWriter(self.ckpt_folder + os.sep + "logs" + os.sep, self.sess.graph)


    def dot_setup(self):

        if self.load_ckpt : self.load_group()

        if self.train :
            self.cursor = 0

            for i in range(self.start_train,self.cursor_tot): #1000
                batch_xs, batch_ys = self.get_nn_next_train(self.batchsize, 12)
                self.sess.run(self.d_train_step, feed_dict={self.d_x: batch_xs, self.d_y_: batch_ys})

        if self.save_ckpt and self.train : self.save_group()

        if self.test :
            d_correct_prediction = tf.equal(tf.argmax(self.d_y,1), tf.argmax(self.d_y_,1))
            d_accuracy = tf.reduce_mean(tf.cast(d_correct_prediction, tf.float32))

            if self.use_loader : self.get_nn_next_test(self.batchsize, 12)
            print(self.sess.run(d_accuracy, feed_dict={self.d_x: self.mnist_test.images, self.d_y_: self.mnist_test.labels}))

        if self.predict_softmax :
            self.cursor = 0
            self.dat_remove = []

            out = []
            start = 0 # self.start_train
            stop = self.cursor_tot
            if len(self.loader.dat) > self.cursor_tot * self.batchsize:
                stop = self.cursor_tot + 1
                print stop

            for i in range(start, stop ) :
                batch_0, batch_1 = self.get_nn_next_predict(self.batchsize, 12)
                #self.y_out = tf.argmax(self.y,1) # 1
                if len(batch_0) > 0:
                    out.extend( self.sess.run(self.d_y_out, feed_dict={self.d_x : batch_0, self.d_y_: batch_1}))
                    print out, len(out) , i, self.cursor_tot

            for j in range(len(out)) :
                zz = out[j]
                if zz == self.predict_remove_symbol : ## 1
                    self.dat_remove.append( j )

            self.loader.record.remove_lines_from_dat(self.dat_remove)
            self.loader.record.renumber_dat_list(self.loader.dat)
            print "remove skintone", self.dat_remove


    def skintone_setup(self):

        if self.load_ckpt : self.load_group()

        if self.train :
            self.cursor = 0

            for i in range(self.start_train,self.cursor_tot): #1000
                batch_xs, batch_ys = self.get_nn_next_train(self.batchsize, 3)
                self.sess.run(self.train_step, feed_dict={self.x: batch_xs, self.y_: batch_ys})

        if self.save_ckpt and self.train : self.save_group()

        if self.test :
            correct_prediction = tf.equal(tf.argmax(self.y,1), tf.argmax(self.y_,1))
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

            if self.use_loader : self.get_nn_next_test(self.batchsize, 3)
            print(self.sess.run(accuracy, feed_dict={self.x: self.mnist_test.images, self.y_: self.mnist_test.labels}))

        if self.predict_softmax :
            self.cursor = 0
            self.dat_remove = []

            out = []
            start = 0 # self.start_train
            stop = self.cursor_tot
            if len(self.loader.dat) > self.cursor_tot * self.batchsize:
                stop = self.cursor_tot + 1
                print stop

            for i in range(start, stop ) :
                batch_0, batch_1 = self.get_nn_next_predict(self.batchsize, 3)
                #self.y_out = tf.argmax(self.y,1) # 1
                if len(batch_0) > 0:
                    out.extend( self.sess.run(self.y_out, feed_dict={self.x : batch_0, self.y_: batch_1}))
                    print out, len(out) , i, self.cursor_tot

            for j in range(len(out)) :
                zz = out[j]
                if zz == self.predict_remove_symbol : ## 1
                    self.dat_remove.append( j )

            self.loader.record.remove_lines_from_dat(self.dat_remove)
            self.loader.record.renumber_dat_list(self.loader.dat)
            print "remove skintone", self.dat_remove


    def conv_setup(self):
        #c_output = 2

        if self.load_ckpt : self.load_group()

        if self.train :
            #self.cursor = 0
            for i in range(self.start_train, self.cursor_tot ):
                batch_0, batch_1 = self.get_nn_next_train(self.batchsize)

                if i % 100 == 0:
                    train_accuracy = self.c_accuracy.eval(feed_dict={
                        self.c_x: batch_0, self.c_y_: batch_1, self.keep_prob: 1.0})
                    print("step %d, training accuracy %g" % (i, train_accuracy))
                self.c_train_step.run(feed_dict={self.c_x: batch_0, self.c_y_: batch_1, self.keep_prob: 0.5})

        if self.save_ckpt and self.train  : self.save_group()

        if self.test :
            if self.use_loader : self.get_nn_next_test(self.batchsize)
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
                batch_0, batch_1 = self.get_nn_next_predict(self.batchsize)
                #self.c_y_out = tf.argmax(self.y_conv,1) ## 1
                if len(batch_0) > 0  :
                    out.extend( self.sess.run(self.c_y_out, feed_dict={self.c_x : batch_0, self.c_y_: batch_1, self.keep_prob: 1.0}))
                    #print out, len(out) , i, self.cursor_tot

            for j in range(len(out)) :
                zz = out[j]
                if zz == self.predict_remove_symbol : ## 1
                    self.dat_remove.append( j)

            self.loader.record.remove_lines_from_dat(self.dat_remove)
            self.loader.record.renumber_dat_list(self.loader.dat)
            print "remove conv", self.dat_remove

        #self.sess.close()


    def save_group(self):
        filename = "group" # self.save_name
        #self.ckpt_name = filename
        folder = self.ckpt_folder + os.sep + "ckpt"
        if not os.path.exists(folder) :
            os.makedirs(folder)
        saver = tf.train.Saver()
        save_path = saver.save(self.sess, folder + os.sep + self.ckpt_name + "."+ filename)
        print ("saved?", filename)

    def load_group(self):
        filename = "group"
        #self.ckpt_name = filename
        file = self.ckpt_folder + os.sep + "ckpt" + os.sep + self.ckpt_name + "." + filename
        if os.path.isfile(file):
            saver = tf.train.Saver()
            saver.restore(self.sess, file)
            print ("load?", filename)


    def set_loader(self, load):
        self.loader = load
        self.cursor = 0
        self.use_loader = True

    def set_vars(self, length,  batchsize, start = 1):
        self.cursor_tot = int(length / batchsize) ## -1
        self.save_name = "group-miss"
        #self.start_train = start
        #self.loader.start_num = start
        self.cursor = start
        #print "vars", self.cursor_tot, self.save_name

    def get_nn_next_predict(self, batchsize, num_channels = 1):
        print self.cursor, num_channels
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
                pass
                self.save()
                sys.exit()

            self.cursor = self.cursor + 1

        #print lables, "lables"
        return  images, lables

    def get_nn_next_test(self, batchsize, num_channels = 1):
        #print ("test", self.cursor_tot, num_channels)
        self.mnist_test = self.loader.get_nn_next_test(batchsize, num_channels)
