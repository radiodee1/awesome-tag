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
        self.train = True
        self.test = True
        self.load_ckpt = True
        self.save_ckpt = False
        self.sess = tf.Session() #None
        self.mnist = []#input_data.read_data_sets("MNIST_data/", one_hot=True)
        self.mnist_train = []
        self.mnist_test = []

        self.cursor = 0
        self.cursor_tot = 0
        self.batchsize = 100

    def color_setup(self):
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


    def set_mnist_train_test(self, valtrain = None, valtest = None):

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
