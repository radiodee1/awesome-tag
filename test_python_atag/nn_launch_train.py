#!/usr/bin/python

import os
import signal
import sys
import atag_csv as enum
import nn_loader as loader
import atag_dotfolder as aa
#import nn_model as model
#import nn_kmeans as kmeans
import argparse

'''
Here we read the csv file that we made and train the models. NOTE: nn_model is imported BELOW.
'''

class Read( enum.Enum) :
    def __init__(self, atag, pic):
        enum.Enum.__init__(self)

        self.pic = pic

        self.a = atag

        self.nn = model.NN(self.a)

        self.dot_only = False
        self.conv_only = False

        self.pipeline_stage = 10

        self.predict_mc = False

    def run_nn(self):

        self.check_folder_exists()

        ll = loader.Load(self.a, self.pic)
        #ll.read_csv()

        signal.signal(signal.SIGINT, self.signal_handler)

        self.nn.set_loader(ll)

        switch = False
        if switch:
            self.dot_only = True
            self.conv_only = False
            self.nn.load_ckpt = True
            self.nn.save_ckpt = True
            self.nn.train = False
            self.nn.test = True

        if self.dot_only :
            pass
            ll.csv_input = self.a.VAR_LOCAL_DATABASE + os.sep + self.a.VAR_MY_CSV_NAME + ".dot.csv"
            ll.read_csv()

            self.nn.set_vars(len(ll.dat), 100, 0)
            self.nn.dot_setup()
            self.a.dot_write(a.FOLDER_SAVED_CURSOR_DOT, str(0))

        if self.conv_only :
            ll.csv_input = self.a.VAR_LOCAL_DATABASE + os.sep + self.a.VAR_MY_CSV_NAME + ".csv"
            ll.read_csv()

            #self.nn.set_vars(len(ll.dat), 100, 0)
            #self.nn.skintone_setup()

            self.nn.set_vars(len(ll.dat), 100, 0)
            self.nn.conv_setup()
            self.a.dot_write(a.FOLDER_SAVED_CURSOR_CONV, str(0))

    def run_predict(self):
        self.check_folder_exists()

        ll = loader.Load(self.a, self.pic)

        self.nn.load_ckpt = True
        self.nn.save_ckpt = False
        self.nn.train = False
        self.nn.test = False
        self.nn.set_loader(ll)

        ''' make initial box grid '''
        if not  self.predict_mc and self.pipeline_stage >= 1:
            ll.dat = ll.record.make_boxes(self.pic, dim=4) # 7
            print "num-boxes", len(ll.dat)


        if not self.predict_mc and self.pipeline_stage >=2:
            ''' initial simple neural network '''
            self.nn.predict_remove_symbol = 1
            self.nn.set_vars(len(ll.dat), 100, 0)
            self.nn.dot_setup()
            print "len-dat2", len(ll.dat)


        if not self.predict_mc and self.pipeline_stage >=3 :
            ''' two passes through aggregate function '''
            ll.dat = ll.record.aggregate_dat_list(ll.dat)
            ll.record.renumber_dat_list(ll.dat)
            ll.dat = ll.record.aggregate_dat_list(ll.dat, del_shapes=True)
            ll.record.renumber_dat_list(ll.dat)
            print "len-dat1", len(ll.dat)

        if self.pipeline_stage >=4 :
            ''' final convolution neural network '''
            self.nn.predict_remove_symbol = 1
            self.nn.set_vars(len(ll.dat), 100,  0)
            self.nn.conv_setup()
            print "len-dat2", len(ll.dat)

        if self.pipeline_stage >=5 :
            ''' try to improve box '''
            see_boxes = False
            if self.pipeline_stage == 5: see_boxes = True
            see_list = []
            self.nn.dat_best = []
            self.dat_mc = ll.dat[:]
            for k in range(len(self.dat_mc)):
                ll.dat = ll.record.make_boxes_mc(self.pic,dim=100 ,dat=[self.dat_mc[k]])
                ll.record.renumber_dat_list(ll.dat)
                if see_boxes: see_list.extend(ll.dat[:])

                self.nn.predict_remove_symbol = 1
                self.nn.set_vars(len(ll.dat), 100, 0)
                if not see_boxes: self.nn.conv_setup_mc()
            if not see_boxes: ll.dat = ll.record.renumber_dat_list(self.nn.dat_best)
            else : ll.dat = see_list[:]
            print "len-dat3", len(self.nn.dat_best)

        ll.record.save_dat_to_file(ll.dat)

    def run_weight_img(self):
        print "weight img"
        self.nn.conv_weight_img()
        pass

    def signal_handler(self, signum, frame):
        if self.nn.save_ckpt:
            self.nn.save_group()
        sys.exit()

    def check_folder_exists(self):
        folder = self.a.VAR_LOCAL_DATABASE + os.sep + "logs"
        #print folder
        if not os.path.exists(folder):
            os.makedirs(folder)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Train or Test ATAG neural network for facial detection in Python with Tensorflow.")
    parser.add_argument("filename", nargs="?")
    parser.add_argument("-train",   action="store_true")
    parser.add_argument("-test", action="store_true")
    parser.add_argument("-no-save", action="store_false")
    parser.add_argument("-no-load", action="store_false")
    parser.add_argument("-dot-only", action="store_true")
    parser.add_argument("-conv-only", action="store_true")
    parser.add_argument("-pipeline", nargs=1)
    parser.add_argument("-zero-dot", action="store_true")
    parser.add_argument("-zero-conv", action="store_true")
    parser.add_argument("-weight-img", action="store_true")

    args = parser.parse_args()
    print args
    #sys.exit()

    pic = ""
    #if len(sys.argv) > 1 :
    #    pic = str(sys.argv[1])
    if args.filename != None: pic = args.filename
    #print sys.argv
    print pic
    a = aa.Dotfolder()
    #r = Read(a, pic)

    if args.zero_dot and not args.test and not args.train:
        a.dot_write(a.FOLDER_SAVED_CURSOR_DOT, str(0))
        sys.exit()
        pass
    if args.zero_conv and not args.test and not args.train:
        a.dot_write(a.FOLDER_SAVED_CURSOR_CONV, str(0))
        sys.exit()
        pass

    import nn_model as model

    #a = aa.Dotfolder()
    r = Read(a, pic)
    if args.pipeline != None: r.pipeline_stage = int(args.pipeline[0])

    if len(pic) > 0 :
        ''' any combination '''
        r.nn.predict_softmax = True
        r.nn.predict_conv = True
        r.nn.predict_dot = True
        r.run_predict()
    elif args.weight_img == True:
        r.run_weight_img()
        pass
    else:
        r.nn.save_ckpt = args.no_save
        r.nn.load_ckpt = args.no_load
        r.nn.train = args.train
        r.nn.test = args.test
        r.dot_only = args.dot_only
        r.conv_only = args.conv_only
        r.run_nn()

    print "pipeline", r.pipeline_stage
    print("done")