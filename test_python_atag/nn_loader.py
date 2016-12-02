import numpy as np
from PIL import Image
import math
import os
import sys
import atag_csv as enum

class Load(enum.Enum):
    def __init__(self, atag):
        enum.Enum.__init__(self)
        self.mnist_train = {}
        self.mnist_test = {}
        self.load_official_mnist = True
        self.image_folder = atag.VAR_ROOT_DATABASE

        self.csv_input = atag.VAR_LOCAL_DATABASE + os.sep + atag.VAR_MY_CSV_NAME + ".csv"
        self.label = []
        self.image = []
        self.dat = [] ## this is the raw csv data
        #self.dat_subset = []
        self.iter = 0

        self.inspection_num = 0

        #self.dat = []
        #self.iter = 0
        with open(self.csv_input, 'r') as f:
            for line in f:
                self._process_read_line(line)
            f.close()

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

    def get_mnist_next_train(self, batchsize, cursor):
        print batchsize, cursor, "here"
        ##self.dat_subset = self.dat[cursor * batchsize, cursor * batchsize + batchsize]
        images, lables = self._get_pixels_from_dat(cursor * batchsize, cursor * batchsize + batchsize)
        return images, lables

    def get_mnist_next_test(self, batchsize):
        images, labels = self._get_pixels_from_dat( len(self.dat) - batchsize, len(self.dat))
        self.mnist_test = Map({'images':images, 'labels': labels})
        return self.mnist_test

    def get_csv_image_dat(self):
        '''
        self.dat = []
        self.iter = 0
        with open(self.csv_input, 'r') as f:
            for line in f:
                self._process_read_line(line)
            f.close()
        '''
        images, lables = self._get_pixels_from_dat(0, len(self.dat))
        return images, lables

    def _get_pixels_from_dat(self, start, stop):
        print "work with dat var"
        self.image = []
        self.label = []
        self.iter = start
        while self.iter < stop :
            filename = self.image_folder + os.sep + self.dat[self.iter][self.FILE]
            x = self.dat[self.iter][self.FACE_X]
            y = self.dat[self.iter][self.FACE_Y]
            width = self.dat[self.iter][self.FACE_WIDTH]
            height = self.dat[self.iter][self.FACE_HEIGHT]

            if not (os.path.isfile(filename) and width >=28 and height >= 28) :
                self.iter = self.iter + 1
                continue

            img = self.look_at_img(filename,x,y,width,height)

            print self.iter, filename

            if self.inspection_num == self.iter or True :
                self.print_block(img)
                sys.exit()

            lbl_1 = 0
            lbl_2 = 0
            if self.dat[self.iter][self.IS_FACE] == 1: lbl_1 = 1

            self.image.append(img)
            self.label.append([lbl_1,lbl_2])
            self.iter = self.iter + 1
        return self.image, self.label

    def _process_read_line(self, line):
        print line
        row = []
        strings = line.rstrip("\r\n").split(",")
        try:
            int(strings[self.FACE_X]) # are we looking at heading?
        except ValueError:
            return

        for l in range(self.TOTAL):
            if l == self.FILE or l == self.FRAME :
                row.append(strings[l])
            else:
                row.append(int(strings[l]))
        self.dat.append(row)


    def look_at_img(self, filename, x = 0, y = 0, width = 28, height = 28):
        img = Image.open(open(filename))
        size = 28, 28
        img2 = [[0.0 ,0.0 ,0.0] * 28 ]* 28
        oneimg = []

        mnist_dim = 28
        divx = mnist_dim / float(width)
        divy = mnist_dim / float(height)
        #div = 1/div
        #print div
        xy_list = []
        dimx, dimy = img.size
        img = np.asarray(img, dtype='float64')
        print len(img), dimx, dimy, "size", self.iter

        ''' Detect 0 for black -- put in list in shrunk form. '''
        if not len (img.shape) < 3 :
            if not (x + width > dimx and y + height > dimy) :
                for xx in range(x + 0, x + width):
                    for yy in range(y + 0, y + height):
                        #print img[xx,yy,0]
                        if (xx -x ) * divx < dimx  and (yy - y) * divy  < dimy and xx < dimx -1 and yy < dimy -1:
                            #colors = img[xx,yy ] # + 16 * img[xx,yy,1] + 256 * img[xx,yy,2]
                            #print colors , "color"
                            if True or float(img[xx , yy , 0]) < float(205) : ## 255
                                #print img.shape #xx, yy, (xx-x) * divx, (yy -y) * divy, "mags"
                                xy_list.append([int ((xx -x) * divx) , int( (yy-y) * divy), list(img[yy,xx]) ])

        ''' Put list in 28 x 28 array. '''
        if len(xy_list) == 0:
            xy_list = [[0, 0,[0,0,0]]]
            #print "len zero" , filename
        for q in xy_list:
            if (q[0] < 28) and (q[1] < 28) and (q[0] >= 0) and (q[1] >= 0):
                #print q[0], q[1], q[2], q
                #print  img2
                img2[int(math.floor(q[0]))][ int(math.floor(q[1]))] =   q[2][0]
            #else :
            #    print "exception" , q

        ''' Then add entire array to oneimg variable and flatten.'''
        for y in range(28):
            for x in range(28):
                oneimg.append(img2[y][x])

        return oneimg #, oneindex

    def print_block(self, img):
        print len(img)
        for y in range(28):
            for x in range(28):
                out = " "
                #if img[y * 28 + x] > 0: out = "X"
                out = str(img[x *28 + y]) +" "
                sys.stdout.write(out)
            print "|"
        print "---------------"

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