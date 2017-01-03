import random
import os
import atag_csv as enum
from PIL import Image
import math

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

    def do_km(self, dat, num_centroids):
        self.dat = dat
        self.num_centroids = num_centroids
        self._make_centroids(self.num_centroids)
        print
        while not self._has_converged(self.cent, self.cent_old):
            self.cent_old = self.cent
            print "loop"
            self.dat = self._assign_points(self.dat, self.cent)
            self.cent = self._move_centers(self.dat, self.cent)
        self.dat = self._make_boxes(self.dat, self.cent)
        return self.dat

    def _assign_points(self, dat, cent):
        self.dat = dat
        self.cent = cent
        for j in range(len(self.dat)):
            smallarray = []
            for i in self.cent:
                smallarray.append(0)
            for i in range(len(self.cent)):
                h1 = self.cent[i][0]
                h2 = self.dat[j][self.FACE_X]
                v1 = self.cent[i][1]
                v2 = self.dat[j][self.FACE_Y]
                l = math.sqrt(math.pow(h1 -h2,2) + math.pow(v1-v2,2))
                smallarray[i] = l
            index = 0
            smallest = smallarray[0]
            for i in range(len(self.cent)):
                if smallarray[i] < smallest :
                    index = i
                    smallest = smallarray[i]
            self.dat[j][self.ATAG_ID] = index
        pass
        return self.dat

    def _move_centers(self, dat, cent):
        self.dat = dat
        self.cent = cent

        for i in range(len(self.cent)):
            h = 0
            v = 0
            for j in range(len(self.dat)) :
                if self.dat[j][self.ATAG_ID] == i :
                    h = h + self.dat[j][self.FACE_X]
                    v = v + self.dat[j][self.FACE_Y]
            self.cent[i][0] = h / len(self.dat)
            self.cent[i][1] = v / len(self.dat)
            print "working on", i
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

    def _make_boxes(self, dat, cent):
        self.dat = dat
        self.cent = cent
        new_dat = []
        print cent
        for i in range(len(self.cent)):
            one_box = []
            x = 0
            y = 0
            h = 0
            v = 0
            for j in range(len(self.dat)):
                if self.dat[j][self.ATAG_ID] == i:
                    if self.dat[j][self.FACE_X] < x : x = self.dat[j][self.FACE_X]
                    if self.dat[j][self.FACE_Y] < y : y = self.dat[j][self.FACE_Y]
                    if self.dat[j][self.FACE_X] + self.dat[j][self.FACE_WIDTH] > x + h :
                        h = self.dat[j][self.FACE_WIDTH] -  self.dat[j][self.FACE_X]
                    if self.dat[j][self.FACE_Y] + self.dat[j][self.FACE_HEIGHT] > y + v :
                        v = self.dat[j][self.FACE_HEIGHT] -  self.dat[j][self.FACE_Y]
            for k in range(self.TOTAL):
                num = self.dat[0][k]
                if k == self.FACE_X: num = x
                if k == self.FACE_Y: num = y
                if k == self.FACE_WIDTH: num = h
                if k == self.FACE_HEIGHT: num = v

                one_box.append(num)
            new_dat.append(one_box)
        print new_dat
        return new_dat