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
        self.external_count = 0

    def read_skipping_repeats(self):
        self.ll = loader.Load(self.a, "")
        self.ll.read_csv()
        self.start = self.ll.dat[:]
        self.dat = []
        filename = self.start[0]
        self.dat.append(filename)
        #print len(self.start), filename, "before_start"
        for i in range(len(self.start)):
            if not self.start[i][self.FILE].endswith(filename[self.FILE]):
                self.dat.append(self.start[i])
            filename = self.start[i]

    def read_predict_list(self):
        self.ll.read_csv()
        self.dat = self.ll.dat
        if len(self.dat) > 0 and self.dat[self.pic_num][self.FILE].endswith(self.filename) : return
        count = 0
        self.external_count = 0
        filename_old = ""
        for i in range(len(self.dat)):

            if self.dat[i][self.FILE].endswith(self.filename) :
                if i != self.pic_num: self.pic_num = i
                break
            if not filename_old.endswith(self.dat[i][self.FILE]):
                count += 1
            filename_old = self.dat[i][self.FILE]
        self.external_count = count

        pass

    def predict_next(self, pic):
        list = self.dat[:]
        num = self.pic_num
        if num + 1 >= len(list): return pic
        self.external_count += 1
        oldpic = pic # list[num][self.FILE]
        while oldpic.endswith(pic) and num < len(list):
            num += 1
            oldpic = pic
            pic = list[num][self.FILE]

        return pic


    def predict_prev(self, pic):
        list = self.dat[:]
        num = self.pic_num
        if num - 1 < 0: return pic
        self.external_count -= 1
        oldpic = pic # list[num][self.FILE]
        while oldpic.endswith(pic) and num > 0:
            num -= 1
            oldpic = pic
            pic = list[num][self.FILE]
        return pic


