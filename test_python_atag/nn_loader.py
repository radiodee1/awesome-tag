import numpy as np
from PIL import Image, ImageFile
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
        self.image_x3 = []
        self.image_skin = []
        self.dat = [] ## this is the raw csv data
        #self.dat_subset = []
        self.iter = 0

        ImageFile.LOAD_TRUNCATED_IMAGES = True
        self.inspection_num = 2

        ''' Read csv file '''
        with open(self.csv_input, 'r') as f:
            for line in f:
                self._process_read_line(line)
            f.close()



    def get_mnist_next_train(self, batchsize, cursor, num_channels = 1):
        skin, three, images, lables = self._get_pixels_from_dat(cursor * batchsize, cursor * batchsize + batchsize)
        if num_channels == 1 : return images, lables
        if num_channels == 3 : return three, lables
        if num_channels == 12 : return skin, lables
        return images, lables

    def get_mnist_next_test(self, batchsize, num_channels = 1):
        testframe = 0
        skin, three, images, labels = self._get_pixels_from_dat( testframe * batchsize, testframe * batchsize + batchsize) #len(self.dat) - batchsize, len(self.dat))
        print ("test", len(images), batchsize)
        if num_channels == 1 : self.mnist_test = Map({'images':images, 'labels': labels})
        if num_channels == 3 : self.mnist_test = Map({'images':three, 'labels':labels})
        if num_channels == 12 : self.mnist_test = Map({'images':skin, 'labels': labels})
        return self.mnist_test


    def _get_pixels_from_dat(self, start, stop):
        #print ("work with dat var")
        self.image = []
        self.label = []
        self.image_x3 = []
        self.image_skin = []
        self.iter = start
        while self.iter < stop and stop < len(self.dat) :
            filename = self.image_folder + os.sep + self.dat[self.iter][self.FILE]
            x = self.dat[self.iter][self.FACE_X]
            y = self.dat[self.iter][self.FACE_Y]
            width = self.dat[self.iter][self.FACE_WIDTH]
            height = self.dat[self.iter][self.FACE_HEIGHT]

            if not (os.path.isfile(filename) and width >=28 and height >= 28 and len(Image.open(filename).getbands()) >=3) :
                self.iter = self.iter + 1
                stop = stop + 1
                continue

            lbl_1 = 0
            lbl_2 = 0
            if self.dat[self.iter][self.IS_FACE] == 1:
                lbl_1 = 1
            else:
                lbl_2 = 1

            skin, img , three = self.look_at_img(filename,x,y,width,height)
            #print three, "three"

            print (self.iter, filename)

            if self.inspection_num >= self.iter and False :
                self.print_block(img)
                print "========="
                self.print_block(three[:28*28])
                self.print_block(three[28*28:28*28*2])
                self.print_block(three[28*28*2:])
                print [lbl_1, lbl_2]
                sys.exit()

            self.image.append(img)
            self.image_x3.append(three)
            self.image_skin.append(skin)
            self.label.append([lbl_1,lbl_2])
            self.iter = self.iter + 1
        return self.image_skin, self.image_x3, self.image, self.label

    def _process_read_line(self, line):
        #print line
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
        #img = Image.open(open(filename))
        img = Image.open(filename)

        #img2 = [[0] * 28] * 28
        img2 = [[0] * 28 for _ in range(28)]
        img2 = np.asarray(img2, dtype="float32") ## 'img2' MUST BE A NUMPY ARRAY!!

        img3 = [[0] * 28 for _ in range(28)] #[[0] * 28 ] * 28
        img3 = np.asarray(img3, dtype="float32")

        img_skin = [[0] *3] * 4
        img_skin = np.asarray(img_skin, dtype="float32")

        oneimg = []
        threeimg = []
        skin = []

        mnist_dim = 28

        multx = width / float(mnist_dim)
        multy = height / float(mnist_dim)

        xy_list = []
        dimx, dimy = img.size

        counter = 0

        ''' Put in shrunk form. '''
        if  len (img.getbands()) == 3 :
            if not (x + width > dimx and y + height > dimy) :

                for aa in range(28) :
                    for bb in range(28) :
                        astart = x + aa * multx
                        bstart = y + bb * multy

                        if  astart >= 0 and astart < dimx and bstart >= 0 and bstart < dimy :
                            item = [ aa, bb, list(img.getpixel((int(astart) ,int(bstart))))]
                            xy_list.append(item)
                            counter = counter + 1


        ''' Put list in 28 x 28 array. '''
        if len(xy_list) == 0:
            xy_list = [[0, 0,[0,0,0]]]
        ''' just one color '''
        high = img.getextrema()[0][1] /2
        for i in range(len(xy_list)):
            q = xy_list[i]
            color = q[2][0]
            if color > high : img2[int(q[0]), int(q[1])] =   color

        ''' Then add entire array to oneimg variable and flatten.'''
        for yz in range(28):
            for xz in range(28):
                oneimg.append(img2[yz][xz])

        ''' Three color channels '''
        if len(xy_list) >= 28 * 28 or True:
            img3 = [[0] * 28] * 28
            img3 = np.asarray(img3, dtype="float32")
            high = img.getextrema()[0][1] / 2

            for i in range(len(xy_list)):
                q = xy_list[i]
                color = q[2][0]
                if color > high : img3 [int(q[0]), int(q[1])] = color
            for yz in range(28):
                for xz in range(28):
                    threeimg.append(img3[yz][xz])

            img3 = [[0] * 28] * 28
            img3 = np.asarray(img3, dtype="float32")
            high = img.getextrema()[1][1] / 2

            for i in range(len(xy_list)):
                q = xy_list[i]
                color = q[2][1]
                if color > high : img3 [int(q[0]), int(q[1])] = color
            for yz in range(28):
                for xz in range(28):
                    threeimg.append(img3[yz][xz])

            img3 = [[0] * 28] * 28
            img3 = np.asarray(img3, dtype="float32")
            high = img.getextrema()[2][1] / 2

            for i in range(len(xy_list)):
                q = xy_list[i]
                color = q[2][2]
                if color > high : img3 [int(q[0]), int(q[1])] = color
            for yz in range(28):
                for xz in range(28):
                    threeimg.append(img3[yz][xz])

        ''' Skin tone '''
        for i in range(len(xy_list)):
            q = xy_list[i]
            color = q[2]
            if q[0] == 28 /2 and q[1] == 28/2 : img_skin[0] = color
            if q[0] == 28 /2 +1 and q[1] == 28/2 : img_skin[1] = color
            if q[0] == 28/2 and q[1] == 28/2 + 1 : img_skin[2] = color
            if q[0] == 28 / 2 +1 and q[1] == 28/2 + 1 :img_skin[3] = color

        for i in range(4) :
            skin.extend(list(img_skin[i]))

        return skin, oneimg, threeimg

    def print_block(self, img):
        for x in range(28):
            for y in range(28):
                out = " "
                if img[y * 28 + x] > 200: out = "X"
                out = str(img[x *28 + y]) +" "
                sys.stdout.write(out)
            print ("|")
        print ("---------------")

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