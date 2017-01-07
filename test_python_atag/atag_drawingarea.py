#!/usr/bin/python

#import easygui

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk
import cairo

class DrawingArea(Gtk.DrawingArea) :
    def __init__(self):
        Gtk.DrawingArea.__init__(self)
        self.space_top = 0#10
        self.space_left = 0
        self.imagename = None
        self.set_size_request(500,500)
        #self.set_default_size(500,500)
        self.connect("draw", self.draw)
        #self.set_hexpand(True)
        #self.set_vexpand(True)

        self.boxlist_red = []#[(0,0,10,20),(5,5,10,20)]
        self.boxlist_green = []#[(3,3,3,3),(7,7,7,7)]
        self.boxlist_blue = []

    def set_imagename(self, imagename):
        self.imagename = imagename

    def set_red(self, red):
        self.boxlist_red = red

    def set_green(self,green):
        self.boxlist_green = green

    def set_blue(self, blue):
        self.boxlist_blue = blue

    def draw(self, widget, context):
        name = self.imagename.strip("\n")
        #print name

        if name.lower().endswith("png") :
            self.image = cairo.ImageSurface.create_from_png(name)
            context.set_source_surface(self.image, self.space_left, self.space_top)
            context.paint()
            width = self.image.get_width()
            height = self.image.get_height()
            self.set_size_request(width, height)
            #print 'png image', width, height

        if name.lower().endswith("jpg") or name.lower().endswith("jpeg"):
            self.pb = GdkPixbuf.Pixbuf.new_from_file(name)
            Gdk.cairo_set_source_pixbuf(context, self.pb, self.space_left, self.space_top)
            context.paint()
            self.dim = GdkPixbuf.Pixbuf.get_file_info(name)
            self.set_size_request(self.dim.width, self.dim.height)
            #print 'jpg image'


        context.set_line_width(1)
        context.set_source_rgb(1, 0, 0)
        self.box_list(context, self.boxlist_red)
        context.set_source_rgb(0, 1, 0)
        self.box_list(context, self.boxlist_green)
        context.set_source_rgb(0, 0, 1)
        self.box_list(context, self.boxlist_blue)
        return False

    def box_list(self, context, list):
        for red in list:
            context.move_to(red[0] + self.space_left, red[1] + self.space_top)
            context.line_to(red[0] + self.space_left, red[1] + self.space_top + red[3])
            context.line_to(red[0] + self.space_left + red[2], red[1] + self.space_top + red[3])
            context.line_to(red[0] + self.space_left + red[2], red[1] + self.space_top)
            context.line_to(red[0] + self.space_left, red[1] + self.space_top)
        context.stroke()
