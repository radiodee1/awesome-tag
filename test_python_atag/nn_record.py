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

    def set_dat(self, dat):
        self.dat = dat

        print

    def make_boxes(self, filename):
        xx, yy = Image.open(filename).size

        w = xx / 28  ## how many tiles wide
        h = yy / 28  ## how many tiles high
        print "do individual file prediction"
        for i in range(w * h):
            x = i - (i / w)
            y = i / h
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
                    num = x * (xx / w)
                elif j is self.FACE_Y:
                    num = y * (yy / h)
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