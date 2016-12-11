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

    def skintone_setup(self):
        input_num = 4 * 3
        mid_num = 3
        output_num = 2

        x = tf.placeholder(tf.float32, [None, input_num])
        W_1 = tf.Variable(tf.random_normal([input_num, mid_num], stddev=0.5))
        b_1 = tf.Variable(tf.random_normal([mid_num], stddev=0.5))

        y_mid = tf.nn.relu(tf.matmul(x,W_1) + b_1)

        W_2 = tf.Variable(tf.random_normal([mid_num, output_num], stddev=0.5))
        b_2 = tf.Variable(tf.random_normal([output_num],stddev=0.5))

        y_logits = tf.matmul(y_mid, W_2) + b_2
        y = tf.nn.softmax(y_logits)
        #y = tf.nn.softmax(tf.matmul(y_mid, W_2) + b_2)

        y_ = tf.placeholder(tf.float32, [None, output_num])

        cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y_logits, y_))

        train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy) #0.5
        #train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy) #0.5

        init = tf.initialize_all_variables()
        #init = tf.global_variables_initializer()
        #self.sess = tf.Session()
        self.sess.run(init)

        #summary_writer = tf.train.SummaryWriter(self.ckpt_folder + os.sep + "logs" + os.sep, self.sess.graph)

        if self.load_ckpt : self.load()

        if self.train :
            self.cursor = 0
            for i in range(1,self.cursor_tot): #1000
                batch_xs, batch_ys = self.get_nn_next_train(self.batchsize, 12)
                self.sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

        if self.save_ckpt and self.train : self.save()

        if self.test :
            correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

            #print self.sess.run(y_)

            if self.use_loader : self.get_nn_next_test(self.batchsize, 12)
            print(self.sess.run(accuracy, feed_dict={x: self.mnist_test.images, y_: self.mnist_test.labels}))


    def softmax_setup(self):
        input_num = 784 * 3 # like mnist but with three channels
        mid_num = 50 # 10
        output_num = 2

        x = tf.placeholder(tf.float32, [None, input_num])
        W_1 = tf.Variable(tf.random_normal([input_num, mid_num], stddev=0.0004)) #0.0004
        b_1 = tf.Variable(tf.random_normal([mid_num], stddev=0.5))

        #y_mid = tf.nn.relu(tf.matmul(x,W_1) + b_1)
        y_mid = tf.nn.relu(tf.matmul(x,W_1) + b_1)

        W_2 = tf.Variable(tf.random_normal([mid_num, output_num],stddev=0.0004))
        b_2 = tf.Variable(tf.random_normal([output_num],stddev=0.5))

        y_logits = tf.matmul(y_mid, W_2) + b_2
        y = tf.nn.softmax(y_logits)

        y_ = tf.placeholder(tf.float32, [None, output_num])

        #cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
        cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y_logits, y_))

        train_step = tf.train.GradientDescentOptimizer(0.0001).minimize(cross_entropy) #0.0001
        #train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy) #0.5

        init = tf.initialize_all_variables()
        #init = tf.global_variables_initializer()
        #self.sess = tf.Session()
        self.sess.run(init)


        summary_writer = tf.train.SummaryWriter(self.ckpt_folder + os.sep + "logs" + os.sep, self.sess.graph)

        if self.load_ckpt : self.load()

        if self.train :
            self.cursor = 0

            for i in range(self.start_train,self.cursor_tot): #1000
                batch_xs, batch_ys = self.get_nn_next_train(self.batchsize, 3)
                self.sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

        if self.save_ckpt and self.train : self.save()

        if self.test :
            correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

            if self.use_loader : self.get_nn_next_test(self.batchsize, 3)
            print(self.sess.run(accuracy, feed_dict={x: self.mnist_test.images, y_: self.mnist_test.labels}))

        if self.predict_softmax :
            self.cursor = 0
            self.dat_remove = []

            out = []
            for i in range(self.start_train, self.cursor_tot + 3) :
                batch_0, batch_1 = self.get_nn_next_predict(self.batchsize, 3)
                y_out = tf.argmax(y,1)
                out.extend( self.sess.run(y_out, feed_dict={x : batch_0, y_: batch_1}))
                print out, len(out) , i, self.cursor_tot

            for j in range(len(out)) :
                zz = out[j]
                if zz == 0 :
                    self.dat_remove.append( j)
            print "remove", self.dat_remove

    def conv_setup(self):
        output = 2
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


        x = tf.placeholder(tf.float32, shape=[None, 784])
        y_ = tf.placeholder(tf.float32, shape=[None, output])


        #self.sess = tf.InteractiveSession()
        W_conv1 = weight_variable([5, 5, 1, 32])
        b_conv1 = bias_variable([32])
        x_image = tf.reshape(x, [-1, 28, 28, 1])
        h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
        h_pool1 = max_pool_2x2(h_conv1)

        W_conv2 = weight_variable([5, 5, 32, 64])
        b_conv2 = bias_variable([64])

        h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
        h_pool2 = max_pool_2x2(h_conv2)

        W_fc1 = weight_variable([7 * 7 * 64, 1024])
        b_fc1 = bias_variable([1024])

        h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

        keep_prob = tf.placeholder(tf.float32)
        h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

        W_fc2 = weight_variable([1024, output])
        b_fc2 = bias_variable([output])

        y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2


        cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y_conv, y_))
        train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
        correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        #init = tf.global_variables_initializer()
        init = tf.initialize_all_variables()
        self.sess.run(init)
        #self.sess.run(tf.initialize_all_variables())

        if self.load_ckpt : self.load()

        if self.train :
            #self.cursor = 0
            for i in range(self.start_train,self.cursor_tot ):
                batch_0, batch_1 = self.get_nn_next_train(self.batchsize)

                if i % 100 == 0:
                    train_accuracy = accuracy.eval(feed_dict={
                        x: batch_0, y_: batch_1, keep_prob: 1.0})
                    print("step %d, training accuracy %g" % (i, train_accuracy))
                train_step.run(feed_dict={x: batch_0, y_: batch_1, keep_prob: 0.5})

        if self.save_ckpt and self.train: self.save()

        if self.test :
            if self.use_loader : self.get_nn_next_test(self.batchsize)
            print("test accuracy %g" % accuracy.eval(feed_dict={
                x: self.mnist_test.images, y_: self.mnist_test.labels, keep_prob: 1.0}))

        if self.predict_conv :
            self.cursor = 0
            self.dat_remove = []

            out = []
            for i in range(self.start_train, self.cursor_tot + 3) :
                batch_0, batch_1 = self.get_nn_next_predict(self.batchsize)
                y_out = tf.argmax(y_conv,1)
                out.extend( self.sess.run(y_out, feed_dict={x : batch_0, y_: batch_1, keep_prob: 0.5}))
                #print out, len(out) , i, self.cursor_tot

            for j in range(len(out)) :
                zz = out[j]
                if zz == 0 :
                    self.dat_remove.append( j)
            #print "remove", self.dat_remove


    def save(self):
        filename = self.save_name
        folder = self.ckpt_folder + os.sep + "ckpt"
        if not os.path.exists(folder) :
            os.makedirs(folder)
        saver = tf.train.Saver()
        save_path = saver.save(self.sess, folder + os.sep + self.ckpt_name + "."+ filename)
        print ("saved?", filename)

    def load(self):
        filename = self.save_name
        file = self.ckpt_folder + os.sep + "ckpt" + os.sep + self.ckpt_name +"."+ filename
        if os.path.isfile(file) :
            saver = tf.train.Saver()
            saver.restore(self.sess, file)
            print ("load?", filename)



    def set_loader(self, load):
        self.loader = load
        self.cursor = 0
        self.use_loader = True

    def set_vars(self, length,  batchsize, name = "", start = 1):
        self.cursor_tot = int(length / batchsize) - 1
        self.save_name = name
        #self.start_train = start
        #self.loader.start_num = start
        self.cursor = start
        #print "vars", self.cursor_tot, self.save_name

    def get_nn_next_predict(self, batchsize, num_channels = 1):
        images, labels = self.loader.get_nn_next_train(batchsize, self.cursor, num_channels)
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
