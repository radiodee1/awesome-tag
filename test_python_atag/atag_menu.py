#!/usr/bin/python

import easygui

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk
import cairo

import atag_dotfolder as atag


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

        self.label = Gtk.Label("Base Name")
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
        self.button.connect("clicked", self.on_image_name_button, self.VAR_LOCAL_DATABASE, self.FOLDER_LOCAL_DATABASE,
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
        self.button.connect("clicked", self.on_image_name_button, self.VAR_ROOT_DATABASE, self.FOLDER_ROOT_DATABASE,
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

        self.label = Gtk.Label("Saved Cursor Position")
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

        self.label = Gtk.Label("Saved Split")
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

        self.label = Gtk.Label("Current Split")
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

        self.label = Gtk.Label("Split End")
        self.grid.attach(self.label, 3, 10, 1, 1)

        ''' row 11 '''
        self.label = Gtk.Label(self.shorten(self.VAR_SPLIT_FOLDER_NAME))
        self.grid.attach(self.label, 0, 11, 1, 1)

        self.entry = Gtk.Entry()
        self.entry.set_text("")
        self.entry.connect("activate", self.enter_image_name_callback, self.VAR_SPLIT_FOLDER_NAME, self.FOLDER_SPLIT_FOLDER_NAME,
                           self.label)
        self.grid.attach(self.entry, 1, 11, 1, 1)

        self.button = Gtk.Button(label="Picker")
        self.button.connect("clicked", self.on_image_name_button, self.VAR_SPLIT_FOLDER_NAME, self.FOLDER_SPLIT_FOLDER_NAME,
                            self.label)
        self.grid.attach(self.button, 2, 11, 1, 1)

        self.label = Gtk.Label("Split Foldername")
        self.grid.attach(self.label, 3, 11, 1, 1)

        ''' row 12 '''
        self.label = Gtk.Label(self.shorten(self.VAR_SPLIT_START))
        self.grid.attach(self.label, 0, 12, 1, 1)

        self.entry = Gtk.Entry()
        self.entry.set_text("")
        self.entry.connect("activate", self.enter_image_name_callback, self.VAR_SPLIT_START, self.FOLDER_SPLIT_START,
                           self.label)
        self.grid.attach(self.entry, 1, 12, 1, 1)

        self.button = Gtk.Button(label="Picker")
        self.button.set_sensitive(False)
        self.button.connect("clicked", self.on_image_name_button, self.VAR_SPLIT_START, self.FOLDER_SPLIT_START,
                            self.label)
        self.grid.attach(self.button, 2, 12, 1, 1)

        self.label = Gtk.Label("Split Start")
        self.grid.attach(self.label, 3, 12, 1, 1)

        ''' row 13
        self.label = Gtk.Label(self.shorten(self.VAR_IMAGE_NAME))
        self.grid.attach(self.label, 0, 13, 1, 1)

        self.entry = Gtk.Entry()
        self.entry.set_text("")
        self.entry.connect("activate", self.enter_image_name_callback, self.VAR_IMAGE_NAME, self.FOLDER_IMAGE_NAME,
                           self.label)
        self.grid.attach(self.entry, 1, 13, 1, 1)

        self.button = Gtk.Button(label="Picker")
        self.button.connect("clicked", self.on_image_name_button, self.VAR_IMAGE_NAME, self.FOLDER_IMAGE_NAME,
                            self.label)
        self.grid.attach(self.button, 2, 13, 1, 1)

        self.label = Gtk.Label("Base Name")
        self.grid.attach(self.label, 3, 13, 1, 1)

        '''
        self.drawingarea = Gtk.DrawingArea()
        self.drawingarea.set_size_request(500,500)
        self.drawingarea.connect("draw", self.draw)
        self.grid.attach(self.drawingarea, 0,13,4,20)


    def show_window(self):
        win = self  # Interface()
        win.connect("delete-event", Gtk.main_quit)
        win.show_all()
        Gtk.main()

    def draw(self, widget, context):
        name = self.VAR_IMAGE_NAME.strip("\n")
        print name

        if name.lower().endswith("png") :
            self.image = cairo.ImageSurface.create_from_png(name)
            context.set_source_surface(self.image, 0.0, 10.0)
            context.paint()
            print ('png image')
        if name.lower().endswith("jpg") or name.lower().endswith("jpeg"):
            self.pb = GdkPixbuf.Pixbuf.new_from_file(name)
            Gdk.cairo_set_source_pixbuf(context, self.pb, 0, 10)
            context.paint()
            print('jpg image')
        return False

    def enter_image_name_callback(self, widget, var, folder, label):
        var = widget.get_text()
        self.dot_write(folder, var)
        #self.entry.set_text(self.shorten(var))
        label.set_text(self.shorten(var))
        self.switch_folder_var(folder,var)

    def on_image_name_button(self, widget, var, folder, label):
        temp = easygui.fileopenbox()
        if len(temp) > 0:
            var = str(temp)
            self.dot_write(folder, var)
            #self.entry.set_text(self.shorten(var))
            label.set_text(self.shorten(var))
            self.switch_folder_var(folder,var)

    def on_image_folder_button(self, widget, var, folder, label):
        temp = easygui.diropenbox()
        if len(temp) > 0:
            var = str(temp)
            self.dot_write(folder, var)
            #self.entry.set_text(self.shorten(var))
            label.set_text(self.shorten(var))
            self.switch_folder_var(folder,var)

    def shorten(self, input):
        return "..." + input[-10:]

    def switch_folder_var(self, folder, var):
        if folder == self.FOLDER_BASE_NAME :
            self.VAR_BASE_NAME = var
        if folder == self.FOLDER_CSV_FILE_SECOND :
            self.VAR_CSV_FILE_SECOND = var
        if folder == self.FOLDER_CSV_FILE_SINGLE :
            self.VAR_CSV_FILE_SINGLE = var
        if folder == self.FOLDER_IMAGE_NAME :
            self.VAR_IMAGE_NAME = var
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