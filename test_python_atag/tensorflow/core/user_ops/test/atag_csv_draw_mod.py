import os
import atag_csv_mod as enum
#import nn_dim as dim
#import nn_loader as loader
#from PIL import Image, ImageFile

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
            self.gpu_test.extend([6,self.num])
            pass
    
    def is_top(box): return False
    def is_bottom(box): return False
    def is_left(box): return False
    def is_right(box): return False
   
