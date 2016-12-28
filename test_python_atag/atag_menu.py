#!/usr/bin/python

import easygui

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk
#import cairo
import threading

import atag_dotfolder as atag
import atag_drawingarea as dra
import atag_csv_write as write
#import atag_csv_read_tf as read
import atag_csv_draw as draw
import subprocess

class Interface(Gtk.Window, atag.Dotfolder) :

    def __init__(self):
        atag.Dotfolder.__init__(self)
        Gtk.Window.__init__(self, title="Tag")
        self.set_border_width(10)

        #self.image = cairo.ImageSurface.create_from_png(self.VAR_IMAGE_NAME)


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

        ''' row 1 '''
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

        ''' row 2 '''
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

        ''' row 3 '''
        self.label = Gtk.Label(self.shorten(self.VAR_IMAGE_NAME))
        self.grid.attach(self.label, 0, 3, 1, 1)

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

        ''' row 7 '''
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

        ''' row 8 '''
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

        ''' row 9 '''
        self.label = Gtk.Label(self.shorten(self.VAR_SPLIT_CURRENT))
        self.grid.attach(self.label, 0, 9, 1, 1)

        self.entry = Gtk.Entry()
        self.entry.set_text("")
        self.entry.connect("activate", self.enter_image_name_callback, self.VAR_SPLIT_CURRENT, self.FOLDER_SPLIT_CURRENT,
                           self.label)
        self.grid.attach(self.entry, 1, 9, 1, 1)

        self.button = Gtk.Button(label="Picker")
        self.button.set_sensitive(False)
        self.button.connect("clicked", self.on_image_name_button, self.VAR_SPLIT_CURRENT, self.FOLDER_SPLIT_CURRENT,
                            self.label)
        self.grid.attach(self.button, 2, 9, 1, 1)

        self.label = Gtk.Label("Current Split (#)")
        self.grid.attach(self.label, 3, 9, 1, 1)

        ''' row 10 '''
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

        self.label = Gtk.Label("Split Foldername")
        self.grid.attach(self.label, 3, position12, 1, 1)

        ''' row 12 '''
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

        ''' some buttons in one row '''
        self.grid2 = Gtk.Grid()

        self.button = Gtk.Button(label="Read CSV, Show Boxes")
        self.button.connect("clicked", self.on_button_show_csv)
        self.grid2.attach(self.button, 0, 0, 1, 1)
        self.button = Gtk.Button(label="Read And Write CSV")
        self.button.connect("clicked", self.on_button_write_csv)
        self.grid2.attach(self.button, 1, 0, 1, 1)
        self.button = Gtk.Button(label="Train")
        self.button.connect("clicked", self.on_button_train)
        self.grid2.attach(self.button, 2, 0, 1, 1)
        self.button = Gtk.Button(label="Predict")
        self.button.connect("clicked", self.on_button_test)
        self.grid2.attach(self.button, 3, 0, 1, 1)
        self.button = Gtk.Button(label="More Options")
        self.button.connect("clicked", self.on_button_options)
        self.grid2.attach(self.button, 4, 0, 1, 1)

        self.grid.attach(self.grid2, 0, 13, 4,1)

        ''' end of list -- add drawingarea '''
        self.drawingarea = dra.DrawingArea()
        self.drawingarea.set_imagename(self.VAR_IMAGE_NAME)
        #self.drawingarea.boxlist_red = draw.Read(self).boxlist

        self.grid.attach(self.drawingarea, 0, 14, 4, 1)

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
        thread = threading.Thread(target=self.run_csv_read)
        thread.daemon = True
        thread.start()
        print 3

    def on_button_test(self, widget):
        print 4
        subprocess.call(["python","./nn_launch_train.py",self.VAR_IMAGE_NAME])

    def on_button_options(self, widget):
        print 5

    ''' threading etc '''
    def run_draw_compile(self):
        ii = easygui.buttonbox("Type of Diagram","Choose",choices=("TRAIN","DOT","PREDICT"))
        r = draw.Read(self)
        if ii == "TRAIN" :
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
        self.drawingarea.queue_draw()

    def run_csv_write(self):
        write.Write(self)

    def run_csv_read(self):
        #read.Read(self)
        print "run from command line!"
        subprocess.call(["python","./nn_launch_train.py",""])

    ''' utility and atag var callback '''
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

if __name__ == '__main__':
    d = Interface()
    d.show_window()
    #d.dot_write(d.FOLDER_IMAGE_NAME, "/home/dave/image.png")
    #print (d.dot_read(d.FOLDER_IMAGE_NAME))
    #d.VAR_IMAGE_NAME = d.dot_read(d.FOLDER_IMAGE_NAME)
    #print d.VAR_IMAGE_NAME
    print("done")