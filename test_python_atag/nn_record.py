import os
import atag_csv as enum
from PIL import Image

class Record( enum.Enum):
    def __init__(self, atag):
        enum.Enum.__init__(self)
        print
        self.dat = []
        self.a = atag
        self.predict_filename = self.a.VAR_LOCAL_DATABASE + os.sep + "predict" + ".csv"
        self.strict_columns = False

    def set_dat(self, dat):
        self.dat = dat

    def make_boxes(self, filename):
        xx, yy = Image.open(filename).size

        w = xx / 28  ## how many tiles wide
        h = yy / 28  ## how many tiles high
        print "do individual file prediction"
        for i in range(w * h):
            y = i / w
            x = i - (y * w)
            temp = []
            for j in range(self.TOTAL):
                num = 0
                if j is self.FILE:
                    num = filename
                elif j is self.FACE_WIDTH:
                    num = xx / w
                    if num < 28: num = 28
                elif j is self.FACE_HEIGHT:
                    num = yy / h
                    if num < 28: num = 28
                elif j is self.FACE_X:
                    #print xx / w
                    num = x  * (xx / w) #- (y * (yy / w))
                elif j is self.FACE_Y:
                    num = y * (yy / h)
                elif j is self.COLOR :
                    num = self.RED
                elif j is self.ATAG_ID :
                    num = i
                temp.append(num)
            self.dat.append(temp)
        return self.dat

    def save_dat_to_file(self):
        #print self.dat
        f = open(self.predict_filename, "w")
        f = open(self.predict_filename, "a")
        for i in self.dat :
            temp = ""
            for j in range(len(i)) :
                temp = temp + str(i[j])
                if j < len(i) -1 : temp = temp + ","
                else: temp = temp + "\n"
            pass
            f.write(temp)

    def remove_lines_from_dat(self, lines):
        for line in lines:
            for num in range(len(self.dat)) :
                print self.dat[num], "list"

                if self.dat[num][self.ATAG_ID] == line :
                    del self.dat[num]
                    break
        return self.dat

    def show_dat_list(self, name = "listing"):
        for line in self.dat:
            print line, name
        print name, "over"

    def renumber_dat_list(self, dat):
        self.dat = dat
        for i in range(len(self.dat)) :
            zz = self.dat[i]
            zz[self.ATAG_ID] = i
        return  self.dat

    def aggregate_dat_list(self, dat):
        self.dat = dat
        loop = True
        for i in range(len(self.dat)):
            self.dat[i][self.ATAG_ID] = self.AGGREGATE_START
        while loop:
        #for k in self.dat:
            for i in self.dat:
                loop = False
                if i[self.ATAG_ID] == self.AGGREGATE_START : loop = True
            for i in range(len(self.dat)) :
                if  self.dat[i][self.ATAG_ID] != self.AGGREGATE_DELETE:
                    self.dat[i][self.ATAG_ID] = self.AGGREGATE_TOUCHED
                    self._make_row(i)
            for i in range(len(self.dat)):
                pass
                if self.dat[i][self.ATAG_ID] == self.AGGREGATE_TOUCHED: self.dat[i][self.ATAG_ID] = self.AGGREGATE_START
            for i in range(len(self.dat)) :
                if self.dat[i][self.ATAG_ID] != self.AGGREGATE_DELETE:
                    self.dat[i][self.ATAG_ID] = self.AGGREGATE_TOUCHED
                    self._make_column(i)
        for i in range(len(self.dat) -1, -1, -1) :
            print i, "del", len(self.dat), self.dat[i]
            if self.dat[i][self.ATAG_ID] == self.AGGREGATE_DELETE:
                del self.dat[i]
                print len(self.dat), "after"

    def _get_xywh(self, i):
        x = self.dat[i][self.FACE_X]
        y = self.dat[i][self.FACE_Y]
        w = self.dat[i][self.FACE_WIDTH]
        h = self.dat[i][self.FACE_HEIGHT]
        return x,y,w,h

    def _box_at_right(self, x, y, w, h):
        for i in range(len(self.dat)) :
            if self.dat[i][self.ATAG_ID] == self.AGGREGATE_START:
                xx,yy,ww,hh = self._get_xywh(i)
                if  yy == y and x + w + 2 >= xx and y + h == yy + hh and x < xx and x + w -2 <= xx:
                    print "boxatright"
                    return i
        return -1

    def _box_at_bottom(self, x, y, w, h):
        for i in range(len(self.dat)) :
            if self.dat[i][self.ATAG_ID] == self.AGGREGATE_START:
                xx,yy,ww,hh = self._get_xywh(i)
                if  xx == x and y + h + 2 >= yy and y < yy and y + h -2 <= yy:
                    if self.strict_columns and x + w == xx + ww:
                        print "boxatbottom strict"
                        return i
                    else:
                        print "boxatbottom loose"
                        return i
        return -1

    def _empty_box(self):
        return [0,0,"",0,0,0,0,0,0,0,"",0,0]

    def _make_row(self, box_id):

        zz = 0
        i = box_id
        j = box_id
        k = 0
        while  k < len(self.dat):

            if j < len(self.dat) \
                    and self.dat[j][self.ATAG_ID] != self.AGGREGATE_DELETE: # \
                    #and self.dat[i][self.ATAG_ID] != self.AGGREGATE_DELETE :
                x,y,w,h = self._get_xywh(j)
                zz = self._box_at_right(x,y,w,h)
                if zz != -1:

                    self.dat[i][self.FACE_WIDTH] = self.dat[i][self.FACE_WIDTH] + self.dat[zz][self.FACE_WIDTH]
                    self.dat[zz][self.ATAG_ID] = self.AGGREGATE_DELETE

            k = k + 1

    def _make_column(self, box_id):
        print "c"
        zz = 0
        i = box_id
        j = box_id
        k = 0
        while k < len(self.dat):

            if j < len(self.dat) \
                    and self.dat[j][self.ATAG_ID] != self.AGGREGATE_DELETE: # \
                    #and self.dat[i][self.ATAG_ID] != self.AGGREGATE_DELETE:
                x, y, w, h = self._get_xywh(j)
                zz = self._box_at_bottom(x, y, w, h)
                if zz != -1:
                    self.dat[i][self.FACE_HEIGHT] = self.dat[i][self.FACE_HEIGHT] + self.dat[zz][self.FACE_HEIGHT]
                    self.dat[zz][self.ATAG_ID] = self.AGGREGATE_DELETE

            k = k + 1