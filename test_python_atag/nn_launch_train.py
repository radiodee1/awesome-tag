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
        #ll.read_csv()

        signal.signal(signal.SIGINT, self.signal_handler)


        self.nn.load_ckpt = True
        self.nn.save_ckpt = True
        self.nn.train = False
        self.nn.test = True
        self.nn.set_loader(ll)

        if True:
            pass
            ll.csv_input = self.a.VAR_LOCAL_DATABASE + os.sep + self.a.VAR_MY_CSV_NAME + ".dot.csv"
            ll.read_csv()

            self.nn.set_vars(len(ll.dat), 100, 0)
            self.nn.dot_setup()

        else:
            ll.csv_input = self.a.VAR_LOCAL_DATABASE + os.sep + self.a.VAR_MY_CSV_NAME + ".csv"
            ll.read_csv()

            #self.nn.set_vars(len(ll.dat), 100, 0)
            #self.nn.skintone_setup()

            self.nn.set_vars(len(ll.dat), 100, 0) #50, 'conv', 676
            self.nn.conv_setup()



    def run_predict(self):
        self.check_folder_exists()

        ll = loader.Load(self.a, self.pic)
        ll.read_csv()

        ll.dat = ll.record.make_boxes(self.pic, dim=7)

        self.nn.load_ckpt = True
        self.nn.save_ckpt = False
        self.nn.train = False
        self.nn.test = False
        self.nn.set_loader(ll)

        self.nn.predict_remove_symbol = 1

        self.nn.set_vars(len(ll.dat), 100, 0)
        self.nn.dot_setup()
        print "len-dat0", len(ll.dat)

        #self.nn.set_vars(len(ll.dat), 100, 0)
        #self.nn.skintone_setup()
        #print "len-dat1", len(ll.dat)

        ll.dat = ll.record.aggregate_dat_list(ll.dat)
        ll.record.renumber_dat_list(ll.dat)

        self.nn.predict_remove_symbol = 1
        self.nn.set_vars(len(ll.dat), 100,  0)  # 50, 'conv', 676
        self.nn.conv_setup()
        print "len-dat2", len(ll.dat)


        ll.record.save_dat_to_file()

    def signal_handler(self, signum, frame):
        self.nn.save_group()
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
    if len(pic) > 0 :
        r.nn.predict_softmax = True
        r.nn.predict_conv = True
        r.run_predict()
    else:
        r.run_nn()

    print("done")