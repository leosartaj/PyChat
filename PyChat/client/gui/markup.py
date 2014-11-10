#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

"""
Helper functions for formatting text
"""

import gtk
import pango

"""
    SOLARIZED HEX     
    --------- ------- 
    base03    #002b36  
    base02    #073642  
    base01    #586e75 
    base00    #657b83 
    base0     #839496 
    base1     #93a1a1 
    base2     #eee8d5  
    base3     #fdf6e3 
    yellow    #b58900  
    orange    #cb4b16  
    red       #dc322f  
    magenta   #d33682  
    violet    #6c71c4 
    blue      #268bd2  
    cyan      #2aa198  
    green     #859900  

"""

# Color Palette
color_dict = {'orange': '#cb4b16', 'red': '#dc322f', 'magenta': '#d33682', 'violet': '#6c71c4', 'blue': '#268bd2', 'cyan': '#2aa198', 'green': '#859900'}

def background(widget, color):
    """
    Background of a widget
    """
    widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse(color)) 

def textcolor(widget, color):
    """
    Change the text color
    displayed in a widget
    """
    widget.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse(color))

def color_text(buf, color):
    """
    Colors a line with the desired color
    """
    tag = buf.create_tag(foreground=color)

    # get the region to be colored
    lines = buf.get_line_count()
    start = buf.get_iter_at_line(lines - 2)
    end = buf.get_iter_at_line(lines)

    buf.apply_tag(tag, start, end) # color the region
