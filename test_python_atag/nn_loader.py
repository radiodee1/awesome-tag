import numpy as np
from PIL import Image
import math

class Load(object):
    def __init__(self, atag):
        self.csv_filename = ""
        self.mnist_train = {}
        self.mnist_test = {}
        self.load_official_mnist = True

    def get_mnist_dat(self):
        from tensorflow.examples.tutorials.mnist import input_data


        train = [0] * 784
        test = [0] * 784
        labels = [0] * 10

        train = [train * 200]
        test = [test]
        labels_train = [labels * 200]
        train = np.reshape(train, (-1,784))
        labels = [labels]
        labels_train = np.reshape(labels_train, (-1, 10))

        self.mnist_train = Map({'images':train, 'labels': labels_train})
        self.mnist_test = Map({'images':test, 'labels': labels})

        if self.load_official_mnist :
            mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
            self.mnist_train = mnist.train
            self.mnist_test = mnist.test

        print self.mnist_train
        return self.mnist_train, self.mnist_test

    def look_at_img(self, filename, i=0, load_type=0):
        img = Image.open(open(filename))
        size = 28, 28
        img2 = np.zeros(shape=(size), dtype='float64')
        oneimg = []
        oneindex = i
        xy_list = []

        img = np.asarray(img, dtype='float64')
        marker = 0
        ''' Detect 0 for black -- put in list in shrunk form. '''
        for x in range(0, len(img)):
            for y in range(0, len(img)):
                if (float(img[x, y, 0]) < 255) is True:
                    xy_list.append([x * 1 / float(2) - 18, y * 1 / float(2) - 18])

        ''' Put list in 28 x 28 array. '''
        if len(xy_list) == 0:
            xy_list = [0, 0]
        for q in xy_list:
            if (q[0] < 28) and (q[1] < 28) and (q[0] >= 0) and (q[1] >= 0):
                # print (q[0], q[1])
                img2[int(math.floor(q[0])), int(math.floor(q[1]))] = 1

        ''' Then add entire array to oneimg variable and flatten.'''
        for x in range(28):
            for y in range(28):
                oneimg.append(img2[x, y])

        ''' Get the image ascii number from the filename. '''
        #oneindex, unused = get_number(filename, load_type)
        return oneimg #, oneindex


class Map(dict):

    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.iteritems():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.iteritems():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]