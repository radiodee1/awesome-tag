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

class NN(enum.Enum):
    def __init__(self, atag):
        enum.Enum.__init__(self)

        self.a = atag
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
        self.dat_len = 0
        self.save_name = ""
        self.start_train = 1

        self.predict_skintone = False
        self.predict_softmax = False
        self.predict_conv = False
        self.predict_dot = False

        self.dat_remove = []
        self.dat_best = []

        self.dot_only = False
        self.conv_only = False

        self.nn_out_skintone = None
        self.nn_out_softmax = None
        self.nn_out_conv = None

        self.group_initialize = False
        self.predict_remove_symbol = 1 ## 1 or 0 ??

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
        self.d_b_1 = tf.Variable(tf.zeros([output_num]))

        # y_mid = tf.nn.relu(tf.matmul(x,W_1) + b_1)
        #self.d_y_mid = tf.nn.relu(tf.matmul(self.d_x, self.d_W_1) + self.d_b_1)

        #self.d_W_2 = tf.Variable(tf.random_normal([mid_num, output_num], stddev=0.0001))
        #self.d_b_2 = tf.Variable(tf.random_normal([output_num], stddev=0.5))

        self.d_y_logits = tf.matmul(self.d_x, self.d_W_1) + self.d_b_1
        self.d_y = tf.nn.softmax(self.d_y_logits)

        self.d_y_ = tf.placeholder(tf.float32, [None, output_num])

        # cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
        self.d_cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(self.d_y_logits, self.d_y_))

        self.d_train_step = tf.train.GradientDescentOptimizer(0.001).minimize(self.d_cross_entropy)  # 0.0001
        # train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy) #0.5

        self.d_y_out = tf.argmax(self.d_y, 1)  ## for prediction


        ''' CONVOLUTION NEXT '''
        c_output = 2
        c_input = 784 * 3

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

        self.W_conv1 = weight_variable([5, 5, 3, 32])
        self.b_conv1 = bias_variable([32])
        self.x_image = tf.reshape(self.c_x, [-1, 28, 28  , 3])
        self.h_conv1 = tf.nn.relu(conv2d(self.x_image, self.W_conv1) + self.b_conv1)
        self.h_pool1 = max_pool_2x2(self.h_conv1)

        self.W_conv2 = weight_variable([5, 5, 32, 64])
        self.b_conv2 = bias_variable([64])

        self.h_conv2 = tf.nn.relu(conv2d(self.h_pool1, self.W_conv2) + self.b_conv2)
        self.h_pool2 = max_pool_2x2(self.h_conv2)

        self.W_fc1 = weight_variable([7 * 7 * 64, 1024])
        self.b_fc1 = bias_variable([1024])

        self.h_pool2_flat = tf.reshape(self.h_pool2, [-1, 7 * 7 * 64 ])
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
            self.dot_only = True
            self.cursor = self.load_cursor(self.a.FOLDER_SAVED_CURSOR_DOT)

            for i in range(self.start_train,self.cursor_tot): #1000
                batch_xs, batch_ys = self.get_nn_next_train(self.batchsize, self.CONST_DOT)
                self.sess.run(self.d_train_step, feed_dict={self.d_x: batch_xs, self.d_y_: batch_ys})

        if self.save_ckpt and self.train : self.save_group()

        if self.test :
            self.cursor = 0
            d_correct_prediction = tf.equal(tf.argmax(self.d_y,1), tf.argmax(self.d_y_,1))
            d_accuracy = tf.reduce_mean(tf.cast(d_correct_prediction, tf.float32))

            if self.use_loader : self.get_nn_next_test(self.batchsize, self.CONST_DOT)
            print(self.sess.run(d_accuracy, feed_dict={self.d_x: self.mnist_test.images, self.d_y_: self.mnist_test.labels}))

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
                print stop

            for i in range(start, stop ) :
                batch_0, batch_1 = self.get_nn_next_predict(self.batchsize, self.CONST_DOT)
                print "batch_0", len(batch_0)
                if len(batch_0) > 0 :
                    out.extend( self.sess.run(self.d_y_out, feed_dict={self.d_x : batch_0, self.d_y_: batch_1}))
                    print "out" , len(out) , i, self.cursor_tot, out[:10],"..."

            for j in range(len(out)) :
                zz = out[j]
                if int(zz) == int(self.predict_remove_symbol ) : ## 1
                    self.dat_remove.append( j )

            print "remove dot", len(self.dat_remove), self.dat_remove
            self.loader.record.remove_lines_from_dat(self.dat_remove)
            self.loader.record.renumber_dat_list(self.loader.dat)


    def conv_setup(self):


        if self.load_ckpt : self.load_group()

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

        if self.save_ckpt and self.train  : self.save_group()

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
                    #print batch_0
                    out.extend( self.sess.run(self.c_y_out, feed_dict={self.c_x : batch_0, self.c_y_: batch_1, self.keep_prob: 1.0}))
                    #print out, len(out) , i, self.cursor_tot

            for j in range(len(out)) :
                zz = out[j]
                if int(zz) == int(self.predict_remove_symbol ) : ## 1
                    self.dat_remove.append( j)

            self.loader.record.remove_lines_from_dat(self.dat_remove)
            self.loader.dat = self.loader.record.renumber_dat_list(self.loader.dat)
            print "remove conv", self.dat_remove[:10],"..."

        #self.sess.close()
    def conv_setup_mc(self):
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
                    #print batch_0
                    out.extend( self.sess.run(self.y_conv, feed_dict={self.c_x : batch_0, self.c_y_: batch_1, self.keep_prob: 1.0}))
                    #print out, len(out) , i, self.cursor_tot

            if True:
                print "out", len(out)
                numlow = 0.5
                numhigh = 0.5
                numhigh_index = 0
                for j in range(len(out)) :
                    zz = out[j][0]
                    if float(zz) < numlow : # int(self.predict_remove_symbol ) : ## 1
                        numlow = zz
                        self.dat_remove.append( j)
                    if float(zz) > numhigh:
                        numhigh = zz
                        numhigh_index = j

                self.dat_best.append(self.loader.dat[numhigh_index])


            print out [:3], "..."
            #self.loader.record.remove_lines_from_dat(self.dat_remove)
            #self.loader.dat = self.loader.record.renumber_dat_list(self.loader.dat)
            #print "remove conv mc", self.dat_remove
            print "best conv mc", self.dat_best[:]

    def conv_weight_img(self):
        if self.load_ckpt : self.load_group()
        filename2 = self.ckpt_folder + os.sep+ "visualize_weights.bmp"
        filename = self.ckpt_folder + os.sep + "visualize_weights_alternate.bmp"
        filename3 = self.ckpt_folder + os.sep + "visualize_weights_skintone.bmp"
        weights = self.sess.run(self.W_conv1)
        skin = self.sess.run(self.d_W_1)
        show1 = False
        show2 = True
        show3 = True
        size = (5*8* 10,5*4*2*10)
        size2 = (5*8*10, 5 * 4* 10)
        size3 = (2* 50 * 3, 2* 50)
        img = Image.new("RGBA", size, color=0)
        img2 = Image.new("RGBA", size2, color=0)
        img3 = Image.new("RGBA", size3, color=0)
        xy = (0,0)
        xy2 = (0,0)
        xy3 = (0,0)
        rgba = (0,0,0,0)
        rgba2 = (0,0,0,0)
        rgba3 = (0,0,0,0)
        if True:
            for i in range(5):
                for j in range(5):
                    for k in range(8):
                        for m in range(4 ):
                            for n in range(2):
                                for p in range(10):
                                    for q in range(10):
                                        pass
                                        if show1:
                                            xy = ((i *8+  k) * 10 + p   , (j *4  +m  )  * 10 *2 + n * 10 + q)
                                            r = weights[i][j][0][k*4+m] * 255.0 * math.pow(10,3)
                                            g = weights[i][j][1][k*4+m] * 255.0 * math.pow(10,3)
                                            b = weights[i][j][2][k*4+m] * 255.0 * math.pow(10,3)
                                            if r > 255: r = 255
                                            if g > 255: g = 255
                                            if b > 255: b = 255
                                            if r < 0: r = 0
                                            if g < 0: g = 0
                                            if b < 0: b = 0
                                            rgba = (int(r),int(g),int(b),0)
                                            if (q == 0 and m == 0 and n == 0) or (k == 0 and p == 0):
                                                rgba = (255, 255, 255, 0)
                                            img.putpixel(xy,rgba)

                                        if show2:
                                            xy2 = ((k * 5 + i) * 10 + p  , (m*n * 5 + j) * 10 * n + q )
                                            rr = weights[i][j][0][k * 4 + m] * 255.0 * math.pow(10, 3)
                                            gg = weights[i][j][1][k * 4 + m] * 255.0 * math.pow(10, 3)
                                            bb = weights[i][j][2][k * 4 + m] * 255.0 * math.pow(10, 3)
                                            if rr > 255: rr = 255
                                            if gg > 255: gg = 255
                                            if bb > 255: bb = 255
                                            if rr < 0: rr = 0
                                            if gg < 0: gg = 0
                                            if bb < 0: bb = 0
                                            rgba2 = (int(rr),int(gg),int(bb),0)

                                            if (k != 0 and i == 0 and p == 0) or ( m != 0 and j == 0 and q == 0) :
                                                rgba2 = (255,255,255,0)
                                            img2.putpixel(xy2, rgba2)

        #print weights
        if True:
            index = 0
            for index in range(3):
                for i in range(2):
                    for j in range(2):
                        for m in range(50):
                            for n in range(50):
                                xy3 = ((i*1) * 50 + m + index * 50 * 2, (j * 1) * 50 + n)
                                if index < 2:
                                    rr = (skin[(j * 2 + i) * 3 + 0][index] + 1.0) * 255.0 * math.pow(10, 0)
                                    gg = (skin[(j * 2 + i) * 3 + 1][index] + 1.0) * 255.0 * math.pow(10, 0)
                                    bb = (skin[(j * 2 + i) * 3 + 2][index] + 1.0) * 255.0 * math.pow(10, 0)
                                    if m == 0 and n == 0 :print rr,gg,bb
                                else:
                                    r1 = (skin[(j * 2 + i) * 3 + 0][0] + 0.0)# * 255.0 * math.pow(10, 1)
                                    g1 = (skin[(j * 2 + i) * 3 + 1][0] + 0.0)# * 255.0 * math.pow(10, 1)
                                    b1 = (skin[(j * 2 + i) * 3 + 2][0] + 0.0)# * 255.0 * math.pow(10, 1)
                                    r2 = (skin[(j * 2 + i) * 3 + 0][1] + 0.0)# * 255.0 * math.pow(10, 1)
                                    g2 = (skin[(j * 2 + i) * 3 + 1][1] + 0.0)# * 255.0 * math.pow(10, 1)
                                    b2 = (skin[(j * 2 + i) * 3 + 2][1] + 0.0)# * 255.0 * math.pow(10, 1)
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

    def save_group(self):
        filename = "group" # self.save_name
        #self.ckpt_name = filename
        folder = self.ckpt_folder + os.sep + "ckpt"
        if not os.path.exists(folder) :
            os.makedirs(folder)
        saver = tf.train.Saver()
        save_path = saver.save(self.sess, folder + os.sep + self.ckpt_name + "."+ filename)
        if self.train:
            if self.conv_only:
                self.a.dot_write(self.a.FOLDER_SAVED_CURSOR_CONV,str(self.cursor))
                pass
            elif self.dot_only:
                self.a.dot_write(self.a.FOLDER_SAVED_CURSOR_DOT, str(self.cursor))
                pass

        print ("saved?", filename)

    def load_group(self):
        filename = "group"
        #self.ckpt_name = filename
        file = self.ckpt_folder + os.sep + "ckpt" + os.sep + self.ckpt_name + "." + filename
        if os.path.isfile(file):
            saver = tf.train.Saver()
            saver.restore(self.sess, file)
            print ("load?", filename)

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

    def set_vars(self, length,  batchsize, start = 1):
        self.batchsize = batchsize
        self.dat_len = length
        self.cursor_tot = int(length / batchsize) ## -1
        self.save_name = "group-miss"
        #self.start_train = start
        #self.loader.start_num = start
        self.cursor = start
        #print "vars", self.cursor_tot, self.save_name

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
                self.cursor = 0
                self.save_group()
                print "exit at end"
                sys.exit()

            self.cursor = self.cursor + 1

        #print lables, "lables"
        return  images, lables

    def get_nn_next_test(self, batchsize, num_channels = 1):
        #print ("test", self.cursor_tot, num_channels)
        self.mnist_test = self.loader.get_nn_next_test(batchsize, num_channels)
