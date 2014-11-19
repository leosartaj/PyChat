#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

# for GUI
import gtk

# other imports
from helper import helperFunc as hf

class connectBoxClass:
    """ 
    Sets up Connect Box
    """
    def __init__(self, parent):

        self.parent = parent # save the parent caller

        self.load_interface() # load the interface
        self.save_objects() # save objects
        self.builder.connect_signals(self.setup_signals()) # setup signals

        hf.center(self.window, self.parent.window) # center the window to the center of the parent

        self.window.show_all() # display widgets

    def load_interface(self):
        """
        Loads the interface
        in particular loads the glade file
        """
        fName = hf.find_file(__file__, 'connectBox.glade')
        self.builder = gtk.Builder()
        self.builder.add_from_file(fName)

    def setup_signals(self):
        """
        Sets up the signals
        """
        sig = { 'on_mainwindow_destroy': self.close
              , 'on_cancel_clicked'   : self.close }

        return sig

    def save_objects(self):
        """
        Get the required objects
        """
        self.window = self.builder.get_object('mainwindow')

    def close(self, *args):
        """
        Handles Destroy Event
        """
        self.window.destroy()
