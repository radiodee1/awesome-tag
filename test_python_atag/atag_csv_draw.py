import os
import atag_csv as enum

'''
Here we read the csv file that we made and train the models
'''

class Read( enum.Enum) :
    def __init__(self, atag):
        enum.Enum.__init__(self)

        self.boxlist = []
        self.num = 0

        self.a = atag
        self.picname = atag.VAR_IMAGE_NAME
        self.folder = atag.VAR_ROOT_DATABASE

        if self.picname.startswith(self.folder) :
            self.picname = self.picname[len(self.folder)+1 : ]
        print self.picname, "picname"

        self.csv_input = atag.VAR_LOCAL_DATABASE + os.sep + atag.VAR_MY_CSV_NAME + ".csv"

        with open(self.csv_input, 'r') as f:
            for line in f:
                self.process_read_line(line)
        f.close()
        print "num of boxes", self.num

    def process_read_line(self, line):
        line = line.split(",")
        print line[self.FILE]
        if line[self.FILE] == self.picname:
            self.num = self.num + 1
            self.boxlist.append([int(line[self.FACE_X]), int(line[self.FACE_Y]),
                                 int (line[self.FACE_WIDTH]) , int (line[self.FACE_HEIGHT])])