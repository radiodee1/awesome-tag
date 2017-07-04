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

        self.make_list = True
        self.list_end = 0
        self.list_dat = []

        self.image_folder = atag.VAR_ROOT_DATABASE


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

            self.nn.set_vars(len(ll.dat), 100, 0, adjust_x=self.nn.train)
            self.nn.conv_setup()
            self.a.dot_write(a.FOLDER_SAVED_CURSOR_CONV, str(0))

    def run_predict(self, picture):
        self.pic = picture
        self.check_folder_exists()

        ll = loader.Load(self.a, self.pic)

        self.nn.load_ckpt = True
        self.nn.save_ckpt = False
        self.nn.train = False
        self.nn.test = False
        self.nn.set_loader(ll)
        ll.special_horizontal_align = False

        ''' make initial box grid '''
        if self.pipeline_stage >= 1:
            ll.dat = ll.record.make_boxes(self.pic, dim=4) # 7
            print "num-boxes", len(ll.dat)


        if self.pipeline_stage >=2:
            ''' initial simple neural network '''
            self.nn.predict_remove_symbol = 1
            self.nn.set_vars(len(ll.dat), 100, 0)
            self.nn.dot_setup()
            print "len-dat2", len(ll.dat)


        if self.pipeline_stage >=3 :
            ''' two passes through aggregate box function '''
            ll.dat = ll.record.aggregate_dat_list(ll.dat)
            ll.record.renumber_dat_list(ll.dat)
            ll.dat = ll.record.aggregate_dat_list(ll.dat, del_shapes=True)
            ll.record.renumber_dat_list(ll.dat)
            print "len-dat1", len(ll.dat)

        if self.pipeline_stage >=4 :
            ''' final convolution neural network '''
            #ll.normal_train = False
            self.nn.predict_remove_symbol = 1
            self.nn.set_vars(len(ll.dat), 100,  0, adjust_x=True)
            self.nn.conv_setup()
            print "len-dat2", len(ll.dat)

        if self.pipeline_stage >=5 and True:
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
                self.nn.set_vars(len(ll.dat), 100, 0, adjust_x=True)
                if not see_boxes: self.nn.conv_setup_mc()
            if not see_boxes: ll.dat = ll.record.renumber_dat_list(self.nn.dat_best)
            else : ll.dat = see_list[:]
            print "len-dat3", len(self.nn.dat_best)

        ll.record.save_dat_to_file(ll.dat, erase=(not self.make_list))


    def run_weight_img(self):
        print "weight img"
        self.nn.conv_weight_img()
        pass

    def run_make_list(self):
        print "make list", self.list_end
        self.check_folder_exists()

        ll = loader.Load(self.a, "")
        ll.read_csv()
        self.list_dat = ll.dat[:]

        signal.signal(signal.SIGINT, self.signal_handler)

        predict_filename = self.a.VAR_LOCAL_DATABASE + os.sep + "predict-list" + ".csv"
        f = open(predict_filename, "w")
        f.write("")

        filename = ""
        filename_old = None
        iterate = 0
        iterfile = 0
        while iterate < self.list_end and iterfile < len(self.list_dat):
            filename = self.list_dat[iterfile][self.FILE]
            if not filename.startswith(self.image_folder + os.sep) and not (filename.startswith(os.sep)) :
                filename = self.image_folder + os.sep + filename
            print filename, self.list_dat[iterfile]
            #sys.exit()
            if filename != filename_old:
                self.run_predict(filename)
                iterate += 1
            filename_old = filename
            iterfile += 1
            print iterate, "make-list"
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
    parser.add_argument("-make-list", nargs=1)

    args = parser.parse_args()
    print args
    #sys.exit()

    pic = ""

    if args.filename != None: pic = args.filename
    #print sys.argv
    print pic
    a = aa.Dotfolder()

    if args.zero_dot and not args.test and not args.train:
        a.dot_write(a.FOLDER_SAVED_CURSOR_DOT, str(0))
        sys.exit()
        pass
    if args.zero_conv and not args.test and not args.train:
        a.dot_write(a.FOLDER_SAVED_CURSOR_CONV, str(0))
        sys.exit()
        pass

    import nn_model as model

    r = Read(a, pic)
    if args.pipeline != None: r.pipeline_stage = int(args.pipeline[0])

    if len(pic) > 0 :
        ''' any combination '''
        r.nn.predict_softmax = True
        r.nn.predict_conv = True
        r.nn.predict_dot = True
        r.run_predict(pic)
    elif args.weight_img == True:
        r.run_weight_img()
        pass
    elif args.make_list != None:
        r.nn.predict_softmax = True
        r.nn.predict_conv = True
        r.nn.predict_dot = True
        r.make_list = True
        r.list_end = int(args.make_list[0])
        r.run_make_list()
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