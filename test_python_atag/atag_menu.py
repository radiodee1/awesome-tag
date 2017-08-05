#!/usr/bin/python

import easygui

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk
import threading
import signal
import atag_dotfolder as atag
import atag_drawingarea as dra
import atag_csv_write as write
#import atag_csv_read_tf as read
import atag_csv_predict as predict
import atag_csv_draw as draw
import atag_csv as aa
import nn_record as record
import nn_loader as loader
import subprocess
import os
import sys

class Interface(Gtk.Window, atag.Dotfolder) :

    def __init__(self):
        atag.Dotfolder.__init__(self)
        Gtk.Window.__init__(self, title="Tag")

        self.a = aa.Enum()

        self.connect("destroy", self.exit)
        signal.signal(signal.SIGINT, self.signal_handler)
        self.p = None # process instance
        self.record = record.Record(self)

        self.set_border_width(10)

        if self.VAR_DIM_CONFIG == "" : self.VAR_DIM_CONFIG = 4
        self.predict_call_list = ["-pipeline","10"]
        self.dim_key_call_list = ["-dim-config", str(self.VAR_DIM_CONFIG)]
        self.list_predict_call_list = []
        self.train_list = []
        self.train_thread = None

        self.progress_text = ""
        self.list_filename = ""

        self.grid = Gtk.Grid()
        self.add(self.grid)

        ''' row 0 '''
        self.label = Gtk.Label(self.shorten(self.VAR_BASE_NAME))
        self.grid.attach(self.label, 0, 0, 1, 1)

        self.entry = Gtk.Entry()
        self.entry.set_text("")
        self.entry.connect("activate", self.enter_image_name_callback, self.VAR_BASE_NAME, self.FOLDER_BASE_NAME,
                           self.label)
        self.grid.attach(self.entry, 1, 0, 1, 1)

        self.button = Gtk.Button(label="Picker")
        self.button.set_sensitive(False)
        self.button.connect("clicked", self.on_image_name_button, self.VAR_BASE_NAME, self.FOLDER_BASE_NAME,
                            self.label)
        self.grid.attach(self.button, 2, 0, 1, 1)

        self.label = Gtk.Label("Checkpoint Base Name")
        self.grid.attach(self.label, 3, 0, 1, 1)

        ''' row 1  x '''
        '''
        self.label = Gtk.Label(self.shorten(self.VAR_CSV_FILE_SECOND))
        self.grid.attach(self.label, 0, 1, 1, 1)

        self.entry = Gtk.Entry()
        self.entry.set_text("")
        self.entry.connect("activate", self.enter_image_name_callback, self.VAR_CSV_FILE_SECOND, self.FOLDER_CSV_FILE_SECOND,
                           self.label)
        self.grid.attach(self.entry, 1, 1, 1, 1)

        self.button = Gtk.Button(label="Picker")
        self.button.connect("clicked", self.on_image_name_button, self.VAR_CSV_FILE_SECOND, self.FOLDER_CSV_FILE_SECOND,
                            self.label)
        self.grid.attach(self.button, 2, 1, 1, 1)

        self.label = Gtk.Label("Second CSV")
        self.grid.attach(self.label, 3, 1, 1, 1)
        '''

        ''' row 2  x '''
        '''
        self.label = Gtk.Label(self.shorten(self.VAR_CSV_FILE_SINGLE))
        self.grid.attach(self.label, 0, 2, 1, 1)

        self.entry = Gtk.Entry()
        self.entry.set_text("")
        self.entry.connect("activate", self.enter_image_name_callback, self.VAR_CSV_FILE_SINGLE, self.FOLDER_CSV_FILE_SINGLE,
                           self.label)
        self.grid.attach(self.entry, 1, 2, 1, 1)

        self.button = Gtk.Button(label="Picker")
        self.button.connect("clicked", self.on_image_name_button, self.VAR_CSV_FILE_SINGLE, self.FOLDER_CSV_FILE_SINGLE,
                            self.label)
        self.grid.attach(self.button, 2, 2, 1, 1)

        self.label = Gtk.Label("Single CSV")
        self.grid.attach(self.label, 3, 2, 1, 1)
        '''

        ''' row 3 '''
        self.label = Gtk.Label(self.shorten(self.VAR_IMAGE_NAME))
        self.grid.attach(self.label, 0, 3, 1, 1)
        self.label_image = self.label

        self.entry = Gtk.Entry()
        self.entry.set_text("")
        self.entry.connect("activate", self.enter_image_name_callback, self.VAR_IMAGE_NAME, self.FOLDER_IMAGE_NAME,
                           self.label)
        self.grid.attach(self.entry, 1, 3, 1, 1)

        self.button = Gtk.Button(label="Picker")
        self.button.connect("clicked", self.on_image_name_button, self.VAR_IMAGE_NAME, self.FOLDER_IMAGE_NAME,
                            self.label)
        self.grid.attach(self.button, 2, 3, 1, 1)

        self.label = Gtk.Label("Sample Image")
        self.grid.attach(self.label, 3, 3, 1, 1)

        ''' row 4 '''
        self.label = Gtk.Label(self.shorten(self.VAR_LOCAL_DATABASE))
        self.grid.attach(self.label, 0, 4, 1, 1)

        self.entry = Gtk.Entry()
        self.entry.set_text("")
        self.entry.connect("activate", self.enter_image_name_callback, self.VAR_LOCAL_DATABASE, self.FOLDER_LOCAL_DATABASE,
                           self.label)
        self.grid.attach(self.entry, 1, 4, 1, 1)

        self.button = Gtk.Button(label="Picker")
        self.button.connect("clicked", self.on_image_folder_button, self.VAR_LOCAL_DATABASE, self.FOLDER_LOCAL_DATABASE,
                            self.label)
        self.grid.attach(self.button, 2, 4, 1, 1)

        self.label = Gtk.Label("Local Folder")
        self.grid.attach(self.label, 3, 4, 1, 1)

        ''' row 5 '''
        self.label = Gtk.Label(self.shorten(self.VAR_MY_CSV_NAME))
        self.grid.attach(self.label, 0, 5, 1, 1)

        self.entry = Gtk.Entry()
        self.entry.set_text("")
        self.entry.connect("activate", self.enter_image_name_callback, self.VAR_MY_CSV_NAME, self.FOLDER_MY_CSV_NAME,
                           self.label)
        self.grid.attach(self.entry, 1, 5, 1, 1)

        self.button = Gtk.Button(label="Picker")
        self.button.set_sensitive(False)
        self.button.connect("clicked", self.on_image_name_button, self.VAR_MY_CSV_NAME, self.FOLDER_MY_CSV_NAME,
                            self.label)
        self.grid.attach(self.button, 2, 5, 1, 1)

        self.label = Gtk.Label(" Base Name For ATAG CSV")
        self.grid.attach(self.label, 3, 5, 1, 1)

        ''' row 6 '''
        self.label = Gtk.Label(self.shorten(self.VAR_ROOT_DATABASE))
        self.grid.attach(self.label, 0, 6, 1, 1)

        self.entry = Gtk.Entry()
        self.entry.set_text("")
        self.entry.connect("activate", self.enter_image_name_callback, self.VAR_ROOT_DATABASE, self.FOLDER_ROOT_DATABASE,
                           self.label)
        self.grid.attach(self.entry, 1, 6, 1, 1)

        self.button = Gtk.Button(label="Picker")
        self.button.connect("clicked", self.on_image_folder_button, self.VAR_ROOT_DATABASE, self.FOLDER_ROOT_DATABASE,
                            self.label)
        self.grid.attach(self.button, 2, 6, 1, 1)

        self.label = Gtk.Label("Root Database")
        self.grid.attach(self.label, 3, 6, 1, 1)

        ''' row 7  x '''
        '''
        self.label = Gtk.Label(self.shorten(self.VAR_SAVED_CURSOR))
        self.grid.attach(self.label, 0, 7, 1, 1)

        self.entry = Gtk.Entry()
        self.entry.set_text("")
        self.entry.connect("activate", self.enter_image_name_callback, self.VAR_SAVED_CURSOR, self.FOLDER_SAVED_CURSOR,
                           self.label)
        self.grid.attach(self.entry, 1, 7, 1, 1)

        self.button = Gtk.Button(label="Picker")
        self.button.set_sensitive(False)
        self.button.connect("clicked", self.on_image_name_button, self.VAR_SAVED_CURSOR, self.FOLDER_SAVED_CURSOR,
                            self.label)
        self.grid.attach(self.button, 2, 7, 1, 1)

        self.label = Gtk.Label("Saved Cursor Position (#)")
        self.grid.attach(self.label, 3, 7, 1, 1)
        '''

        ''' row 8  x '''
        '''
        self.label = Gtk.Label(self.shorten(self.VAR_SAVED_SPLIT))
        self.grid.attach(self.label, 0, 8, 1, 1)

        self.entry = Gtk.Entry()
        self.entry.set_text("")
        self.entry.connect("activate", self.enter_image_name_callback, self.VAR_SAVED_SPLIT, self.FOLDER_SAVED_SPLIT,
                           self.label)
        self.grid.attach(self.entry, 1, 8, 1, 1)

        self.button = Gtk.Button(label="Picker")
        self.button.set_sensitive(False)
        self.button.connect("clicked", self.on_image_name_button, self.VAR_SAVED_SPLIT, self.FOLDER_SAVED_SPLIT,
                            self.label)
        self.grid.attach(self.button, 2, 8, 1, 1)

        self.label = Gtk.Label("Saved Split (#)")
        self.grid.attach(self.label, 3, 8, 1, 1)
        '''

        ''' row 9 '''
        
        if self.VAR_SPLIT_CURRENT == '' :
            self.VAR_SPLIT_CURRENT = '0'
        self.label = Gtk.Label(self.shorten(self.VAR_SPLIT_CURRENT))
        self.grid.attach(self.label, 0, 9, 1, 1)

        self.spin = Gtk.SpinButton()
        self.spin_adjust = Gtk.Adjustment(int(self.VAR_SPLIT_CURRENT),0,100,1,10,0)
        self.spin.set_adjustment(self.spin_adjust)
        policy = Gtk.SpinButtonUpdatePolicy.IF_VALID
        self.spin.set_update_policy(policy)
        self.spin.set_numeric(True)
        self.spin.connect("value-changed", self.on_spinner_change, self.VAR_SPLIT_CURRENT, self.FOLDER_SPLIT_CURRENT,
                          self.label)
        self.grid.attach(self.spin, 1, 9, 2, 1)


        self.label = Gtk.Label("Current Split (#)")
        self.grid.attach(self.label, 3, 9, 1, 1)

        ''' row 10  x '''
        '''
        self.label = Gtk.Label(self.shorten(self.VAR_SPLIT_END))
        self.grid.attach(self.label, 0, 10, 1, 1)

        self.entry = Gtk.Entry()
        self.entry.set_text("")
        self.entry.connect("activate", self.enter_image_name_callback, self.VAR_SPLIT_END, self.FOLDER_SPLIT_END,
                           self.label)
        self.grid.attach(self.entry, 1, 10, 1, 1)

        self.button = Gtk.Button(label="Picker")
        self.button.set_sensitive(False)
        self.button.connect("clicked", self.on_image_name_button, self.VAR_SPLIT_END, self.FOLDER_SPLIT_END,
                            self.label)
        self.grid.attach(self.button, 2, 10, 1, 1)

        self.label = Gtk.Label("Split End (#)")
        self.grid.attach(self.label, 3, 10, 1, 1)
        '''

        ''' row 11 '''
        position12 = 12
        self.label = Gtk.Label(self.shorten(self.VAR_SPLIT_FOLDER_NAME))
        self.grid.attach(self.label, 0, position12, 1, 1)

        self.entry = Gtk.Entry()
        self.entry.set_text("")
        self.entry.connect("activate", self.enter_image_name_callback, self.VAR_SPLIT_FOLDER_NAME, self.FOLDER_SPLIT_FOLDER_NAME,
                           self.label)
        self.grid.attach(self.entry, 1, position12, 1, 1)

        self.button = Gtk.Button(label="Picker")
        self.button.connect("clicked", self.on_image_folder_button, self.VAR_SPLIT_FOLDER_NAME, self.FOLDER_SPLIT_FOLDER_NAME,
                            self.label)
        self.grid.attach(self.button, 2, position12, 1, 1)

        self.label = Gtk.Label("Split Folder for Base Name")
        self.grid.attach(self.label, 3, position12, 1, 1)

        ''' row 12  x '''
        '''
        position11 = 11
        self.label = Gtk.Label(self.shorten(self.VAR_SPLIT_START))
        self.grid.attach(self.label, 0, position11, 1, 1)

        self.entry = Gtk.Entry()
        self.entry.set_text("")
        self.entry.connect("activate", self.enter_image_name_callback, self.VAR_SPLIT_START, self.FOLDER_SPLIT_START,
                           self.label)
        self.grid.attach(self.entry, 1, position11, 1, 1)

        self.button = Gtk.Button(label="Picker")
        self.button.set_sensitive(False)
        self.button.connect("clicked", self.on_image_name_button, self.VAR_SPLIT_START, self.FOLDER_SPLIT_START,
                            self.label)
        self.grid.attach(self.button, 2, position11, 1, 1)

        self.label = Gtk.Label("Split Start (#)")
        self.grid.attach(self.label, 3, position11, 1, 1)
        '''

        ''' some buttons in one row '''
        self.grid2 = Gtk.Grid()
        self.grid2.set_border_width(10)

        self.button = Gtk.Button(label="Show Boxes")
        self.button.connect("clicked", self.on_button_show_csv)
        self.grid2.attach(self.button, 0, 0, 1, 1)
        self.button = Gtk.Button(label="Read And Write CSV")
        self.button.connect("clicked", self.on_button_write_csv)
        self.grid2.attach(self.button, 1, 0, 1, 1)
        self.button = Gtk.Button(label="Train")
        self.button.connect("clicked", self.on_button_train)
        self.grid2.attach(self.button, 2, 0, 1, 1)
        self.button = Gtk.Button(label="Test")
        self.button.connect("clicked", self.on_button_options)
        self.grid2.attach(self.button, 3, 0, 1, 1)
        self.button = Gtk.Button(label="Predict")
        self.button.connect("clicked", self.on_button_test)
        self.grid2.attach(self.button, 4, 0, 1, 1)
        self.button = Gtk.Button(label="More")
        self.button.connect("clicked", self.on_button_more)
        self.grid2.attach(self.button, 5, 0, 1, 1)
        self.button = Gtk.Button(label="List")
        self.button.connect("clicked", self.on_button_list)
        self.grid2.attach(self.button, 6, 0, 1, 1)
        self.button = Gtk.Button(label="Stop")
        self.button.connect("clicked", self.on_button_stop)
        self.grid2.attach(self.button, 7, 0, 1, 1)

        self.grid.attach(self.grid2, 0, 13, 4,1)

        ''' end of list -- add drawingarea '''
        self.grid3 = Gtk.Grid()

        self.viewport = Gtk.ScrolledWindow()
        self.viewport.set_size_request(500,500)
        self.viewport.set_hexpand(True)
        self.viewport.set_vexpand(True)
        self.drawingarea = dra.DrawingArea()
        self.drawingarea.set_imagename(self.VAR_IMAGE_NAME)
        self.viewport.add(self.drawingarea)

        vadjustment = self.viewport.get_vadjustment()
        hadjustment = self.viewport.get_hadjustment()

        vscrollbar = Gtk.Scrollbar(orientation=Gtk.Orientation.VERTICAL, adjustment=vadjustment)
        hscrollbar = Gtk.Scrollbar(orientation=Gtk.Orientation.HORIZONTAL, adjustment=hadjustment)
        vscrollbar.set_adjustment(vadjustment)
        hscrollbar.set_adjustment(hadjustment)
        self.grid3.attach(self.viewport, 1, 1, 1, 1)
        self.grid3.attach(hscrollbar, 1, 0, 2, 1)
        self.grid3.attach(vscrollbar, 0, 1, 1, 2)

        self.grid.attach(self.grid3, 0, 14, 4, 1)

        ''' progress text '''
        self.progress_label = Gtk.Label()
        self.grid.attach(self.progress_label, 0, 15, 4, 1)
        self.set_progress_text("started")

    ''' button callback '''
    def on_button_show_csv(self, widget):
        self.run_draw_compile()
        #print 1

    def on_button_write_csv(self, widget):
        thread = threading.Thread(target=self.run_csv_write)
        thread.daemon = True
        thread.start()
        print 2

    def on_button_train(self, widget):
        #self.run_csv_read()
        self.ii = easygui.buttonbox("Type of training", "Choose", choices=("SKIN", "CONVOLUTION", "ZERO-COUNTERS", "CANCEL"))
        print "run from command line!"
        if self.ii == "SKIN":
            self.ii = "-dot-only"
        elif self.ii == "CONVOLUTION":
            self.ii = "-conv-only"
        elif self.ii == "ZERO-COUNTERS":
            self.dot_write(self.FOLDER_SAVED_CURSOR_DOT, str(0))
            self.dot_write(self.FOLDER_SAVED_CURSOR_CONV, str(0))
            return
        elif self.ii == "CANCEL":
            return


        thread = threading.Thread(target=self.run_csv_read)
        thread.daemon = True
        thread.start()
        print 3

    def on_button_test(self, widget):
        print 4
        thread = threading.Thread(target=self.run_predict_single_image)
        thread.daemon = False
        thread.start()


    def on_button_options(self, widget):
        print 5
        ii = easygui.buttonbox("Test Only, Etc.","Choose",choices=("SKIN","CONVOLUTION","CANCEL"))
        print "run from command line!"
        if ii == "SKIN":
            subprocess.call(["python", "./nn_launch_train.py", "-dot-only", "-test", "-no-save"])
        elif ii == "CONVOLUTION":
            subprocess.call(["python", "./nn_launch_train.py", "-conv-only", "-test", "-no-save"])

    def on_spinner_change(self, widget, var, folder, label):
        print 6
        result = self.spin.get_value_as_int()
        #print result
        self.enter_image_name_callback(widget,var,folder,label)

    def on_button_more(self, widget):
        ii = easygui.buttonbox("Further Options","Choose",choices=("PIPELINE","SET-DIM","RESET-CURSOR","SHOW-WEIGHTS","CANCEL"))
        if ii == "PIPELINE":
            jj = easygui.buttonbox("Pipeline Options","Choose",choices=("1","2","3","4","5","6","7"))
            self.predict_call_list = ["-pipeline", str(jj)]
            print self.predict_call_list
            self.set_progress_text("started")
            pass
        if ii == "SET-DIM":
            jj = easygui.buttonbox("Dimension Options","Program Will Quit",choices=("0","1","2","3","4","5","6","7"))
            self.dim_key_call_list = ["-dim-config", str(jj)]
            #print self.dim_key_call_list
            self.dot_write(self.FOLDER_DIM_CONFIG, str(jj))
            self.exit(None)
            #self.set_progress_text("started")
            pass
        if ii == "RESET-CURSOR":
            jj = easygui.buttonbox("Training Cursor To Reset On Next Run!","Choose",choices=("SKIN","CONVOLUTION","CANCEL"))
            if jj == "SKIN":
                pass
                self.train_list = "-zero-dot"
            if jj == "CONVOLUTION":
                pass
                self.train_list = "-zero-conv"
            pass
            call = ["python", "./nn_launch_train.py", self.train_list]
            subprocess.call(call)
        if ii == "SHOW-WEIGHTS" :
            pass
            call = ["python", "./nn_launch_train.py", "-weight-img"]
            subprocess.call(call)
        print 7
        pass

    def on_button_list(self, widget):

        p = predict.PredictRead(self)
        p.filename = self.VAR_IMAGE_NAME
        p.read_predict_list()
        self.set_progress_text("List:" + str(p.external_count + 1))
        print "short list length", len(p.dat), p.external_count + 1


        ii = easygui.buttonbox("List Viewing Options","Choose",choices=("FIRST","NEXT","PREV","LAUNCH","CANCEL"))
        if ii == "CANCEL" : return

        if ii == "FIRST": self.VAR_IMAGE_NAME = p.predict_first(self.VAR_IMAGE_NAME)
        if ii == "NEXT" : self.VAR_IMAGE_NAME = p.predict_next(self.VAR_IMAGE_NAME)
        if ii == "PREV" : self.VAR_IMAGE_NAME = p.predict_prev(self.VAR_IMAGE_NAME)
        if ii == "NEXT" or ii == "PREV" or ii == "FIRST" :
            self.set_progress_text("List:" + str(p.external_count+1))
            r = draw.Read(self)
            folder = self.FOLDER_IMAGE_NAME
            var = self.VAR_IMAGE_NAME
            print var, "new image"
            self.dot_write(folder, var)

            self.label_image.set_text(self.shorten(var))
            self.switch_folder_var(folder, var)

            self.drawingarea.set_imagename(self.VAR_IMAGE_NAME)

            r.process_read_file_predict_list()
            self.drawingarea.boxlist_red = r.boxlist_r
            self.drawingarea.boxlist_green = r.boxlist_g
            self.drawingarea.boxlist_blue = r.boxlist_b

            self.drawingarea.queue_draw()
        if ii == "LAUNCH":
            jj = easygui.buttonbox("Number of Pictures","Choose",choices=("2","5","10","50","100","CANCEL"))
            if jj != "CANCEL":
                if False:
                    pass
                    '''
                    call =  ["python", "./nn_launch_train.py", "-make-list", str(jj)]
                    self.p = subprocess.Popen(call)
                    '''
                elif True:
                    self.list_predict_call_list = ["-make-list", "1"]
                    thread = threading.Thread(target=self.run_predict_list_images, kwargs={"num":int(jj)})

                    thread.daemon = True
                    thread.start()

        print 8
        pass

    def on_button_stop(self, widget):
        if self.p != None:
            try:
                self.p.send_signal(signal.SIGINT)
            except:
                print "stop signal"

        pass

    ''' threading etc '''
    def run_draw_compile(self):
        ii = easygui.buttonbox("Type of Diagram","Choose",choices=("CONVOLUTION","INSET","DOT","PREDICT","[CLEAR]","LIST"))
        r = draw.Read(self)
        self.drawingarea.draw_enum = self.drawingarea.ENUM_BOXES
        if ii == "CONVOLUTION" :
            r.process_read_file_simple()
            self.drawingarea.boxlist_red = r.boxlist_r
        elif ii == "PREDICT" :
            r.process_read_file_predict()
            self.drawingarea.boxlist_red = r.boxlist_r
            self.drawingarea.boxlist_green = r.boxlist_g
            self.drawingarea.boxlist_blue = r.boxlist_b
            print self.drawingarea.boxlist_red, "red"
        elif ii == "DOT" :
            pass
            r.process_read_file_dot()
            self.drawingarea.boxlist_red = r.boxlist_r
        elif ii == "LIST":
            r.process_read_file_predict_list()
            self.drawingarea.boxlist_red = r.boxlist_r
            self.drawingarea.boxlist_green = r.boxlist_g
            self.drawingarea.boxlist_blue = r.boxlist_b
        elif ii == "INSET":
            ii = easygui.buttonbox("Number of Diagram", "Choose",
                                   choices=("0", "1", "2", "3", "4","5","6","7", "CANCEL"))
            if ii == "CANCEL" :
                self.drawingarea.queue_draw()
                return
            skin, img, three = r.process_read_file_convolution_in_depth(num=(int(ii) * 2 - 1))
            #print three
            self.drawingarea.set_gradient_info(skin, img, three)
            pass
        elif ii == "[CLEAR]":
            self.record.save_dat_to_list_file()
            self.drawingarea.boxlist_red = []
            self.drawingarea.boxlist_green = []
            self.drawingarea.boxlist_blue = []
            pass
        self.drawingarea.queue_draw()

    def run_csv_write(self):
        write.Write(self)

    def run_csv_read(self):
        #read.Read(self)
        #ii = easygui.buttonbox("Type of training","Choose", choices=("SKIN","CONVOLUTION"))
        print "run from command line!"

        call = ["python","./nn_launch_train.py",self.ii,"-train","-test"]

        self.train_list = ""
        print call
        self.p = subprocess.Popen(call)

        if False:
            self.train_thread = subprocess.Popen(call, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True, preexec_fn=os.setsid)

            while self.train_thread.poll() is None:
                out = self.train_thread.stdout.read(1)
                sys.stdout.write(out)
                sys.stdout.flush()

    def run_predict_single_image(self):
        call = ["python", "./nn_launch_train.py", str(self.VAR_IMAGE_NAME[:])]
        print call, "single_image"
        call.extend(self.predict_call_list)
        call.extend(self.dim_key_call_list)
        call.extend(self.list_predict_call_list)
        # print call
        self.p = subprocess.Popen(call)
        self.p.wait()
        #print "waited"
        r = draw.Read(self)
        r.process_read_file_predict_list()
        self.drawingarea.boxlist_red = r.boxlist_r
        self.drawingarea.boxlist_green = r.boxlist_g
        self.drawingarea.boxlist_blue = r.boxlist_b
        self.drawingarea.queue_draw()

        pass

    def run_predict_list_images(self, num):
        jj = num
        p = predict.PredictRead(self)
        p.read_skipping_repeats()

        list_dat = p.dat_no_repeat
        self.image_folder = self.VAR_ROOT_DATABASE


        for i in range(int(jj)):
            iterfile = i
            self.list_filename = list_dat[iterfile][self.a.FILE]
            if not self.list_filename.startswith(self.image_folder + os.sep) and not (
                    self.list_filename.startswith(os.sep)):
                self.list_filename = self.image_folder + os.sep + self.list_filename
            #print self.list_filename, list_dat[iterfile], "list_filename"
            self.dot_write(self.FOLDER_IMAGE_NAME, self.list_filename)
            self.VAR_IMAGE_NAME = self.list_filename
            self.drawingarea.set_imagename(self.VAR_IMAGE_NAME)
            self.drawingarea.queue_draw()
            self.run_predict_single_image()
        pass
        self.list_predict_call_list = []


    ''' utility and atag var callback '''
    def set_progress_text(self, text):
        self.progress_label.set_text("Dimension Configuration:"+self.dim_key_call_list[1] +",Pipeline:" +self.predict_call_list[1] +", Progress: "+ text)

    def show_window(self):
        win = self  # Interface()
        win.connect("delete-event", Gtk.main_quit)
        win.show_all()
        Gtk.main()


    def enter_image_name_callback(self, widget, var, folder, label):
        var = widget.get_text()
        self.dot_write(folder, var)
        #self.entry.set_text(self.shorten(var))
        label.set_text(self.shorten(var))
        self.switch_folder_var(folder,var)

    def on_image_name_button(self, widget, var, folder, label):
        temp = easygui.fileopenbox(msg="pick a file",title="FILE")
        if len(temp) > 0:
            var = str(temp)
            self.dot_write(folder, var)
            #self.entry.set_text(self.shorten(var))
            label.set_text(self.shorten(var))
            self.switch_folder_var(folder,var)

    def on_image_folder_button(self, widget, var, folder, label):
        temp = easygui.diropenbox(msg="pick a folder", title="FOLDER")
        if len(temp) > 0:
            var = str(temp)
            self.dot_write(folder, var)
            #self.entry.set_text(self.shorten(var))
            label.set_text(self.shorten(var))
            self.switch_folder_var(folder,var)

    def shorten(self, input):
        if len(input) < 25 : return input
        return "..." + input[-25:]

    def switch_folder_var(self, folder, var):
        if folder == self.FOLDER_BASE_NAME :
            self.VAR_BASE_NAME = var
        if folder == self.FOLDER_CSV_FILE_SECOND :
            self.VAR_CSV_FILE_SECOND = var
        if folder == self.FOLDER_CSV_FILE_SINGLE :
            self.VAR_CSV_FILE_SINGLE = var
        if folder == self.FOLDER_IMAGE_NAME :
            self.VAR_IMAGE_NAME = var
            self.drawingarea.set_imagename(var)
            self.drawingarea.queue_draw()
        if folder == self.FOLDER_LOCAL_DATABASE :
            self.VAR_LOCAL_DATABASE = var
        if folder == self.FOLDER_MY_CSV_NAME :
            self.VAR_MY_CSV_NAME = var
        if folder == self.FOLDER_ROOT_DATABASE :
            self.VAR_ROOT_DATABASE = var
        if folder == self.FOLDER_SAVED_CURSOR :
            self.VAR_SAVED_CURSOR = var
        if folder == self.FOLDER_SAVED_SPLIT:
            self.VAR_SAVED_SPLIT = var
        if folder == self.FOLDER_SPLIT_CURRENT :
            self.VAR_SPLIT_CURRENT = var
        if folder == self.FOLDER_SPLIT_END :
            self.VAR_SPLIT_END = var
        if folder == self.FOLDER_SPLIT_FOLDER_NAME :
            self.VAR_SPLIT_FOLDER_NAME = var
        if folder == self.FOLDER_SPLIT_START :
            self.VAR_SPLIT_START = var

    def signal_handler(self, signum, frame):
        #if self.nn.save_ckpt:
        #    self.nn.save_group()
        Gtk.main_quit()
        sys.exit()

    def exit(self, widget):
        if self.p != None:
            try:
                self.p.send_signal(signal.SIGINT)
            except :
                print "must be predict operation"
        print "exit here"
        Gtk.main_quit()
        sys.exit()

if __name__ == '__main__':
    d = Interface()
    d.show_window()
    #d.connect("delete-event", d.exit)
    #d.dot_write(d.FOLDER_IMAGE_NAME, "/home/dave/image.png")
    #print (d.dot_read(d.FOLDER_IMAGE_NAME))
    #d.VAR_IMAGE_NAME = d.dot_read(d.FOLDER_IMAGE_NAME)
    #print d.VAR_IMAGE_NAME
    print("done")
