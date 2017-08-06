import os
import random
import atag_csv as enum
from PIL import Image
import sys
import nn_dim as dim
import math

'''
Here we read the split file and write our own csv file for training later on.
'''

class Write( enum.Enum, dim.Dimension) :
    def __init__(self, atag):
        enum.Enum.__init__(self)
        dim.Dimension.__init__(self)

        self.random_dark_false_dot = False

        self.dim_x = self.DIMENSIONS[self.key][self.COLUMN_XY_CONV][0]
        self.dim_y = self.DIMENSIONS[self.key][self.COLUMN_XY_CONV][1]

        self.dat = []

        self.a = atag
        self.csvnum = atag.VAR_SPLIT_CURRENT
        self.csvfolder = atag.VAR_SPLIT_FOLDER_NAME
        self.csvname = 'train_'
        self.csvend = '.csv'

        self.csvfolder = self.csvfolder[: -1]
        if self.csvfolder.endswith('1') : self.csvfolder = self.csvfolder[: -1]

        self.csv_input = self.csvfolder + self.csvnum + os.sep + self.csvname + self.csvnum + self.csvend
        print self.csv_input + '\n'

        self.csv_output = atag.VAR_LOCAL_DATABASE + os.sep + atag.VAR_MY_CSV_NAME + ".csv"
        self.csv_output_dot = atag.VAR_LOCAL_DATABASE + os.sep + atag.VAR_MY_CSV_NAME +".dot.csv"
        self.csv_output_eye = atag.VAR_LOCAL_DATABASE + os.sep + atag.VAR_MY_CSV_NAME +".eye.csv"


        with open(self.csv_input, 'r') as f:
            for line in f:
                self.process_read_line(line)
            f.close()

        print self.csv_input, "input file"
        print self.csv_output, "output file"
        self.f = open(self.csv_output, "w")
        self.f = open(self.csv_output, "a")

        for l in self.dat :
            self.process_write_line(l, filter_yaw=False)
        self.f.close()

        #exit()
        print self.csv_output_dot , "dotfile"
        print "wait... this could take time."
        self.f = open(self.csv_output_dot, "w")
        self.f = open(self.csv_output_dot, "a")

        d = 0
        for l in self.dat:
            d += 1
            print "dot... this could take time. -- ", int(float(d)/len(self.dat) * 100) , "%"
            self.process_write_line_for_dot(l)
        self.f.close()

        print self.csv_output_eye, "eyefile"
        print "wait... this could take time."
        self.f = open(self.csv_output_eye, "w")
        self.f = open(self.csv_output_eye, "a")

        d = 0
        for l in self.dat:
            d += 1
            print "eyes... this could take time. -- ", int(float(d) / len(self.dat) * 100), "%"
            self.process_write_line_for_eye(l)
        self.f.close()

        print "done"

    def process_read_line(self, line):
        l = line.split(",")
        z = []
        for x in l:
            x = x.rstrip("\n\r")
            z.append(x)
        self.dat.append(z)
        print z, "strip"

    def process_write_line(self, line, filter_yaw=False):

        filename = line[self.FILE]
        if not filename.startswith(self.a.VAR_ROOT_DATABASE + os.sep) :
            filename = self.a.VAR_ROOT_DATABASE + os.sep + line[self.FILE]

        if not os.path.isfile(filename) : return

        dimx = 1
        dimy = 1
        #i = Image.open(filename)

        try:
            #print filename, "try Image.open()"
            if True : dimx, dimy = Image.open(filename).size # get image bounds... slow!!
            if dimy == 0 or dimx == 0 : return
        except:
            print "bad jpg " + filename
            return

        try:
            int(line[self.FACE_X]) # are we looking at heading?
        except ValueError:
            return

        left = int(math.floor(float(line[self.FACE_X])))
        right = int(math.floor(float(line[self.FACE_X]))) + int(math.floor(float(line[self.FACE_WIDTH])))
        top = int(math.floor(float(line[self.FACE_Y])))
        bottom = int(math.floor(float(line[self.FACE_Y]))) + int(math.floor(float(line[self.FACE_HEIGHT])))
        width = int(math.floor(float(line[self.FACE_WIDTH])))
        height = int(math.floor(float(line[self.FACE_HEIGHT])))

        yaw = 3.5
        has_yaw = False
        if len(line) > self.FACE_YAW:
            if len(line[self.FACE_YAW]) == 0:
                line[self.FACE_YAW] = yaw
            else:
                yaw = float(line[self.FACE_YAW])
                has_yaw = True
            #print yaw, line[self.FILE]

        if filter_yaw and (yaw < - 4.0 or yaw > 4.0): # don't know what values to use here!!
            #print "X"
            return

        for y in range(2): #3 # values of 2 or 3 are valid

            for x in range(self.TOTAL_READ):
                if y == 0  :
                    if x != self.FILE and len(line[x]) > 0:
                        #print line, x
                        self.f.write(str(int(math.floor(float(line[x])))))
                    elif len(line[x]) == 0:
                        self.f.write("0")
                    else:
                        self.f.write(line[x])

                elif (y == 1 or y == 2) and x == self.FACE_X:
                    r = 0
                    if left + width < dimx : r = random.randint(0,dimx - width) # somewhere on top
                    self.f.write(str(r))
                elif (y == 1 or y == 2) and x == self.FACE_Y:
                    r = 0
                    #g = 0

                    #if top - height <= 0 : g = 0 - (top - height)
                    if top - height > 0 : r = random.randint(0, top - height)
                    self.f.write(str(r))
                else:
                    if x != self.FILE and len(line[x]) > 0:
                        self.f.write(str(int(math.floor(float(line[x])))))
                    elif len(line[x]) == 0:
                        self.f.write("0")
                    else:
                        self.f.write(line[x])

                if x < self.TOTAL_READ - 1:
                    self.f.write(",")
                elif y == 0 :
                    #true
                    self.f.write(","+ self.RED+",1,0\n")
                elif (y == 1 or y == 2):
                    #false
                    self.f.write(","+self.RED+",0,0\n")

    def process_write_line_for_eye(self, line, filter_yaw=False):

        filename = line[self.FILE]
        if not filename.startswith(self.a.VAR_ROOT_DATABASE + os.sep) :
            filename = self.a.VAR_ROOT_DATABASE + os.sep + line[self.FILE]

        if not os.path.isfile(filename) : return

        dimx = 1
        dimy = 1
        #i = Image.open(filename)

        try:
            #print filename, "try Image.open()"
            if True : dimx, dimy = Image.open(filename).size # get image bounds... slow!!
            if dimy == 0 or dimx == 0 : return
        except:
            print "bad jpg " + filename
            return

        try:
            int(line[self.FACE_X]) # are we looking at heading?
        except ValueError:
            return

        left = int(math.floor(float(line[self.FACE_X])))
        #right = int(math.floor(float(line[self.FACE_X]))) + int(math.floor(float(line[self.FACE_WIDTH])))
        top = int(math.floor(float(line[self.FACE_Y])))
        #bottom = int(math.floor(float(line[self.FACE_Y]))) + int(math.floor(float(line[self.FACE_HEIGHT])))
        width = int(math.floor(float(line[self.FACE_WIDTH])))
        height = int(math.floor(float(line[self.FACE_HEIGHT])))

        if len(line[self.RIGHT_EYE_Y]) == 0 or len(line[self.LEFT_EYE_Y]) == 0:
            right_eye_y = top + 13
            left_eye_y = top + 13
        else:

            #print line,"line", line[self.RIGHT_EYE_X], "right eye x"

            #right_eye_x = int(math.floor(float(line[self.RIGHT_EYE_X])))
            right_eye_y = int(math.floor(float(line[self.RIGHT_EYE_Y])))
            #left_eye_x = int(math.floor(float(line[self.LEFT_EYE_X])))
            left_eye_y = int(math.floor(float(line[self.LEFT_EYE_Y])))

        avg_eye_y = int((right_eye_y + left_eye_y ) /2) - 6 ## very magic numbery

        line[self.FACE_Y] = avg_eye_y

        yaw = 3.5
        has_yaw = False
        if len(line) > self.FACE_YAW:
            if line[self.FACE_YAW] == "" or  len(str(line[self.FACE_YAW])) == 0:
                line[self.FACE_YAW] = yaw
            else:
                yaw = float(line[self.FACE_YAW])
                has_yaw = True
            #print yaw, line[self.FILE]

        if filter_yaw and (yaw < - 4.0 or yaw > 4.0): # don't know what values to use here!!
            #print "X"
            return

        for y in range(2): #3 # values of 2 or 3 are valid

            for x in range(self.TOTAL_READ):
                if y == 0  :
                    if x != self.FILE and len(str(line[x])) > 0:
                        #print line, x
                        self.f.write(str(int(math.floor(float(line[x])))))
                    elif len(line[x]) == 0:
                        self.f.write("0")
                    else:
                        self.f.write(line[x])

                elif (y == 1 or y == 2) and x == self.FACE_X:
                    r = 0
                    if left + width < dimx : r = random.randint(0,dimx - width) # somewhere on top
                    self.f.write(str(r))
                elif (y == 1 or y == 2) and x == self.FACE_Y:
                    r = 0
                    #g = 0

                    #if top - height <= 0 : g = 0 - (top - height)
                    if top - height > 0 : r = random.randint(0, top - height)
                    self.f.write(str(r))
                else:
                    if x != self.FILE and len(line[x]) > 0:
                        self.f.write(str(int(math.floor(float(line[x])))))
                    elif len(line[x]) == 0:
                        self.f.write("0")
                    else:
                        self.f.write(line[x])

                if x < self.TOTAL_READ - 1:
                    self.f.write(",")
                elif y == 0 :
                    #true
                    self.f.write(","+ self.RED+",1,0\n")
                elif (y == 1 or y == 2):
                    #false
                    self.f.write(","+self.RED+",0,0\n")

    def process_write_line_for_dot(self, line):
        #space = 25
        #space = self.dim_y / 2 # - 3
        filename = line[self.FILE]
        if not filename.startswith(self.a.VAR_ROOT_DATABASE + os.sep):
            filename = self.a.VAR_ROOT_DATABASE + os.sep + line[self.FILE]

        if not os.path.isfile(filename): return


        try:
            if True: dimx, dimy = Image.open(filename).size  # get image bounds... slow!!
            if dimy == 0 or dimx == 0: return
        except:
            return

        try:
            int(line[self.FACE_X])  # are we looking at heading?
        except ValueError:
            return



        left = int(math.floor(float(line[self.FACE_X])))
        right = int(math.floor(float(line[self.FACE_X]))) + int(math.floor(float(line[self.FACE_WIDTH])))
        top = int(math.floor(float(line[self.FACE_Y])))
        bottom = int(math.floor(float(line[self.FACE_Y]))) + int(math.floor(float(line[self.FACE_HEIGHT])))
        width = int(math.floor(float(line[self.FACE_WIDTH])))
        height = int(math.floor(float(line[self.FACE_HEIGHT])))

        rx = 0
        ry = 0

        space = width / 2
        num_repeated_samples = 1 # 5
        if self.random_dark_false_dot:
            num_repeated_samples = 2

        for z in range(num_repeated_samples):
            for y in range(2):  # 3 # values of 2 or 3 are valid
                if self.random_dark_false_dot and z == 1:
                    rx, ry = self._get_false_dot_xy(filename, x=dimx, y=dimy)
                for x in range(self.TOTAL_READ):
                    if y % 2 == 0:
                        if x != self.FACE_X and x != self.FACE_Y  and x != self.FACE_HEIGHT and x != self.FACE_WIDTH:
                            self.f.write(line[x])
                        #else:
                        #    self.f.write(line[x])
                        if x == self.FACE_X:
                            self.f.write(str(int(math.floor(float(line[x]))) + z * 2 + space))
                        elif x == self.FACE_Y:
                            self.f.write(str(int(math.floor(float(line[x]))) + z * 2 + space))
                        elif x == self.FACE_WIDTH or x == self.FACE_HEIGHT:
                            self.f.write(str(self.dim_x))

                    elif (y % 2 == 1 ) and x == self.FACE_X:
                        r = 0
                        if left + width < dimx: r = random.randint(0, dimx - width)  # somewhere on top
                        if self.random_dark_false_dot and z == 1:
                            r = rx
                        self.f.write(str(r))
                    elif (y % 2 == 1 ) and x == self.FACE_Y:
                        r = 0
                        if top - height > 0: r = random.randint(0, top - height)
                        if self.random_dark_false_dot and z == 1:
                            r = ry
                        self.f.write(str(r))
                    elif (y % 2 == 1) and (x == self.FACE_WIDTH or x == self.FACE_HEIGHT):
                        self.f.write(str(self.dim_y))
                    else :
                        self.f.write(line[x])

                    if x < self.TOTAL_READ - 1:
                        self.f.write(",")
                    elif y % 2 == 0:
                        # true
                        self.f.write("," + self.RED + ",1,0\n")
                    elif (y % 2 == 1 ):
                        # false
                        self.f.write("," + self.RED + ",0,0\n")

    def _get_false_dot_xy(self, filename, x=0, y=0):
        try:
            img = Image.open(filename)
            #x, y = img.size()
            for z in range(20):
                rx = random.randint(0,x-1)
                ry = random.randint(0,y-1)
                pixel = img.getpixel((rx,ry))
                #print pixel
                if len(pixel) >= 3 and pixel[0] < 128 and pixel[1] < 128 and pixel[2] < 128:
                    return rx,ry
                    pass
                else:
                    #return rx, ry
                    pass
            return int(x/2) , int(y/2)
        except:
            print "some error"
            return int(x/2), int(y/2)