#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

# System imports
import os

# for GUI
import gtk

# other imports
from helper import helperFunc as hf

class fileChooserClass:
    """ 
    Sets up Connect Box
    """
    def __init__(self, parent):

        self.parent = parent # save the parent caller

        self.builder = hf.load_interface(__file__, 'glade/filechooser.glade') # load the interface
        self.save_objects() # save objects
        self.builder.connect_signals(self.setup_signals()) # setup signals

        hf.center(self.window, self.parent.window) # center the window to the center of the parent

        self.window.show_all() # display widgets

    def setup_signals(self):
        """
        Sets up the signals
        """
        sig = { 'on_filewindow_destroy'     : self.close 
              , 'on_cancel_clicked'         : self.close
              , 'on_file_activated'         : self.sendFile
              , 'on_send_clicked'           : self.sendFile }

        return sig

    def save_objects(self):
        """
        Get the required objects
        """
        self.window = self.builder.get_object('filewindow')
        self.file = self.builder.get_object('filechooser')
        self.send = self.builder.get_object('send')
        self.cancel = self.builder.get_object('cancel')

    def sendFile(self, button):
        """
        Send the selected file
        """
        fName = self.file.get_filename()
        if fName:
            if os.path.isdir(fName):
                self.file.set_current_folder(fName)
            else:
                self.parent.sendFile(fName)
                self.close()

    def close(self, *args):
        """
        Handles Destroy Event
        """
        self.window.destroy()
