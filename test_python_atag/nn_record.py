import random
import os
import atag_csv as enum
#import nn_kmeans as kmeans
from PIL import Image

class Record( enum.Enum):
    def __init__(self, atag):
        enum.Enum.__init__(self)
        print
        self.dat = []
        self.a = atag
        self.predict_filename = self.a.VAR_LOCAL_DATABASE + os.sep + "predict" + ".csv"
        self.strict_columns = False
        self.allow_skipping = True
        self.strict_next_to = True
        self.dim_x = 28
        self.dim_y = 28
        self.count = 0

    def set_dat(self, dat):
        self.dat = dat

    def make_boxes(self, filename, dim=28):
        self.dim_x = dim
        self.dim_y = dim
        xx, yy = Image.open(filename).size

        w = xx / self.dim_x  ## w is how many tiles wide
        h = yy / self.dim_y  ## h is how many tiles high
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
                    if num < self.dim_x: # 28
                        num = self.dim_x # 28
                elif j is self.FACE_HEIGHT:
                    num = yy / h
                    if num < self.dim_y: # 28
                        num = self.dim_y # 28
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

    def make_boxes_mc(self, filename, dim=28, dat = []):
        self.dim_x = dim
        self.dim_y = dim

        self.dat = []

        for k in range(len(dat)) :
            xpos = dat[k][self.FACE_X]
            ypos = dat[k][self.FACE_Y]
            width = dat[k][self.FACE_WIDTH]
            height = dat[k][self.FACE_HEIGHT]

            xx, yy = Image.open(filename).size

            mc_num = dim # xx / dim # random.randint(0,xx) #(xx, xx*yy)
            div = 2 # 4
            print "do mc file prediction"
            for i in range(mc_num):
                sizex = random.randint(width - width/div, width + width/div)
                sizey = random.randint(height - height/div, height + height/div)

                temp = []
                for j in range(self.TOTAL):
                    num = 0
                    if j is self.FILE:
                        num = filename
                    elif j is self.FACE_WIDTH:
                        num = sizex #xx / w

                    elif j is self.FACE_HEIGHT:
                        num = sizey #yy / h

                    elif j is self.FACE_X:

                        num = random.randint(xpos - width/div, xpos + width/div)
                    elif j is self.FACE_Y:

                        num = random.randint(ypos - height/div, ypos + height/div)

                    elif j is self.COLOR :
                        num = self.RED
                    elif j is self.ATAG_ID :
                        num = i
                    temp.append(num)

                if not (temp[self.FACE_X] + temp[self.FACE_WIDTH] >= xx or temp[self.FACE_Y] + temp[self.FACE_HEIGHT] >= yy or
                    temp[self.FACE_X] < 0 or temp[self.FACE_Y] < 0):
                    self.dat.append(temp)
            self.dat.append(dat[k])

        return self.dat

    def save_dat_to_file(self, dat = []):
        self.dat = dat
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
            for num in range(len(self.dat)-1,-1,-1) :
                #print self.dat[num], "list"

                if self.dat[num][self.ATAG_ID] == line :
                    del self.dat[num]
                    print "delete here", num, line
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

    ##############################################################

    def aggregate_dat_list(self, dat, del_shapes=False):
        self.dat = dat
        loop = True
        for i in range(len(self.dat)):
            self.dat[i][self.ATAG_ID] = self.AGGREGATE_START

        self.count = 0
        if True:
            ''' find rows '''

            self._make_row()
            print "---"

            self.dat = self._make_boxes()
            self._delete_marked()
            ''' renumber '''
            for i in range(len(self.dat)):
                if self.dat[i][self.ATAG_ID] >= 0 : self.dat[i][self.ATAG_ID] = self.AGGREGATE_START
            ''' make columns '''

            self._make_column()
            self.dat = self._make_boxes()
            self._delete_marked()

            #self._make_column()
            #self.dat = self._make_boxes()
            #self._delete_marked()
        if del_shapes:
            for i in range(len(self.dat) -1, -1, -1) :
                ''' delete odd sizes '''
                if (self.dat[i][self.FACE_WIDTH] >= float(self.dat[i][self.FACE_HEIGHT]) * float(2.5) or
                    float(self.dat[i][self.FACE_WIDTH]) * float(2.5) <= self.dat[i][self.FACE_HEIGHT] or
                    self.dat[i][self.FACE_HEIGHT] <= self.dim_y * 2 or
                    self.dat[i][self.FACE_WIDTH] <= self.dim_x * 2):
                    pass
                    del self.dat[i]

        return self.dat

    def _delete_marked(self):
        for i in range(len(self.dat) -1, -1, -1) :
            ''' delete marked for delete '''
            if self.dat[i][self.ATAG_ID] == self.AGGREGATE_DELETE:
                del self.dat[i]
                print "del"

    def _get_xywh(self, i):
        x = self.dat[i][self.FACE_X]
        y = self.dat[i][self.FACE_Y]
        w = self.dat[i][self.FACE_WIDTH]
        h = self.dat[i][self.FACE_HEIGHT]
        return x,y,w,h

    def _box_at_right(self, x, y, w, h, k):
        for i in range(len(self.dat)) :
            if self.dat[i][self.ATAG_ID] == self.AGGREGATE_START and k != i:# or self.strict_next_to:
                xx,yy,ww,hh = self._get_xywh(i)
                if  yy >= y and x + w + 2 >= xx and y + h >= yy and x <= xx and x + w -2 <= xx:
                    print "boxatright"
                    return i
                if  self.allow_skipping and x + w + 2 + self.dim_x >= xx and x <= xx and ((yy >= y and y + h >= yy) or
                                                                     (y >= yy and y <= yy+hh))  :
                    print "boxatright skipping"
                    return i
        #self.count = self.count + 1
        return -1

    def _box_at_bottom(self, x, y, w, h, k):
        for i in range(len(self.dat)) :
            if self.dat[i][self.ATAG_ID] == self.AGGREGATE_START and k != i: #
                #self.dat[i][self.ATAG_ID] = self.count # self.AGGREGATE_TOUCHED #or self.strict_next_to:
                xx,yy,ww,hh = self._get_xywh(i)
                #if yy +hh +2 >=  y and yy <= y:
                #    print "y is reversed"
                if  y + h + 2  >= yy and y <= yy :
                    print "y is good", y, h, yy, hh
                    if self.strict_columns and x + w == xx + ww and xx == x :
                        print "boxatbottom strict"
                        return i
                    elif (not self.strict_columns): # and not self._reject_box(i, w)) : #and
                        if ((xx >=x and xx <= x+w ) or
                                ( xx + ww >= x and xx + ww <= x+w   ) or
                                ( x + w >=xx and x <= xx) or
                                ( x + w >= xx and x + w <= xx + ww)):
                            print "boxatbottom loose"
                            return i
                        if self.allow_skipping and x + w + 2 + self.dim_x >=xx and x <= xx :
                            print "boxatbottom skipping"
                            return i
                    #else : print "boxatbottom none"
        return -1


    def _reject_box(self, i, w):
        #return False
        if self.dat[i][self.FACE_WIDTH] <= w  :
            if float(self.dat[i][self.FACE_WIDTH]) * float(1.5)  >= w   :
                return False
        return True


    def _make_row(self):

        zz = 0
        k = 0
        while  k < len(self.dat):

            if (k < len(self.dat) and (  self.dat[k][self.ATAG_ID] == self.AGGREGATE_START)):


                self.dat[k][self.ATAG_ID] = self.count

                x,y,w,h = self._get_xywh(k)
                zz = self._box_at_right(x,y,w,h,k)
                while zz != -1:
                    w_calc = self.dat[zz][self.FACE_X] + self.dat[zz][self.FACE_WIDTH] - self.dat[k][self.FACE_X]

                    if True:
                        if True: #self.dat[zz][self.ATAG_ID] == self.AGGREGATE_START:
                            self.dat[zz][self.ATAG_ID] = self.count
                            #w = w_calc
                            #self.dat[zz][self.FACE_WIDTH] = w
                            zz = self._box_at_right(x, y, w, h,k)
                            #if zz != -1: x,y,w,h = self._get_xywh(zz)
                            w = w_calc
                        else:
                            zz = -1

                    print "row", k

            k = k + 1

            self.count = self.count + 1
            print "count" , self.count


    def _make_column(self):

        self.count = 0
        zz = 0
        k = 0
        while k < len(self.dat):
        #for k in range(len(self.dat)):

            if k < len(self.dat) :#and  ( self.dat[k][self.ATAG_ID] >= 0):

                id =  self.dat[k][self.ATAG_ID]
                if id == self.AGGREGATE_START or id == self.AGGREGATE_TOUCHED:
                    self.dat[k][self.ATAG_ID] = self.count

                #if not self.strict_next_to: self.dat[i][self.ATAG_ID] = self.AGGREGATE_TOUCHED
                x, y, w, h = self._get_xywh(k)
                zz = self._box_at_bottom(x, y, w, h,k)
                while zz != -1:
                    h_calc = self.dat[zz][self.FACE_Y] + self.dat[zz][self.FACE_HEIGHT] - self.dat[k][self.FACE_Y]
                    self.dat[k][self.ATAG_ID] = self.count

                    if True:
                        for a in range(len(self.dat)):
                            if a != zz and self.dat[a][self.ATAG_ID] == self.dat[zz][self.ATAG_ID]:# and self.dat[a][self.ATAG_ID] >= 0 :
                                #self.dat[a][self.ATAG_ID] = self.dat[k][self.ATAG_ID]
                                #print "renumber", self.dat[zz][self.ATAG_ID], self.dat[k][self.ATAG_ID], k,y,h, len(self.dat)
                                pass
                        self.dat[zz][self.ATAG_ID] = self.dat[k][self.ATAG_ID]

                        if True: #y != self.dat[k][self.FACE_Y]:
                            y = self.dat[k][self.FACE_Y]
                            h = h_calc
                            x = self.dat[zz][self.FACE_X]
                            w = self.dat[zz][self.FACE_WIDTH]
                            zz = self._box_at_bottom(x, y, w, h,k)

                        else :
                            zz = -1

            print "column" , k, "count", self.count

            k = k + 1
            self.count = self.count + 1
            #if k >= len(self.dat): break


    def _make_boxes(self):
        def sort_key(list):
            return list[self.ATAG_ID]
        self.dat.sort(key=sort_key)

        print "end dat",self.dat[0:1],"..."
        new_dat = []
        loop = True

        for i in range(len(self.dat)):
            if self.dat[i][self.ATAG_ID] < 0:
                self.dat[i][self.ATAG_ID] = self.AGGREGATE_DELETE
                print "lower than zero"
        self._delete_marked()
        i = 0
        while loop:

            if i >= len(self.dat) :
                loop = False
            one_box = []
            '''
            cent_num = 0
            for k in range(len(self.dat)):
                if self.dat[k][self.ATAG_ID] == i:
                    cent_num = k
                    break
            '''
            x = 0
            y = 0
            h = 0
            v = 0
            if True:
                not_found = False
                for j in range(len(self.dat)):
                    if self.dat[j][self.ATAG_ID] == i:
                        x = self.dat[j][self.FACE_X]
                        y = self.dat[j][self.FACE_Y]
                        h = self.dat[j][self.FACE_WIDTH]
                        v = self.dat[j][self.FACE_HEIGHT]
                        print "start", x, y, h, v, "i=", i
                        break
                    if j >= self.dat[len(self.dat) - 1][self.ATAG_ID] :
                        not_found = True
                if not_found == True : #or (False and x == 0 and y == 0 and h == 0 and v == 0):
                    print "skip i", i
                    i = i + 1
                    continue
            newx = x
            newy = y
            print "make boxes for", i
            for j in range(len(self.dat)):
                if self.dat[j][self.ATAG_ID] == i:
                    if self.dat[j][self.FACE_X] < x:
                        newx = self.dat[j][self.FACE_X]

                    if self.dat[j][self.FACE_Y] < y:
                        newy = self.dat[j][self.FACE_Y]

            for j in range(len(self.dat)):
                if self.dat[j][self.ATAG_ID] == i:
                    if self.dat[j][self.FACE_X] + self.dat[j][self.FACE_WIDTH] > x + h:
                        h = self.dat[j][self.FACE_WIDTH] + self.dat[j][self.FACE_X] - x

                    if self.dat[j][self.FACE_Y] + self.dat[j][self.FACE_HEIGHT] > y + v:
                        v = self.dat[j][self.FACE_HEIGHT] + self.dat[j][self.FACE_Y] - y

            x = newx
            y = newy
            if not (x == 0 and y == 0 and h == 0 and v == 0):
                for k in range(self.TOTAL):
                    num = self.dat[0][k]
                    if k == self.FACE_X: num = x
                    if k == self.FACE_Y: num = y
                    if k == self.FACE_WIDTH: num = h
                    if k == self.FACE_HEIGHT: num = v
                    if k == self.ATAG_ID: num = i
                    one_box.append(num)
                new_dat.append(one_box)

            i = i + 1
        self.dat = new_dat
        print self.dat[:10],"..."
        return self.dat
