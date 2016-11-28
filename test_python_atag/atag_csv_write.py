import os
import random
import atag_csv as enum

'''
Here we read the split file and write our own csv file for training later on.
'''

class Write( enum.Enum) :
    def __init__(self, atag):
        enum.Enum.__init__(self)

        self.dat = []

        self.a = atag
        self.csvnum = atag.VAR_SPLIT_CURRENT
        self.csvfolder = atag.VAR_SPLIT_FOLDER_NAME
        self.csvname = 'train_'
        self.csvend = '.csv'

        self.csvfolder = self.csvfolder[: -1]
        if self.csvfolder.endswith('1') : self.csvfolder = self.csvfolder[: -1]

        self.csv_input = self.csvfolder + self.csvnum + os.sep + self.csvname + self.csvnum + self.csvend
        print self.csv_input + '\n'

        self.csv_output = atag.VAR_LOCAL_DATABASE + os.sep + atag.VAR_MY_CSV_NAME + ".csv"

        with open(self.csv_input, 'r') as f:
            for line in f:
                self.process_read_line(line)

        print self.csv_output
        self.f = open(self.csv_output, "w")
        self.f = open(self.csv_output, "a")

        for l in self.dat :
            self.process_write_line(l)


    def process_read_line(self, line):
        l = line.split(",")
        z = []
        for x in l:
            x = x.rstrip("\n\r")
            z.append(x)
        self.dat.append(z)
        print z

    def process_write_line(self, line):
        try:
            int(line[self.FACE_X]) # are we looking at heading?
        except ValueError:
            return

        left = int(line[self.FACE_X])
        right = int(line[self.FACE_X]) + int(line[self.FACE_WIDTH])
        top = int(line[self.FACE_Y])
        bottom = int(line[self.FACE_Y]) + int(line[self.FACE_HEIGHT])
        width = int(line[self.FACE_WIDTH])
        height = int(line[self.FACE_HEIGHT])

        for y in range(2):

            for x in range(self.TOTAL_READ):
                if y == 0 :
                    self.f.write(line[x])

                elif y == 1 and x == self.FACE_X:
                    r = 0
                    if left - width > 0 : r = random.randint(0,left - width)
                    self.f.write(str(r))
                elif y == 1 and x == self.FACE_Y:
                    r = 0
                    if top - height > 0 : r = random.randint(0,top - height)
                    self.f.write(str(r))
                else:
                    self.f.write(line[x])

                if x < self.TOTAL_READ - 1:
                    self.f.write(",")
                elif y == 0:
                    #true
                    self.f.write(",1\n")
                elif y == 1:
                    #false
                    self.f.write(",0\n")