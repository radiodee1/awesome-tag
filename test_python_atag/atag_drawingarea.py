#!/usr/bin/python

#import easygui

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk
import cairo

class DrawingArea(Gtk.DrawingArea) :
    def __init__(self):
        Gtk.DrawingArea.__init__(self)

        self.imagename = None
        self.set_size_request(500,500)
        self.connect("draw", self.draw)

    def set_imagename(self, imagename):
        self.imagename = imagename

    def draw(self, widget, context):
        name = self.imagename.strip("\n")
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