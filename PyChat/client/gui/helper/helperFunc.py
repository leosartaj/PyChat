#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##


"""
Contains Helper functions
"""

import os
import gtk

def validate_host(host):
    """
    Checks the hostname
    four chunks separated by 3 dots
    each a valid integer(0 - 255)
    """
    bits = host.split('.')
    try:
        if len(bits) != 4:
            raise ValueError
        for bit in bits:
            num = int(bit)
            if num > 255 or num < 0:
                raise ValueError
    except ValueError:
        return False
    return True

def find_file(dire, fName):
    """
    Generates the complete path of a file
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
    """
    saves objects from the builder
    returns a list of objects
    """
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

def label(labeltext=None):
    """
    Make a new gtk
    label with labeltext
    """
    label = gtk.Label()
    label.set_text(labeltext)
    return label
