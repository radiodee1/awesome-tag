import os
import atag_csv_mod as enum
#import nn_dim as dim
#import nn_loader as loader
from PIL import Image, ImageDraw

'''
Here we read the csv file that we made and train the models
'''

class Read( enum.Enum) :
    def __init__(self):
        enum.Enum.__init__(self)
        #dim.Dimension.__init__(self)


        self.boxlist_r = []
        self.boxlist_g = []
        self.boxlist_b = []
        self.gpu_test = []
        self.num = 0

        self.num_chosen = 0
        self.line_chosen = []
        #self.dim_x = self.DIMENSIONS[self.key][self.COLUMN_XY_CONV][0]
        #self.dim_y = self.DIMENSIONS[self.key][self.COLUMN_XY_CONV][1]
        self.img = None
        #self.image_folder = atag.VAR_ROOT_DATABASE
        self.dat = []

        #self.a = atag
        #self.picname = atag.VAR_IMAGE_NAME
        #self.folder = atag.VAR_ROOT_DATABASE

        #if self.picname.startswith(self.folder) :
        #    self.picname = self.picname[len(self.folder)+1 : ]
        #print self.picname, "picname"

        #self.csv_input = atag.VAR_LOCAL_DATABASE + os.sep + atag.VAR_MY_CSV_NAME + ".csv"
        #self.csv_input_predict = atag.VAR_LOCAL_DATABASE + os.sep + "predict" + ".csv"
        #self.csv_input_dot = atag.VAR_LOCAL_DATABASE + os.sep + atag.VAR_MY_CSV_NAME + ".dot.csv"
        self.csv_input_predict_list = "." + os.sep + "predict-list" + ".csv"

    def process_read_line(self, line):
        line = line.split(",")
        #print line[self.FILE], "read"
        if True :
            self.num = self.num + 1

            if line[self.COLOR] == self.RED :
                self.boxlist_r.append([int(line[self.FACE_X]), int(line[self.FACE_Y]),
                                 int (line[self.FACE_WIDTH]) , int (line[self.FACE_HEIGHT])])
                self.gpu_test.extend([int(line[self.FACE_X]), int(line[self.FACE_Y]),
                                 int (line[self.FACE_WIDTH]) , int (line[self.FACE_HEIGHT]), self.num, 15])
            if line[self.COLOR] == self.GREEN:
                self.boxlist_g.append([int(line[self.FACE_X]), int(line[self.FACE_Y]),
                                       int(line[self.FACE_WIDTH]), int(line[self.FACE_HEIGHT])])
            if line[self.COLOR] == self.BLUE:
                self.boxlist_b.append([int(line[self.FACE_X]), int(line[self.FACE_Y]),
                                       int(line[self.FACE_WIDTH]), int(line[self.FACE_HEIGHT])])
            if self.num == self.num_chosen:
                self.line_chosen = line

    
    
    def process_read_file_predict_list(self):
        if os.path.isfile(self.csv_input_predict_list):
            self.gpu_test = []
            with open(self.csv_input_predict_list, 'r') as f:
                for line in f:
                    self.process_read_line(line)
            f.close()
            print "num of boxes predict list", self.num
            self.gpu_test.extend([self.GPU_TOT,  self.num])
            pass
    
    def is_top(self, box):
        if (box & self.BIT_TOP) >> 0 == 1 : return True;
        return False
    def is_bottom(self, box):
        if (box & self.BIT_BOTTOM ) >> 1 == 1: return True;
        return False
    def is_left(self, box):
        if (box & self.BIT_LEFT ) >> 2 == 1: return True;
        return False
    def is_right(self, box):
        if (box & self.BIT_RIGHT) >> 3 == 1: return True;
        return False
   

    def process_show_gpu_output(self, dat=[]):
        self.dat = dat
        self.img = Image.new('RGB',(700,900))
        draw = ImageDraw.Draw(self.img)
        for i in range(len(self.dat) // self.GPU_TOT):
            line = self.dat[i * self.GPU_TOT: i * self.GPU_TOT + self.GPU_TOT]
            #print "out", line

            #if line[self.GPU_W] == 0 or line[self.GPU_H] == 0: continue

            if self.is_top(line[self.GPU_BOX]):
                draw.line((line[self.GPU_X], line[self.GPU_Y],
                           line[self.GPU_X] + line[self.GPU_W], line[self.GPU_Y] ), fill=0x0000ff,width=1)
                pass
            if self.is_bottom(line[self.GPU_BOX]):
                draw.line((line[self.GPU_X], line[self.GPU_Y] + line[self.GPU_H],
                           line[self.GPU_X] + line[self.GPU_W], line[self.GPU_Y] + line[self.GPU_H]), fill=0x0000ff, width=1)
                pass
            if self.is_left(line[self.GPU_BOX]):
                draw.line((line[self.GPU_X], line[self.GPU_Y],
                           line[self.GPU_X], line[self.GPU_Y] + line[self.GPU_H]), fill=0x0000ff, width=1)

                pass
            if self.is_right(line[self.GPU_BOX]):
                draw.line((line[self.GPU_X] + line[self.GPU_W], line[self.GPU_Y],
                           line[self.GPU_X] + line[self.GPU_W], line[self.GPU_Y] + line[self.GPU_H]), fill=0x0000ff, width=1)
                pass

            if (line[self.GPU_H] >= 4 and line[self.GPU_W] >= 4 and True)  or line[self.GPU_NUM] == 52:
                draw.rectangle([line[self.GPU_X], line[self.GPU_Y],
                                line[self.GPU_X] + line[self.GPU_W], line[self.GPU_Y] + line[self.GPU_H]], outline=0x00ff00)

            pass
        self.img.show("gpu output")
        self.img.format = "png"
        self.img.save("sample.png","png")