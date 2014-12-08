#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##


"""
Handles main textview related functionality
"""

from markup import color_text

def formatMsg(name, msg):
    """
    Format The received Message
    """
    return name + ' >>> ' + msg + '\n'

def autoScroll(scroll):
    """
    Autoscroll TextView
    """
    obj = scroll.get_vadjustment() # get the adjustment, returns the adjustment object
    obj.set_value(obj.upper - obj.page_size)

def updateTextView(textview, colors, name, msg):
    """
    Updates the Textview appropriately
    """
    msg = formatMsg(name, msg) # get the formatted message

    buf = textview.get_buffer()
    buf.insert(buf.get_end_iter(), msg)
    
    color_text(buf, colors[name]) # color the line
