import os
import atag_csv as enum
import nn_dim as dim
import nn_loader as loader
from PIL import Image, ImageFile

'''
Here we read the csv file that we made and train the models
'''

class Read( enum.Enum, dim.Enum) :
    def __init__(self, atag):
        enum.Enum.__init__(self)
        dim.Enum.__init__(self)


        self.boxlist_r = []
        self.boxlist_g = []
        self.boxlist_b = []
        self.num = 0

        self.num_chosen = 0
        self.line_chosen = []
        self.dim_x = self.DIMENSIONS[self.key][self.COLUMN_XY_CONV][0]
        self.dim_y = self.DIMENSIONS[self.key][self.COLUMN_XY_CONV][1]
        self.img = None
        self.image_folder = atag.VAR_ROOT_DATABASE


        self.a = atag
        self.picname = atag.VAR_IMAGE_NAME
        self.folder = atag.VAR_ROOT_DATABASE

        if self.picname.startswith(self.folder) :
            self.picname = self.picname[len(self.folder)+1 : ]
        print self.picname, "picname"

        self.csv_input = atag.VAR_LOCAL_DATABASE + os.sep + atag.VAR_MY_CSV_NAME + ".csv"
        self.csv_input_predict = atag.VAR_LOCAL_DATABASE + os.sep + "predict" + ".csv"
        self.csv_input_dot = atag.VAR_LOCAL_DATABASE + os.sep + atag.VAR_MY_CSV_NAME + ".dot.csv"
        self.csv_input_predict_list = atag.VAR_LOCAL_DATABASE + os.sep + "predict-list" + ".csv"

    def process_read_line(self, line):
        line = line.split(",")
        #print line[self.FILE], "read"
        if line[self.FILE].endswith(self.picname) :
            self.num = self.num + 1

            if line[self.COLOR] == self.RED :
                self.boxlist_r.append([int(line[self.FACE_X]), int(line[self.FACE_Y]),
                                 int (line[self.FACE_WIDTH]) , int (line[self.FACE_HEIGHT])])
            if line[self.COLOR] == self.GREEN:
                self.boxlist_g.append([int(line[self.FACE_X]), int(line[self.FACE_Y]),
                                       int(line[self.FACE_WIDTH]), int(line[self.FACE_HEIGHT])])
            if line[self.COLOR] == self.BLUE:
                self.boxlist_b.append([int(line[self.FACE_X]), int(line[self.FACE_Y]),
                                       int(line[self.FACE_WIDTH]), int(line[self.FACE_HEIGHT])])
            if self.num == self.num_chosen:
                self.line_chosen = line

    def process_read_file_simple(self):
        if os.path.isfile(self.csv_input):
            with open(self.csv_input, 'r') as f:
                for line in f:
                    self.process_read_line(line)
            f.close()
            print "num of boxes", self.num
            pass

    def process_read_file_predict(self):
        if os.path.isfile(self.csv_input_predict):
            with open(self.csv_input_predict, 'r') as f:
                for line in f:
                    self.process_read_line(line)
            f.close()
            print "num of boxes", self.num
            pass

    def process_read_file_dot(self):
        if os.path.isfile(self.csv_input_dot):
            with open(self.csv_input_dot, 'r') as f:
                for line in f:
                    self.process_read_line(line)
            f.close()
            print "num of boxes", self.num
            pass

    def process_read_file_predict_list(self):
        if os.path.isfile(self.csv_input_predict_list):
            with open(self.csv_input_predict_list, 'r') as f:
                for line in f:
                    self.process_read_line(line)
            f.close()
            print "num of boxes", self.num
            pass

    def process_read_file_convolution_in_depth(self, num = 1):
        self.num_chosen = num
        self.process_read_file_simple()
        #if self.num_chosen > self.num : self.num_chosen = 0
        print self.num_chosen
        self._get_pixels_from_dat()
        pass

    def _get_pixels_from_dat(self):
        print ("work with dat var")
        self.image = []
        self.label = []
        self.image_x3 = []
        self.image_skin = []

        if True: #self.iter < stop and stop <= len(self.dat) and self.iter < len(self.dat):
            #filename = self.dat[self.iter][self.FILE]
            filename = self.picname
            if not filename.startswith(self.image_folder + os.sep) and not (filename.startswith(os.sep)) :
                filename = self.image_folder + os.sep + filename
            x = int(self.line_chosen[self.FACE_X])
            y = int(self.line_chosen[self.FACE_Y])
            width = int(self.line_chosen[self.FACE_WIDTH])
            height = int(self.line_chosen[self.FACE_HEIGHT])

            #if True: #filename != self.filename_old:
            print " -- " , filename

            ''' open image if it is new! '''
            self.filename = filename
            #if True: #self.filename != self.filename_old:
            self.img = Image.open(filename)
            #self.filename_old = self.filename

            ll = loader.Load(self.a, self.picname)
            #ll.__init__(atag,atag.VAR_ROOT_DATABASE, atag.VAR_LOCAL_DATABASE, atag.VAR_MY_CSV_NAME)
            skin, img , three = ll.look_at_img(filename, x, y, width, height)
            print len(skin), len(img), len(three)