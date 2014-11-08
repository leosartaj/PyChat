#!/usr/bin/env python2
##
# PyGp
# https://github.com/leosartaj/PyGp.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

# system imports
import os

# For the GUI
import gtk

# twisted imports
from twisted.python import log


class clientGUIClass:
    """ 
    Sets up the GUI interface
    """
    def __init__(self, client):

        self.client = client # remember the client

        # load the interface
        fName = os.path.join(os.path.dirname(__file__), 'clientGUI.glade') # hack for loading the glade file
        builder = gtk.Builder()
        builder.add_from_file(fName)

        # save objects
        self.window = builder.get_object('MainWindow')
        self.textview = builder.get_object('textview') 
        self.chatbox = builder.get_object('chatbox') 

        self.chatbox.grab_focus() # focus here

        builder.connect_signals(self.setup_signals()) # setup signals

        self.window.show_all() # display everything

    def setup_signals(self):
        """
        Sets up the signals
        """
        sig = {'on_MainWindow_destroy': self.close, 'on_sendButton_clicked': self.sendButton, 'on_sendButton_enter': self.sendButton }
        return sig

    def updateTextView(self, msg):
        """
        Updates the Textview appropriately
        """
        text = self.textview
        text.get_buffer().insert(text.get_buffer().get_end_iter(), msg + '\n')

    def sendButton(self, button):
        """
        When the button is clicked
        """
        text = self.chatbox.get_text()
        if text:
            self.chatbox.set_text('') # clear the textbox and focus it
            self.updateTextView('me >>> ' + text)
            self.client.sendLine(text)
        self.chatbox.grab_focus()

    def close(self, window):
        """
        Handles Destroy Event
        """
        log.msg('Disconnected from server')
        gtk.main_quit()
