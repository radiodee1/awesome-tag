import atag_csv as enum
from PIL import Image

class Record( enum.Enum):
    def __init__(self, atag):
        print
        self.dat = []
        self.a = atag

    def save_dat(self, dat):
        self.dat = dat

        print

    def make_boxes(self, filename):
        w = 10  ## how many tiles wide
        h = 10  ## how many tiles high
        xx, yy = Image.open(filename).size
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