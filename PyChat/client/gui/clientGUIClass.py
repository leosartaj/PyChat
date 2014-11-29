#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

"""
Contains the main GUI Class
"""

# system imports
from random import choice

# twisted imports
from twisted.python import log

# For the GUI
import gtk
from connectBoxClass import connectBoxClass

# Connections
from clientClass import clientClass

# helper modules
from helper import helperFunc as hf
from helper.stack import stack
from helper import markup # functions for formatting text
from helper import notebook # functions for handling notebook

class clientGUIClass:
    """ 
    Sets up the GUI interface
    """
    def __init__(self, name):

        self.name = name # save the client name

        self.builder = hf.load_interface(__file__, 'glade/clientGUI.glade') # load the interface

        self.save_objects() # save objects
        self.builder.connect_signals(self.setup_signals()) # setup signals

        self.chatbox.grab_focus() # focus here

        self.setup_page()
        notebook.show_tabs(self.notebook) # toggle tabs visibility

        self.stack = stack() # for upper key and lower key functionality
        self.objects = [] # list of active connections
        self.showusers = False

        self.window.show_all() # display widgets

    def setup_signals(self):
        """
        Sets up the signals
        """
        sig = { 'on_MainWindow_destroy'     : self.close
              , 'on_exit_button_press_event': self.close
              , 'on_chatbox_activate'       : self.sendButton
              , 'on_sendButton_clicked'     : self.sendButton 
              , 'on_connectedusers_toggled' : self.toggleUsersPanel
              , 'on_connect_activate'       : self.set_connect_box
              , 'on_key_press'              : self.handleKeys }

        return sig

    def save_objects(self):
        """
        Get the required objects
        """
        self.window = self.builder.get_object('MainWindow')
        self.notebook = self.builder.get_object('notebook')
        self.chatbox = self.builder.get_object('chatbox') 

    def setup_page(self):
        """
        sets up a new notebook page
        returns the loaded widgets
        """
        builder = hf.load_interface(__file__, 'glade/chatarea.glade')
        widgets = hf.load_chatarea_widgets(self, builder) # get the widgets

        notebook.add_page(self.notebook, widgets[1], None)
        notebook.show_tabs(self.notebook) # toggle tabs visibility

        markup.basic_markup(widgets[3], widgets[5]) # set the colors

        return widgets

    def toggleUsersPanel(self, widget):
        """
        Toggles the connected users panel
        """
        if self.showusers:
            self.showusers = False
        else:
            self.showusers = True

        # improve for dummy page
        for obj in self.objects:
            userPanel = obj.scrollusers
            if self.showusers:
                userPanel.show()
                obj.updateConnUsers('me')
            else:
                userPanel.hide()

    def set_connect_box(self, menuitem):
        """
        sets up the connection box
        """
        connectBoxClass(self)

    def connect(self, host, port):
        """
        Loads the chatarea
        makes a new notebook page
        Makes a new client object
        saves refrence to the object
        and invokes its connect method
        """
        widgets = self.setup_page()
        clientobj = clientClass(self.name, widgets)
        clientobj.connect(host, port)

        self.objects.append(clientobj) # save a reference finally

    def connectionLost(self, clientobj):
        """
        Removes the refrence of the disconnected clientobj
        """
        del self.objects[self.objects.index(clientobj)]
        del clientobj

    def sendButton(self, button):
        """
        When the button is clicked
        """
        text = self.chatbox.get_text()
        if text:
            self.stack.push(text) # push the text on stack
            if len(self.objects) != 0:
                self.chatbox.set_text('') # clear the textbox
                self.objects[0].send(text)
        self.chatbox.grab_focus() # focus the textbox

    def handleKeys(self, widget, key):
        """
        Handles key press
        event in chatbox
        returns last entered text when up key is pressed
        cycles up the stack when down key is pressed
        """
        keyname = gtk.gdk.keyval_name(key.keyval)

        text = None
        if keyname == 'Up':
            text = self.stack.pop()
        elif keyname == 'Down':
            text = self.stack.up()
        else:
            self.stack.reset_point() # reset the pointer

        if text != None:
            self.chatbox.set_text(text)
            self.chatbox.set_position(len(text)) # set the cursor position

    def close(self, *args):
        """
        Handles Destroy Event
        """
        log.msg('Disconnected from server')
        gtk.main_quit()
