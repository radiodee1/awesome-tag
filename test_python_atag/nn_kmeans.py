import random
import os
import atag_csv as enum
from PIL import Image
import math
import sys

class Kmeans(enum.Enum):
    def __init__(self, atag):
        enum.Enum.__init__(self)

        self.image_folder = atag.VAR_ROOT_DATABASE

        self.num_centroids = 3
        self.cent = []
        self.cent_old = []
        '''
        for i in range(self.num_centroids):
            self.cent.append([0,0])
        print self.cent
        '''
        self.dat = []
        self.show_all_boxes = False

    def do_km(self, dat, num_centroids):
        self.dat = dat
        self.num_centroids = num_centroids
        self._make_centroids(self.num_centroids)
        print
        self._clean_dat(self.dat)

        while not self._has_converged(self.cent, self.cent_old):
            self.cent_old = self._copy_cent( self.cent)
            print "loop"
            self.dat = self._assign_points(self.dat, self.cent)
            self.cent = self._move_centers(self.dat, self.cent)
            #self.cent_old = self.cent
        self.dat = self._make_boxes(self.dat, self.cent)
        return self.dat

    def _clean_dat(self, dat):
        self.dat = dat
        filename = self.dat[0][self.FILE]
        if not filename.startswith(self.image_folder + os.sep) and not (filename.startswith(os.sep)):
            filename = self.image_folder + os.sep + filename
        xx,yy = Image.open(filename).size
        for i in range(len(self.dat)-1,-1,-1):
            self.dat[i][self.ATAG_ID] = -1
            #self.dat[i][self.FACE_Y] = yy - self.dat[i][self.FACE_Y]
            #self.dat[i][self.FACE_X] = xx - self.dat[i][self.FACE_X]
            if self.dat[i][self.FACE_X] == 0 or self.dat[i][self.FACE_Y] == 0: del self.dat[i]
            elif self.dat[i][self.FACE_X] + self.dat[i][self.FACE_WIDTH] >= xx : del self.dat[i]
            elif self.dat[i][self.FACE_Y] + self.dat[i][self.FACE_HEIGHT] >= yy : del self.dat[i]
            print "edge remove"

    def _assign_points(self, dat, cent):
        self.dat = dat
        self.cent = cent
        for j in range(len(self.dat)):
            smallarray = []
            for i in self.cent:
                smallarray.append(0)
            for i in range(len(self.cent)):
                h1 = self.cent[i][0]
                h2 = self.dat[j][self.FACE_X] + self.dat[j][self.FACE_WIDTH] /2
                v1 = self.cent[i][1]
                v2 = self.dat[j][self.FACE_Y] + self.dat[j][self.FACE_HEIGHT] /2
                l = math.sqrt((h2 -h1)**2 + (v2-v1)**2)
                smallarray[i] = l
            print "smallarray", smallarray
            index = 0
            smallest = smallarray[0]
            for i in range(len(self.cent)):
                if smallarray[i] < smallest :
                    index = i
                    smallest = smallarray[i]
            self.dat[j][self.ATAG_ID] = index
            print index
        return self.dat

    def _move_centers(self, dat, cent):
        self.dat = dat
        self.cent = cent

        for i in range(len(self.cent)):
            h = 0
            v = 0
            list = []
            for jj in range(len(self.cent)):
                list.append(0)
            for j in range(len(self.dat)) :
                if self.dat[j][self.ATAG_ID] == i :
                    list[i] = list[i] + 1
                    h = h + self.dat[j][self.FACE_X] + ( self.dat[j][self.FACE_WIDTH]) / 2
                    v = v + self.dat[j][self.FACE_Y] + ( self.dat[j][self.FACE_HEIGHT]) / 2
            self.cent[i][0] = h / float(list[i] +0.01)
            self.cent[i][1] = v / float(list[i] +0.01)
            print "working on", i, self.cent
        return self.cent

    def _has_converged(self, cent, cent_old):
        value = True
        for i in range(len(cent)):
            for j in range(len(cent[i])):
                if cent[i][j] != cent_old[i][j] : value = False
        return value

    def _make_centroids(self, num):
        filename = self.dat[0][self.FILE]
        if not filename.startswith(self.image_folder + os.sep) and not (filename.startswith(os.sep)):
            filename = self.image_folder + os.sep + filename
        w,h = Image.open(filename).size

        print "initial centroids", w, h
        self.cent = []
        division = w/num
        for i in range(num):
            start = division * i
            stop = division * i + division
            self.cent.append([random.randint(start,stop), h/2])
            self.cent_old.append([0,0])
        print self.cent

    def _copy_cent(self, cent):
        arr = []
        for i in cent:
            arr.append(i[:])
        return arr

    def _make_boxes(self, dat, cent):
        self.dat = dat
        self.cent = cent
        new_dat = []
        print cent, len(self.dat)
        for i in range(len(self.cent)):
            if self.cent[i][0] == 0 and self.cent[i][1] == 0: continue
            one_box = []
            x = self.cent[i][0]
            y = self.cent[i][1]
            h = 0
            v = 0
            if True:
                for j in range(len(self.dat)):
                    if self.dat[j][self.ATAG_ID] == i:
                        x = self.dat[j][self.FACE_X]
                        y = self.dat[j][self.FACE_Y]
                        h = self.dat[j][self.FACE_WIDTH]
                        v = self.dat[j][self.FACE_HEIGHT]
                        print "start", x,y,h,v, "i=",i
                        break

            for j in range(len(self.dat)):
                if self.dat[j][self.ATAG_ID] == i:
                    if self.dat[j][self.FACE_X] < x :
                        x = self.dat[j][self.FACE_X]
                        #h = self.dat[j][self.FACE_WIDTH] + self.dat[j][self.FACE_X] - x
                    if self.dat[j][self.FACE_Y] < y :
                        y = self.dat[j][self.FACE_Y]
                        #v = self.dat[j][self.FACE_HEIGHT] + self.dat[j][self.FACE_Y] - y

            for j in range(len(self.dat)):
                if self.dat[j][self.ATAG_ID] == i:
                    if self.dat[j][self.FACE_X] + self.dat[j][self.FACE_WIDTH] > x + h :
                        h = self.dat[j][self.FACE_WIDTH] +  self.dat[j][self.FACE_X] - x
                    if self.dat[j][self.FACE_Y] + self.dat[j][self.FACE_HEIGHT] > y + v :
                        v = self.dat[j][self.FACE_HEIGHT] +  self.dat[j][self.FACE_Y] - y
            for k in range(self.TOTAL):
                num = self.dat[0][k]
                if k == self.FACE_X: num = x
                if k == self.FACE_Y: num = y
                if k == self.FACE_WIDTH: num = h
                if k == self.FACE_HEIGHT: num = v
                if k == self.ATAG_ID: num = i
                one_box.append(num)

            if True:
                second_box = []
                for k in range(self.TOTAL):
                    num = self.dat[0][k]
                    if k == self.FACE_X: num = self.cent[i][0]
                    if k == self.FACE_Y: num = self.cent[i][1]
                    if k == self.FACE_WIDTH: num = 2
                    if k == self.FACE_HEIGHT: num = 2
                    if k == self.ATAG_ID: num = i
                    try:
                        second_box.append(int(num))
                    except:
                        second_box.append(num)
                new_dat.append(second_box)

            new_dat.append(one_box)
        print new_dat
        if not self.show_all_boxes:
            return new_dat
        ''' show all boxes '''
        self.dat.extend(new_dat)
        return self.dat
        #return new_dat