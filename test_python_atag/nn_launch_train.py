#!/usr/bin/python

import os
import signal
import sys
import atag_csv as enum
import nn_loader as loader
import atag_dotfolder as aa
import nn_model as model


'''
Here we read the csv file that we made and train the models
'''

class Read( enum.Enum) :
    def __init__(self, atag, pic):
        enum.Enum.__init__(self)

        self.pic = pic

        self.a = atag

        self.nn = model.NN(self.a)

    def run_nn(self):

        self.check_folder_exists()

        ll = loader.Load(self.a, self.pic)


        signal.signal(signal.SIGINT, self.signal_handler)

        self.nn.load_ckpt = True
        self.nn.save_ckpt = True
        self.nn.train = True
        self.nn.test = True
        self.nn.set_loader(ll)

        #self.nn.predict_skintone = True
        #self.nn.set_vars(len(ll.dat), 100, "skin", 0)
        #self.nn.skintone_setup()


        self.nn.set_vars(len(ll.dat), 100, "softmax", 0)
        self.nn.softmax_setup()

        #self.nn.predict_conv = False
        #self.nn.set_vars(len(ll.dat), 50, "conv", 0)
        #self.nn.conv_setup()

    def signal_handler(self, signum, frame):
        self.nn.save()
        sys.exit()

    def check_folder_exists(self):
        folder = self.a.VAR_LOCAL_DATABASE + os.sep + "logs"
        #print folder
        if not os.path.exists(folder):
            os.makedirs(folder)

if __name__ == '__main__':

    pic = ""
    if len(sys.argv) > 1 :
        pic = str(sys.argv[1])
    print sys.argv
    print pic
    a = aa.Dotfolder()
    r = Read(a, pic)
    if len(pic) > 0 : r.nn.predict_softmax = True
    r.run_nn()

    print("done")