import os
import atag_csv as enum
import nn_loader as loader

class PredictRead(enum.Enum):
    def __init__(self, atag):
        enum.Enum.__init__(self)
        self.a = atag
        self.predict_filename = self.a.VAR_LOCAL_DATABASE + os.sep + "predict-list" + ".csv"
        self.ll = loader.Load(self.a, "", self.predict_filename)
        self.filename = ""
        self.pic_num = 0
        self.dat = []

    def read_predict_list(self):
        self.ll.read_csv()
        self.dat = self.ll.dat
        if len(self.dat) > 0 and self.dat[self.pic_num][self.FILE].endswith(self.filename) : return
        for i in range(len(self.dat)):
            if self.dat[i][self.FILE].endswith(self.filename) :
                if i != self.pic_num: self.pic_num = i

        pass

    def predict_next(self, pic):
        list = self.dat[:]
        num = self.pic_num
        oldpic = pic # list[num][self.FILE]
        while oldpic.endswith(pic) and num < len(list):
            num += 1
            oldpic = pic
            pic = list[num][self.FILE]

        return pic


    def predict_prev(self, pic):
        list = self.dat[:]
        num = self.pic_num
        oldpic = pic # list[num][self.FILE]
        while oldpic.endswith(pic) and num > 0:
            num -= 1
            oldpic = pic
            pic = list[num][self.FILE]
        return pic


