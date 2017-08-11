#!/usr/bin/python

import os
import signal
import sys
import atag_csv as enum
import nn_loader as loader
import atag_dotfolder as aa
import nn_dim as dim
import nn_model as model
#import nn_kmeans as kmeans
import argparse

'''
Here we read the csv file that we made and train the models. NOTE: nn_model is imported twice.
'''

class Read( enum.Enum, dim.Dimension) :
    def __init__(self, atag, pic):
        enum.Enum.__init__(self)
        dim.Dimension.__init__(self)

        self.pic = pic

        self.a = atag

        self.nn = model.NN(self.a)

        self.dot_only = False
        self.conv_only = False
        self.eye_only = False

        self.pipeline_stage = 10

        self.make_list = True
        self.list_end = 0
        self.list_dat = []

        self.image_folder = atag.VAR_ROOT_DATABASE
        self.pipeline_enum = self.DIMENSIONS[self.key][self.COLUMN_ENUM_PIPELINE]

        self.blue_boxes = True

    def run_nn(self):

        self.check_folder_exists()

        ll = loader.Load(self.a, self.pic)
        #ll.read_csv()

        signal.signal(signal.SIGINT, self.signal_handler)

        self.load_dot_only = self.DIMENSIONS[self.key][self.COLUMN_LOAD_DOT_CONV][0]
        self.load_conv_only = self.DIMENSIONS[self.key][self.COLUMN_LOAD_DOT_CONV][1]
        self.load_eye_only = False

        self.nn.set_loader(ll)
        self.zero_out_counter = False
        self.blue_boxes = True

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

            if self.load_dot_only == False and (self.load_conv_only == True or self.load_eye_only == True):
                sys.exit()
            elif self.load_conv_only == False and self.load_eye_only == False :
                self.nn.nn_clear_and_reset()
                self.nn.nn_configure_dot()
                self.nn.nn_global_var_init()

            self.nn.dot_setup()

            if self.zero_out_counter: self.a.dot_write(self.a.FOLDER_SAVED_CURSOR_DOT, str(0))

        if self.conv_only :
            ll.csv_input = self.a.VAR_LOCAL_DATABASE + os.sep + self.a.VAR_MY_CSV_NAME + ".csv"
            ll.read_csv()



            self.nn.set_vars(len(ll.dat), 100, 0, adjust_x=self.nn.train)

            if self.load_conv_only == False and (self.load_dot_only == True or self.load_eye_only == True):
                sys.exit()
            elif self.load_dot_only == False or self.load_eye_only == False :
                self.nn.nn_clear_and_reset()
                self.nn.nn_configure_conv()
                self.nn.nn_global_var_init()

            self.nn.load_ckpt = True
            self.nn.save_ckpt = True
            self.nn.conv_setup()

            if self.zero_out_counter: self.a.dot_write(self.a.FOLDER_SAVED_CURSOR_CONV, str(0))

        if self.eye_only :
            ll.csv_input = self.a.VAR_LOCAL_DATABASE + os.sep + self.a.VAR_MY_CSV_NAME + ".eye.csv"
            ll.read_csv()



            self.nn.set_vars(len(ll.dat), 100, 0, adjust_x=self.nn.train)

            if self.load_eye_only == False and (self.load_dot_only == True or self.load_conv_only == True):
                sys.exit()
            elif self.load_dot_only == False and self.load_conv_only == False:
                self.nn.nn_clear_and_reset()
                self.nn.nn_configure_eyes()
                self.nn.nn_global_var_init()

            self.nn.eye_setup()

            if self.zero_out_counter: self.a.dot_write(self.a.FOLDER_SAVED_CURSOR_CONV, str(0))


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

        if self.pipeline_enum == self.ENUM_PIPELINE_1:
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

            print "pipeline enum 1"
            ll.record.save_dat_to_file(ll.dat, erase=(not self.make_list))

        if self.pipeline_enum == self.ENUM_PIPELINE_2:
            ''' make initial box grid '''
            if self.pipeline_stage >= 1:
                ll.dat = ll.record.make_boxes(self.pic, dim=4)  # 7
                print "num-boxes", len(ll.dat)

            if self.pipeline_stage >= 2:
                ''' initial simple neural network '''
                self.nn.predict_remove_symbol = 1
                self.nn.set_vars(len(ll.dat), 100, 0)
                self.nn.dot_setup()
                print "len-dat2", len(ll.dat)

            if self.pipeline_stage >= 3:
                ''' two passes through aggregate box function '''
                ll.dat = ll.record.aggregate_dat_list(ll.dat)
                ll.record.renumber_dat_list(ll.dat)
                ll.dat = ll.record.aggregate_dat_list(ll.dat, del_shapes=True)
                ll.record.renumber_dat_list(ll.dat)
                print "len-dat1", len(ll.dat)

            if self.pipeline_stage >= 4 and True:
                ''' final convolution neural network '''
                # ll.normal_train = False
                self.nn.predict_remove_symbol = 1
                self.nn.set_vars(len(ll.dat), 100, 0, adjust_x=True)
                self.nn.conv_setup(remove_low=False)
                print "len-dat2", len(ll.dat)

            if self.pipeline_stage >= 5 and True:
                ''' try to improve box '''
                see_boxes = False
                if self.pipeline_stage == 5: see_boxes = True
                see_list = []
                self.nn.dat_best = []
                self.dat_mc = ll.dat[:]
                for k in range(len(self.dat_mc)):
                    ll.dat = ll.record.make_boxes_mc(self.pic, dim=100, dat=[self.dat_mc[k]])
                    ll.record.renumber_dat_list(ll.dat)
                    if see_boxes: see_list.extend(ll.dat[:])

                    self.nn.predict_remove_symbol = 1
                    self.nn.set_vars(len(ll.dat), 100, 0, adjust_x=True)
                    if not see_boxes: self.nn.conv_setup_mc(remove_low=False)
                if not see_boxes:
                    ll.dat = ll.record.renumber_dat_list(self.nn.dat_best)
                else:
                    ll.dat = see_list[:]
                print "len-dat3", len(self.nn.dat_best)

            print "pipeline enum 2"
            ll.record.save_dat_to_file(ll.dat, erase=(not self.make_list))

        if self.pipeline_enum == self.ENUM_PIPELINE_3:
            ''' make initial box grid '''
            if self.pipeline_stage >= 1:
                ll.dat = ll.record.make_boxes(self.pic, dim=-1, grid=10000 * 5)  # dim=4
                print "num-boxes", len(ll.dat)

            if self.pipeline_stage >= 2 and True:
                ''' initial simple neural network '''
                self.nn.nn_clear_and_reset()
                self.nn.nn_configure_dot()
                self.nn.nn_global_var_init()
                self.nn.predict_remove_symbol = 1
                self.nn.set_vars(len(ll.dat), 10 * 100, 0)
                self.nn.dot_setup()
                print "len-dat2", len(ll.dat)

            if self.pipeline_stage >= 3 and True:
                ''' new gpu aggregate box function '''
                if True:
                    self.nn.dat = ll.dat
                    self.nn.nn_clear_and_reset()
                    self.nn.nn_configure_assemble()
                    self.nn.nn_global_var_init()
                    self.nn.assemble_setup()
                    ll.dat = self.nn.dat

                    ll.record.renumber_dat_list(ll.dat)
                elif True:
                    ''' two passes through aggregate box function '''
                    ll.dat = ll.record.aggregate_dat_list(ll.dat)
                    ll.record.renumber_dat_list(ll.dat)
                    ll.dat = ll.record.aggregate_dat_list(ll.dat, del_shapes=True)
                    ll.record.renumber_dat_list(ll.dat)

                if self.blue_boxes: ll.record.save_dat_to_list_file(ll.dat, erase=False,color=self.BLUE)

                print "len-dat3", len(ll.dat)

            mc_experement = True

            if self.pipeline_stage >= 4 and not mc_experement:
                ''' convolution neural network '''
                self.nn.nn_clear_and_reset()
                self.nn.nn_configure_conv()
                self.nn.nn_global_var_init()
                # ll.normal_train = False
                self.nn.predict_remove_symbol = 1
                self.nn.set_vars(len(ll.dat), 100, 0, adjust_x=True)
                self.nn.load_ckpt = True
                self.nn.conv_setup(remove_low=False, color_reject=True)
                print "len-dat4", len(ll.dat)

            if self.pipeline_stage >= 5 and True:
                ''' try to improve box '''
                if mc_experement:
                    self.nn.nn_clear_and_reset()
                    self.nn.nn_configure_conv()
                    self.nn.nn_global_var_init()
                see_boxes = False
                self.nn.load_ckpt = True
                if self.pipeline_stage == 5: see_boxes = True
                see_list = []
                self.nn.dat_best = []
                self.dat_mc = ll.dat[:]
                ll.dat = []
                for k in range(len(self.dat_mc)):
                    ll.dat = ll.record.make_boxes_mc(self.pic, dim=200, dat=[self.dat_mc[k]])
                    ll.record.renumber_dat_list(ll.dat)
                    if see_boxes: see_list.extend(ll.dat[:])


                    self.nn.predict_remove_symbol = 1

                    self.nn.set_vars(len(ll.dat), 100, 0, adjust_x=True)
                    if not see_boxes: self.nn.conv_setup_mc(remove_low=mc_experement, color_reject=True)
                if not see_boxes:
                    pass
                    ll.dat = ll.record.renumber_dat_list(self.nn.dat_best)
                else:
                    ll.dat = see_list[:]
                print "len-dat5", len(self.nn.dat_best)

            print "pipeline enum 3"
            ll.record.save_dat_to_file(ll.dat, erase=(not self.make_list))

        if self.pipeline_enum == self.ENUM_PIPELINE_4:
            ''' make initial box grid '''
            if self.pipeline_stage >= 1:
                ll.dat = ll.record.make_boxes(self.pic, dim=-1, grid=1000 * 50)  # dim=4
                print "num-boxes", len(ll.dat)

            if self.pipeline_stage >= 2 and True:
                ''' initial simple neural network '''
                self.nn.nn_clear_and_reset()
                self.nn.nn_configure_dot()
                self.nn.nn_global_var_init()
                self.nn.predict_remove_symbol = 1
                self.nn.set_vars(len(ll.dat), 10 * 100, 0)
                self.nn.dot_setup()
                print "len-dat2", len(ll.dat)

            if self.pipeline_stage >= 3 and True:
                ''' new gpu aggregate box function '''
                if True:
                    self.nn.dat = ll.dat
                    self.nn.nn_clear_and_reset()
                    self.nn.nn_configure_assemble()
                    self.nn.nn_global_var_init()
                    self.nn.assemble_setup(use_gpu=True)
                    ll.dat = self.nn.dat

                    ll.record.renumber_dat_list(ll.dat)
                elif True:
                    ''' two passes through aggregate box function '''
                    ll.dat = ll.record.aggregate_dat_list(ll.dat)
                    ll.record.renumber_dat_list(ll.dat)
                    ll.dat = ll.record.aggregate_dat_list(ll.dat, del_shapes=True)
                    ll.record.renumber_dat_list(ll.dat)

                if self.blue_boxes and True: ll.record.save_dat_to_list_file(ll.dat, erase=False,color=self.BLUE)

                print "len-dat3", len(ll.dat)

            #mc_experement = True

            if self.pipeline_stage >= 4 and True:
                ''' try to improve box with eyes nn '''
                if True:# mc_experement:
                    self.nn.nn_clear_and_reset()
                    self.nn.nn_configure_eyes()
                    self.nn.nn_global_var_init()
                see_boxes = False
                self.nn.load_ckpt = True
                if self.pipeline_stage == 5: see_boxes = True
                see_list = []
                temp_list = []
                self.nn.dat_best = []
                self.dat_mc = ll.dat[:]
                #eyes_score = 0
                #eyes_index = 0
                for k in range(len(self.dat_mc)):
                    ll.dat = ll.record.make_boxes_mc(self.pic, dim=50, dat=[self.dat_mc[k]], skip_on_height=True)
                    ll.record.renumber_dat_list(ll.dat)
                    if see_boxes: see_list.extend(ll.dat[:])

                    self.nn.predict_remove_symbol = 1
                    eyes_score = - 10.0
                    eyes_index = -1
                    eye_list = []
                    self.nn.dat_eye = ll.dat[:] ##limit output here <---
                    if see_boxes: ll.record.save_dat_to_list_file(mc_list,erase=False, color="GREEN")
                    for j in range(len(self.nn.dat_eye)):
                        #print k, len(self.dat_mc), j, "progress"
                        eye_list = ll.record.make_boxes_eyes(self.pic, dat=[self.nn.dat_eye[j]],skip_on_height=True)
                        ll.dat = eye_list[:]
                        self.nn.set_vars(len(eye_list), 100, 0, adjust_x=True)
                        self.nn.predict_eye = True
                        self.nn.dat = self.dat_mc
                        if not see_boxes:
                            self.nn.eye_setup(remove_low=True, color_reject=True, index=j)

                            if self.nn.mc_score_eyes > eyes_score:
                                eyes_score = self.nn.mc_score_eyes
                                eyes_index = j
                            print eyes_index, k, "mc index <-------",eyes_score, len(self.nn.dat_eye), len(self.dat_mc)

                    if eyes_index != -1 and not self.nn.dat_eye[eyes_index] in temp_list:
                        print "use index", eyes_index
                        temp_list.append(self.nn.dat_eye[eyes_index])
                if not see_boxes:
                    pass
                    self.nn.dat_best = temp_list
                    ll.dat = ll.record.renumber_dat_list(self.nn.dat_best)
                else:
                    ll.dat = eye_list[:]
                    #ll.dat = see_list[:]
                print "len-dat4", len(self.nn.dat_best)


            if self.pipeline_stage >= 5 and True:  # not mc_experement:
                ''' convolution neural network '''
                self.nn.nn_clear_and_reset()
                self.nn.nn_configure_conv()
                self.nn.nn_global_var_init()
                # ll.normal_train = False
                self.nn.predict_remove_symbol = 1
                self.nn.set_vars(len(ll.dat), 100, 0, adjust_x=True)
                self.nn.load_ckpt = True
                self.nn.conv_setup(remove_low=False, color_reject=True)
                print "len-dat5", len(ll.dat)

            print "pipeline enum 4"
            ll.record.save_dat_to_list_file(ll.dat, erase=(not self.make_list), color=self.GREEN)

    def run_weight_img(self):
        print "weight img"
        self.nn.conv_weight_img()
        pass

    def run_make_list(self, pic=""):
        print "make list", self.list_end
        self.check_folder_exists()

        ll = loader.Load(self.a, "")
        ll.read_csv()
        self.list_dat = ll.dat[:]

        #self.list_dat = sorted(self.list_dat, key=lambda line: line[self.FILE].lower())
        #print "index", self.FILE, self.list_dat

        signal.signal(signal.SIGINT, self.signal_handler)

        predict_filename = self.a.VAR_LOCAL_DATABASE + os.sep + "predict-list" + ".csv"
        f = open(predict_filename, "a") # "w"
        f.write("")

        self.blue_boxes = False

        if len(pic) == 0:
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
        else:
            self.run_predict(pic)

    def signal_handler(self, signum, frame):
        if self.nn.save_ckpt:
            load_dot_only = self.DIMENSIONS[self.key][self.COLUMN_LOAD_DOT_CONV][0]
            load_conv_only = self.DIMENSIONS[self.key][self.COLUMN_LOAD_DOT_CONV][1]
            name = ""
            if not load_conv_only or not load_dot_only:
                pass
                if self.nn.dot_only: name = "dot"
                if self.nn.conv_only: name = "conv"
                if self.nn.eye_only: name = "eye"

            self.nn.save_group(graph_name=name)
        sys.exit()

    def check_folder_exists(self):
        folder = self.a.VAR_LOCAL_DATABASE + os.sep + "logs"
        #print folder
        if not os.path.exists(folder):
            os.makedirs(folder)


def main():
    parser = argparse.ArgumentParser(description="Train or Test ATAG neural network for facial detection in Python with Tensorflow.")
    parser.add_argument("filename", nargs="?")
    parser.add_argument("-train",   action="store_true")
    parser.add_argument("-test", action="store_true")
    parser.add_argument("-no-save", action="store_false")
    parser.add_argument("-no-load", action="store_false")
    parser.add_argument("-dot-only", action="store_true")
    parser.add_argument("-conv-only", action="store_true")
    parser.add_argument("-eyes-only", action="store_true")
    parser.add_argument("-pipeline", nargs=1)
    parser.add_argument("-zero-dot", action="store_true")
    parser.add_argument("-zero-conv", action="store_true")
    parser.add_argument("-weight-img", action="store_true")
    parser.add_argument("-make-list", nargs=1)
    parser.add_argument("-dim-config", nargs=1)

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

    if args.dim_config != None:
        a.dot_write(a.VAR_DIM_CONFIG, str(int(args.dim_config[0] ) ))
        r.nn.key = int(args.dim_config[0] )
        print int(args.dim_config[0] ) ,"dim_config"

    if len(pic) > 0 and args.make_list == None :
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
        #print r.list_end, "list_end", pic
        if r.list_end == 1 and len(pic) > 0: r.run_make_list(pic=pic)
        else:
            r.run_make_list()
    else:
        r.nn.save_ckpt = args.no_save
        r.nn.load_ckpt = args.no_load
        r.nn.train = args.train
        r.nn.test = args.test
        r.dot_only = args.dot_only
        r.conv_only = args.conv_only
        r.eye_only = args.eyes_only
        #r.load_correct_model(dim_version=a.VAR_DIM_CONFIG)
        r.run_nn()

    print "pipeline", r.pipeline_stage
    print("done")

if __name__ == '__main__':
    main()
