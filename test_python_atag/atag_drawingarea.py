#!/usr/bin/python

#import easygui

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk
import cairo
import nn_dim as dim

class DrawingArea(Gtk.DrawingArea, dim.Dimension) :
    def __init__(self):
        Gtk.DrawingArea.__init__(self)
        dim.Dimension.__init__(self)
        self.space_top = 0#10
        self.space_left = 0
        self.imagename = None
        self.set_size_request(500,500)

        self.connect("draw", self.draw)

        self.ENUM_BOXES = 0
        self.ENUM_GRADIENT_1 = 1
        self.ENUM_GRADIENT_RGB = 2
        self.gradient_list = []
        self.draw_enum = self.ENUM_BOXES
        self.dim_x = self.DIMENSIONS[self.key][self.COLUMN_XY_CONV][0]
        self.dim_y = self.DIMENSIONS[self.key][self.COLUMN_XY_CONV][1]

        self.boxlist_red = []#[(0,0,10,20),(5,5,10,20)]
        self.boxlist_green = []#[(3,3,3,3),(7,7,7,7)]
        self.boxlist_blue = []

    def set_imagename(self, imagename):
        self.imagename = imagename
        self.boxlist_red = []
        self.boxlist_green = []
        self.boxlist_blue = []

    def set_red(self, red):
        self.boxlist_red = red

    def set_green(self,green):
        self.boxlist_green = green

    def set_blue(self, blue):
        self.boxlist_blue = blue

    def set_gradient_info(self, skin, img, three):
        self.draw_enum = self.ENUM_GRADIENT_RGB
        self.gradient_list = three


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

        if self.draw_enum == self.ENUM_BOXES:
            context.set_line_width(1)
            context.set_source_rgb(1, 0, 0)
            self.box_list(context, self.boxlist_red)
            context.set_source_rgb(0, 1, 0)
            self.box_list(context, self.boxlist_green)
            context.set_source_rgb(0, 0, 1)
            self.box_list(context, self.boxlist_blue)
            return False
        elif self.draw_enum == self.ENUM_GRADIENT_RGB:
            self.gradient_rgb(context, widget)
            pass

    def box_list(self, context, list):
        for red in list:
            context.move_to(red[0] + self.space_left, red[1] + self.space_top)
            context.line_to(red[0] + self.space_left, red[1] + self.space_top + red[3])
            context.line_to(red[0] + self.space_left + red[2], red[1] + self.space_top + red[3])
            context.line_to(red[0] + self.space_left + red[2], red[1] + self.space_top)
            context.line_to(red[0] + self.space_left, red[1] + self.space_top)
        context.stroke()

    def gradient_rgb(self, context, widget):

        for yy in range(self.dim_x) :
            for xx in range(self.dim_x):
                #print xx, yy
                c = (xx * self.dim_x + yy) * 3
                c0 = c
                c1 = c + 1
                c2 = c + 2
                if c2 < len(self.gradient_list) :
                    context.set_source_rgb(self.gradient_list[c0] * 2,
                               self.gradient_list[c1] * 2,
                               self.gradient_list[c2] * 2)

                context.rectangle( xx * 5 , yy * 5, 5,5)
                context.fill()
        pass