import numpy as np
from PIL import Image, ImageFile
#from resizeimage import resizeimage
import math
import os
import sys
import atag_csv as enum
import nn_record as rec
import nn_dim as dim

class Load(enum.Enum, dim.Dimension):
    def __init__(self, atag, filename, csv_filename=None):
        enum.Enum.__init__(self)
        dim.Dimension.__init__(self)

        self.dim_x = self.DIMENSIONS[self.key][self.COLUMN_XY_CONV][0]
        self.dim_y = self.DIMENSIONS[self.key][self.COLUMN_XY_CONV][1]
        self.pixel_enum = self.DIMENSIONS[self.key][self.COLUMN_LOADTYPE]
        self.dot_xy =int(math.sqrt(self.DIMENSIONS[self.key][self.COLUMN_IN_OUT_DOT][0] / 3))

        self.mnist_train = {}
        self.mnist_test = {}
        self.load_official_mnist = True
        self.image_folder = atag.VAR_ROOT_DATABASE

        self.csv_input = atag.VAR_LOCAL_DATABASE + os.sep + atag.VAR_MY_CSV_NAME + ".csv"
        if csv_filename != None: self.csv_input = csv_filename
        self.label = []
        self.image = []
        self.image_x3 = []
        self.image_skin = []
        self.dat = [] ## this is the raw csv data
        #self.dat_subset = []
        self.iter = 0
        self.start_num = 0
        #self.images_used = 0

        self.filename = filename
        self.filename_old = ""
        self.img = None
        self.crop_resize_special = False
        self.special_horizontal_align = False

        self.record = rec.Record(atag)
        self.normal_train = True

        ImageFile.LOAD_TRUNCATED_IMAGES = True
        self.inspection_num = 2

    def read_csv(self):
        ''' Read csv file '''
        if len(self.filename) == 0 :
            print self.csv_input , " - input file"
            if os.path.isfile(self.csv_input):
                with open(self.csv_input, 'r') as f:
                    for line in f:
                        self._process_read_line(line)
                    f.close()
        else:
            self.dat = self.record.make_boxes(self.filename)


    def get_nn_next_train(self, batchsize, cursor, num_channels = 1):
        if cursor * batchsize + batchsize >= len(self.dat):
            skin, three, images, lables = self._get_pixels_from_dat(cursor * batchsize, len(self.dat) -1 )

        elif cursor * batchsize + batchsize < len(self.dat) :
            skin, three, images, lables = self._get_pixels_from_dat(cursor * batchsize, cursor * batchsize + batchsize)
        if num_channels == self.CONST_ONE_CHANNEL : return images, lables
        if num_channels == self.CONST_THREE_CHANNEL : return three, lables
        if num_channels == self.CONST_DOT : return skin, lables
        return images, lables

    def get_nn_next_test(self, batchsize, num_channels = 1):
        testframe = 0
        skin, three, images, labels = self._get_pixels_from_dat( testframe * batchsize, testframe * batchsize + batchsize) #len(self.dat) - batchsize, len(self.dat))
        print ("next test", len(images), batchsize, testframe)
        if num_channels == self.CONST_ONE_CHANNEL : self.mnist_test = Map({'images':images, 'labels': labels})
        if num_channels == self.CONST_THREE_CHANNEL : self.mnist_test = Map({'images':three, 'labels':labels})
        if num_channels == self.CONST_DOT : self.mnist_test = Map({'images':skin, 'labels': labels})
        return self.mnist_test

    def get_nn_next_predict(self, batchsize, cursor, num_channels = 1):
        self.normal_train = False
        tot_cursors = int(len(self.dat) / batchsize)
        if cursor > tot_cursors  :
            print cursor, tot_cursors, batchsize, len(self.dat), "end"
            skin, three, images, labels = self._get_pixels_from_dat(cursor-1 * batchsize, len(self.dat) )
        elif batchsize > len(self.dat):
            skin, three, images, labels = self._get_pixels_from_dat(0, len(self.dat))
        elif cursor <= tot_cursors :
            skin, three, images, labels = self._get_pixels_from_dat(cursor * batchsize, cursor * batchsize + batchsize)
        if num_channels == self.CONST_ONE_CHANNEL : return images, labels
        if num_channels == self.CONST_THREE_CHANNEL : return three, labels
        if num_channels == self.CONST_DOT : return skin, labels
        return images, labels


    def outside_get_pixels_from_dat(self, filename, chosen):
        print ("work with dat var")
        self.image = []
        self.label = []
        self.image_x3 = []
        self.image_skin = []

        self.line_chosen = chosen

        if True:
            if not filename.startswith(self.image_folder + os.sep) and not (filename.startswith(os.sep)) :
                filename = self.image_folder + os.sep + filename
            x = int(self.line_chosen[self.FACE_X])
            y = int(self.line_chosen[self.FACE_Y])
            width = int(self.line_chosen[self.FACE_WIDTH])
            height = int(self.line_chosen[self.FACE_HEIGHT])

            print " -- " , filename

            ''' open image if it is new! '''
            self.filename = filename
            self.img = Image.open(filename)

            self.special_horizontal_align = True

            skin, img , three = self.look_at_img(filename, x, y, width, height)
            print len(skin), len(img), len(three)
            return skin, img, three

    def _get_pixels_from_dat(self, start, stop):
        print ("work with dat var")
        self.image = []
        self.label = []
        self.image_x3 = []
        self.image_skin = []
        self.iter = start

        if self.iter  > len(self.dat):
            self.iter = 0
            stop = stop - start
            print "some kind of reset"

        while self.iter < stop and stop <= len(self.dat) and self.iter < len(self.dat):
            filename = self.dat[self.iter][self.FILE]
            if not filename.startswith(self.image_folder + os.sep) and not (filename.startswith(os.sep)) :
                filename = self.image_folder + os.sep + filename
            x = self.dat[self.iter][self.FACE_X]
            y = self.dat[self.iter][self.FACE_Y]
            width = self.dat[self.iter][self.FACE_WIDTH]
            height = self.dat[self.iter][self.FACE_HEIGHT]

            if filename != self.filename_old:
                print self.iter, " -- ", int(self.iter / float(len(self.dat)) * 100) , "% -- " , filename, len(self.dat)

            ''' open image if it is new! '''
            self.filename = filename
            if self.filename != self.filename_old:
                self.img = Image.open(filename)
            self.filename_old = self.filename


            if not (os.path.isfile(filename) and width >= self.dim_x and height >= self.dim_y
                    and len(self.img.getbands()) >=3) and self.normal_train :
                self.iter = self.iter + 1
                stop = stop + 1
                print "skipping 1, b-n-w:" , filename
                continue

            lbl_1 = 0
            lbl_2 = 0
            if self.dat[self.iter][self.IS_FACE] == 1:
                lbl_1 = 1
            else:
                lbl_2 = 1

            skin, img , three = self.look_at_img(filename,x,y,width,height)
            #print len(three) , three, "three"

            if (len(img) != self.dim_x * self.dim_y or len(three) != self.dim_x * self.dim_y * 3) and self.normal_train :
                self.iter = self.iter + 1
                stop = stop + 1
                print "skipping 2, output sizes"
                continue

            if self.inspection_num >= self.iter and False :
                self.print_block(img)
                print "========="
                self.print_block(three[:self.dim_x * self.dim_y])
                self.print_block(three[ self.dim_x * self.dim_y : self.dim_x * self.dim_y *2])
                self.print_block(three[ self.dim_x * self.dim_y *2:])
                print [lbl_1, lbl_2]
                sys.exit()

            if True:
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
            if l == self.FILE or l == self.FRAME or l == self.COLOR:
                row.append(strings[l])
            else:
                row.append(int(strings[l]))
        self.dat.append(row)


    def look_at_img(self, filename, x = 0, y = 0, width = -1, height = -1):

        if width == -1 : width = self.dim_x
        if height == -1 : height = self.dim_y

        img2 = [[0] * self.dim_x for _ in range(self.dim_y)]
        img2 = np.asarray(img2, dtype="float32") ## 'img2' MUST BE A NUMPY ARRAY!!


        img_skin = [[0] *3] * self.dot_xy * self.dot_xy
        img_skin = np.asarray(img_skin, dtype="float32")

        oneimg = []
        threeimg = []
        skin = []
        oneimg_rgb = []

        mnist_dim = self.dim_x

        #multx = width / float(mnist_dim)
        multy = height / float(mnist_dim)
        multx = multy
        if width > height: # and not self.special_horizontal_align:
            multx = width / float(mnist_dim)

        xy_list = []
        dimx, dimy = self.img.size

        counter = 0

        ''' center image in x direction '''
        if height > width and self.special_horizontal_align:
            xoffset = int (( width  - self.dim_x * multx) / 2)
            if not (x + xoffset <= 0 or x + xoffset + width > dimx) :
                x = x + xoffset


        ''' Put in shrunk form. '''
        if self.crop_resize_special:
            #self.img.show()
            print x, y, width, height, "dimensions"
            cropped = self.img.crop((x,y,x + width, y + height))
            #cropped.show()
            resize = cropped.resize((self.dim_x, self.dim_y))
            #resize = resizeimage.resize_height(resize, self.dim_y)
            for aa in range(self.dim_x):
                for bb in range(self.dim_y):
                    astart = aa #x + aa * multx
                    bstart = bb #y + bb * multy

                    if astart >= 0 and astart < dimx and bstart >= 0 and bstart < dimy:
                        item = [aa, bb, list(resize.getpixel((int(astart), int(bstart)))[:3])]
                        oneimg_rgb.extend(list(resize.getpixel((int(astart), int(bstart)))[:3]))
                        xy_list.append(item)
                        counter = counter + 1
                    else:
                        item = [aa, bb, list((0.0, 0.0, 0.0))]
                        oneimg_rgb.extend(list((0.0, 0.0, 0.0)))
                        xy_list.append(item)
                        counter = counter + 1

        if not self.crop_resize_special:
            if  len (self.img.getbands()) == 3 :
                if not (x + width > dimx and y + height > dimy) :

                    for aa in range(self.dim_x) :
                        for bb in range(self.dim_y) :
                            astart = x + aa * multx
                            bstart = y + bb * multy


                            if  astart >= 0 and astart < dimx and bstart >= 0 and bstart < dimy :
                                item = [ aa, bb, list(self.img.getpixel((int(astart) ,int(bstart))))]
                                oneimg_rgb.extend(list(self.img.getpixel((int(astart) ,int(bstart)))))
                                xy_list.append(item)
                                counter = counter + 1
                            else:
                                item = [aa, bb, list((0.0, 0.0, 0.0))]
                                oneimg_rgb.extend(list((0.0, 0.0, 0.0)))
                                xy_list.append(item)
                                counter = counter + 1
                else:
                    print "change size??"

        ''' Put list in 28 x 28 array. '''
        if len(xy_list) == 0:
            xy_list = [[0, 0,[0,0,0]]]
        ''' just one color '''
        high = self.img.getextrema()[0][1] /2
        for i in range(len(xy_list)):
            q = xy_list[i]
            color = q[2][0]
            if color > high : img2[int(q[0]), int(q[1])] =   color # / float(high * 2)

        ''' Then add entire array to oneimg variable and flatten.'''
        for yz in range(self.dim_x):
            for xz in range(self.dim_y):
                oneimg.append(img2[yz][xz])

        ''' Three color channels '''
        if self.pixel_enum == self.ENUM_LOAD_CONV_GRADIENT : #False:
            if len(xy_list) >= self.dim_x * self.dim_y or True:
                img3 = [[0] * self.dim_x] * self.dim_y
                img3 = np.asarray(img3, dtype="float32")
                high = self.img.getextrema()[0][1] / 2

                for i in range(len(xy_list)):
                    q = xy_list[i]
                    color = q[2][0]
                    if color > high or True: img3 [int(q[0]), int(q[1])] = color  / float(high * 2)
                for yz in range(self.dim_x):
                    for xz in range(self.dim_y):
                        threeimg.append(img3[yz][xz])

                img3 = [[0] * self.dim_x] * self.dim_y
                img3 = np.asarray(img3, dtype="float32")
                high = self.img.getextrema()[1][1] / 2

                for i in range(len(xy_list)):
                    q = xy_list[i]
                    color = q[2][1]
                    if color > high or True: img3 [int(q[0]), int(q[1])] = color  / float(high * 2)
                for yz in range(self.dim_x):
                    for xz in range(self.dim_y):
                        threeimg.append(img3[yz][xz])

                img3 = [[0] * self.dim_x] * self.dim_y
                img3 = np.asarray(img3, dtype="float32")
                high = self.img.getextrema()[2][1] / 2

                for i in range(len(xy_list)):
                    q = xy_list[i]
                    color = q[2][2]
                    if color > high  or True: img3 [int(q[0]), int(q[1])] = color  / float(high * 2)
                for yz in range(self.dim_x):
                    for xz in range(self.dim_y):
                        threeimg.append(img3[yz][xz])
        else:
            for i in range(len(oneimg_rgb)):
                oneimg_rgb[i] = oneimg_rgb[i] / float(255)
            threeimg = oneimg_rgb

        ''' Skin tone '''
        for i in range(len(xy_list)):
            q = xy_list[i]
            color = q[2]
            if True:
                if q[0] == 0 and q[1] == 0 and len(img_skin) >= 1: img_skin[0] = color #/ float(255)
                if q[0] == 1 and q[1] == 0 and len(img_skin) >= 2: img_skin[1] = color #/ float(255)
                if q[0] == 2 and q[1] == 0 and len(img_skin) >= 3: img_skin[2] = color #/ float(255)
                if q[0] == 3 and q[1] == 0 and len(img_skin) >= 4: img_skin[3] = color #/ float(255)
            if False:
                if q[0] == 0 and q[1] == 0 and len(img_skin) >= 1: img_skin[0] = color #/ float(255)
                if q[0] == 1 and q[1] == 0 and len(img_skin) >= 2: img_skin[1] = color #/ float(255)
                if q[0] == 0 and q[1] == 1 and len(img_skin) >= 3: img_skin[2] = color #/ float(255)
                if q[0] == 1 and q[1] == 1 and len(img_skin) >= 4: img_skin[3] = color #/ float(255)


        for i in range(int(self.dot_xy * self.dot_xy)): #len(img_skin)) :
            skin.extend(list(img_skin[i]))

        for s in range(len(skin)):
            skin[s] = skin[s] / float(127)

        #print skin

        return skin, oneimg, threeimg

    def print_block(self, img):
        for x in range(self.dim_x):
            for y in range(self.dim_y):
                out = " "
                if img[y * self.dim_x + x] > 200: out = "X"
                out = str(img[x * self.dim_x + y]) +" "
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