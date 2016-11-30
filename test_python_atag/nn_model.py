#!/usr/bin/python
import os
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
        #self.sess = tf.Session() #None
        self.sess = tf.InteractiveSession()
        self.mnist = []#input_data.read_data_sets("MNIST_data/", one_hot=True)
        self.mnist_train = []
        self.mnist_test = []

        self.cursor = 0
        self.cursor_tot = 0
        self.batchsize = 100

    def mnist_setup(self):

        x = tf.placeholder(tf.float32, [None, 784])
        W = tf.Variable(tf.zeros([784, 10]))
        b = tf.Variable(tf.zeros([10]))

        y = tf.nn.softmax(tf.matmul(x, W) + b)

        y_ = tf.placeholder(tf.float32, [None, 10])

        cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y, y_))

        train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
        init = tf.initialize_all_variables()
        #self.sess = tf.Session()
        self.sess.run(init)

        if self.load_ckpt : self.load()

        if self.train :
            self.cursor = 0
            for i in range(self.cursor_tot): #1000
                batch_xs, batch_ys = self.get_mnist_next_train(self.batchsize)#self.mnist_train.next_batch(100)
                self.sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

        if self.save_ckpt : self.save()

        if self.test :
            correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

            print(self.sess.run(accuracy, feed_dict={x: self.mnist_test.images, y_: self.mnist_test.labels}))

    def conv_setup(self):
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

        #from tensorflow.examples.tutorials.mnist import input_data
        #mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
        #import tensorflow as tf
        x = tf.placeholder(tf.float32, shape=[None, 784])
        y_ = tf.placeholder(tf.float32, shape=[None, 10])


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

        W_fc2 = weight_variable([1024, 10])
        b_fc2 = bias_variable([10])

        y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2

        if self.load_ckpt : self.load()

        cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y_conv, y_))
        train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
        correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        self.sess.run(tf.initialize_all_variables())

        if self.train :
            for i in range(self.cursor_tot):
                #batch = mnist.train.next_batch(50)
                batch_0, batch_1 = self.get_mnist_next_train(self.batchsize)
                if i % 100 == 0:
                    train_accuracy = accuracy.eval(feed_dict={
                        x: batch_0, y_: batch_1, keep_prob: 1.0})
                    print("step %d, training accuracy %g" % (i, train_accuracy))
                train_step.run(feed_dict={x: batch_0, y_: batch_1, keep_prob: 0.5})

        if self.save_ckpt : self.save()

        if self.test :
            print("test accuracy %g" % accuracy.eval(feed_dict={
                x: self.mnist_test.images, y_: self.mnist_test.labels, keep_prob: 1.0}))

    def save(self):
        folder = self.ckpt_folder + os.sep + "ckpt"
        if not os.path.exists(folder) :
            os.makedirs(folder)
        saver = tf.train.Saver()
        save_path = saver.save(self.sess, folder + os.sep + self.ckpt_name + ".ckpt")
        print "saved?"

    def load(self):
        file = self.ckpt_folder + os.sep + "ckpt" + os.sep + self.ckpt_name + ".ckpt"
        if os.path.isfile(file) :
            saver = tf.train.Saver()
            saver.restore(self.sess, file)
        print "load?"


    def set_mnist_train_test(self, valtrain = None, valtest = None, batchsize = 50):
        self.batchsize = batchsize

        if valtrain != None:
            self.mnist_train = valtrain
            self.cursor_tot = int(len(self.mnist_train.images) / self.batchsize)
        else:
            self.mnist_train = input_data.read_data_sets("MNIST_data/", one_hot=True).train

        if valtest != None:
            self.mnist_test = valtest
        else:
            self.mnist_test = input_data.read_data_sets("MNIST_data/", one_hot=True).test
        print "in"

    def get_mnist_next_train(self, batchsize):

        images = self.mnist_train.images[self.cursor * batchsize : self.cursor * batchsize + batchsize]
        lables = self.mnist_train.labels[self.cursor * batchsize : self.cursor * batchsize + batchsize]
        self.cursor = self.cursor + 1
        #print lables, "lables"
        return  images, lables
