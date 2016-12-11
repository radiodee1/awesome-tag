import os
import atag_csv as enum

'''
Here we read the csv file that we made and train the models
'''

class Read( enum.Enum) :
    def __init__(self, atag):
        enum.Enum.__init__(self)

        self.boxlist_r = []
        self.boxlist_g = []
        self.boxlist_b = []
        self.num = 0

        self.a = atag
        self.picname = atag.VAR_IMAGE_NAME
        self.folder = atag.VAR_ROOT_DATABASE

        if self.picname.startswith(self.folder) :
            self.picname = self.picname[len(self.folder)+1 : ]
        print self.picname, "picname"

        self.csv_input = atag.VAR_LOCAL_DATABASE + os.sep + atag.VAR_MY_CSV_NAME + ".csv"
        self.csv_input_predict = atag.VAR_LOCAL_DATABASE + os.sep + "predict" + ".csv"


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

    def process_read_file_simple(self):
        with open(self.csv_input, 'r') as f:
            for line in f:
                self.process_read_line(line)
        f.close()
        print "num of boxes", self.num
        pass

    def process_read_file_predict(self):
        with open(self.csv_input_predict, 'r') as f:
            for line in f:
                self.process_read_line(line)
        f.close()
        print "num of boxes", self.num
        pass