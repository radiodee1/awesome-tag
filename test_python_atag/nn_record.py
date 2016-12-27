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
        self.dim_x = 28
        self.dim_y = 28

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
                if self.dat[i][self.ATAG_ID] == self.AGGREGATE_TOUCHED: self.dat[i][self.ATAG_ID] = self.AGGREGATE_START
            for i in range(len(self.dat)) :
                if self.dat[i][self.ATAG_ID] != self.AGGREGATE_DELETE:
                    self.dat[i][self.ATAG_ID] = self.AGGREGATE_TOUCHED
                    self._make_column(i)
        for i in range(len(self.dat) -1, -1, -1) :
            #print i, "del", len(self.dat), self.dat[i]
            if self.dat[i][self.ATAG_ID] == self.AGGREGATE_DELETE:
                del self.dat[i]
                #print len(self.dat), "after"
        for i in range(len(self.dat) -1, -1, -1) :
            #print i, "del", len(self.dat), self.dat[i]
            if self.dat[i][self.FACE_WIDTH] >= self.dat[i][self.FACE_HEIGHT] * 1.5:
                pass
                del self.dat[i]
                #print len(self.dat), "after"
        return self.dat

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
                    #print "boxatright"
                    return i
        return -1

    def _box_at_bottom(self, x, y, w, h):
        for i in range(len(self.dat)) :
            if self.dat[i][self.ATAG_ID] == self.AGGREGATE_START:
                xx,yy,ww,hh = self._get_xywh(i)
                if  y + h + 2 >= yy and y < yy and y + h -2 <= yy:
                    if self.strict_columns and x + w == xx + ww and xx == x :
                        print "boxatbottom strict"
                        return i
                    elif (not self.strict_columns and not self._reject_box(i, w)) and ((xx >=x and xx <= x+w -2) or
                            ( xx + ww >= x and xx + ww <= x+w   )):
                        print "boxatbottom loose"
                        return i
                    #else : print "boxatbottom none"
        return -1


    def _reject_box(self, i, w):
        #return False
        if self.dat[i][self.FACE_WIDTH] <= w  or True:
            if float(self.dat[i][self.FACE_WIDTH]) * float(1.5)  >= w   :
                return False
        return True


    def _make_row(self, box_id):

        zz = 0
        i = box_id
        j = box_id
        k = 0
        while  k < len(self.dat):

            if j < len(self.dat) \
                    and self.dat[j][self.ATAG_ID] != self.AGGREGATE_DELETE:
                x,y,w,h = self._get_xywh(j)
                zz = self._box_at_right(x,y,w,h)
                if zz != -1:

                    self.dat[i][self.FACE_WIDTH] = self.dat[i][self.FACE_WIDTH] + self.dat[zz][self.FACE_WIDTH]
                    self.dat[zz][self.ATAG_ID] = self.AGGREGATE_DELETE

            k = k + 1

    def _make_column(self, box_id):

        zz = 0
        i = box_id
        j = box_id
        k = 0
        while k < len(self.dat):

            if j < len(self.dat) \
                    and self.dat[j][self.ATAG_ID] != self.AGGREGATE_DELETE:
                x, y, w, h = self._get_xywh(j)
                zz = self._box_at_bottom(x, y, w, h)
                if zz != -1:
                    self.dat[i][self.FACE_HEIGHT] = self.dat[i][self.FACE_HEIGHT] + self.dat[zz][self.FACE_HEIGHT]
                    if not self.strict_columns:
                        if self.dat[i][self.FACE_WIDTH]   > self.dat[zz][self.FACE_WIDTH] + self.dim_x :
                            self.dat[i][self.FACE_WIDTH] = self.dat[zz][self.FACE_WIDTH]
                        if self.dat[i][self.FACE_X] < self.dat[zz][self.FACE_X] - self.dim_x  :

                            w_calc = self.dat[i][self.FACE_X] + self.dat[i][self.FACE_WIDTH] - self.dat[zz][self.FACE_X]
                            if w_calc > 2:
                                self.dat[i][self.FACE_WIDTH] = w_calc
                                self.dat[i][self.FACE_X] = self.dat[zz][self.FACE_X]

                    self.dat[zz][self.ATAG_ID] = self.AGGREGATE_DELETE

            k = k + 1