#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

"""
Contains Helper functions
"""

import os
import gtk

def find_file(dire, fName):
    """
    Finds file in the given directory
    returns the complete path
    """
    path = os.path.join(os.path.dirname(dire), fName)
    return path

def load_interface(dire, fName):
    """
    Loads the interface
    in particular loads the glade file
    returns the builder
    """
    fName = find_file(dire, fName)
    builder = gtk.Builder()
    builder.add_from_file(fName)
    return builder

def load_chatarea_widgets(parent, builder):
    hpane = builder.get_object('hpaned1')
    scroll = builder.get_object('scrolledwindow')
    scrollusers = builder.get_object('scrolledwindow1')
    textview = builder.get_object('textview')
    userview = builder.get_object('userview')
    return [parent, hpane, scroll, textview, scrollusers, userview]

def center(widget, parent):
    """
    Centers the window to the
    location of open instance of
    parent window
    """
    widget.set_transient_for(parent) # set parent
    widget.set_position(gtk.WIN_POS_CENTER_ON_PARENT)

def label(labeltext):
    """
    Make a new gtk
    label with labeltext
    """
    #return gtk.label_new(labeltext)
