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

        self.builder = hf.load_interface(__file__, 'clientGUI.glade') # load the interface

        self.save_objects() # save objects
        self.builder.connect_signals(self.setup_signals()) # setup signals
        self.window.show_all() # display widgets

        self.basic_markup() # setup appearances
        self.chatbox.grab_focus() # focus here
        self.scrollusers.hide() # hide users panel by default

        self.stack = stack() # for upper key and lower key functionality

        self.objects = [] # list of active connections

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

        # Notebook
        self.notebook = self.builder.get_object('notebook')

        # main chat area
        self.textview = self.builder.get_object('textview') 
        self.scroll = self.builder.get_object('scrolledwindow')

        # Connected Users board
        self.userview = self.builder.get_object('userview') 
        self.scrollusers = self.builder.get_object('scrolledwindow1')

        self.chatbox = self.builder.get_object('chatbox') 

        self.widgets = [self, self.textview, self.scroll, self.scrollusers, self.userview] # hack for arguments for client object

    def basic_markup(self):
        """
        set the appearances, 'cause appearances are good
        """
        markup.background(self.textview, '#002b36') # set the background
        markup.textcolor(self.textview, 'white') # set the textcolor 

        markup.background(self.userview, '#002b36') # set the background
        markup.textcolor(self.userview, 'white') # set the textcolor 
        self.userview.get_buffer().set_text('Not connected\n') # setup connected user panel board

    def toggleUsersPanel(self, widget):
        """
        Toggles the connected users panel
        """
        userPanel = self.scrollusers
        if userPanel.get_property('visible'):
            userPanel.hide()
        else:
            userPanel.show()
            if len(self.objects) != 0:
                self.objects[0].updateConnUsers('me') # hack improve it

    def set_connect_box(self, menuitem):
        """
        sets up the connection box
        """
        connectBoxClass(self)

    def connect(self, host, port):
        """
        Makes a new client object
        saves refrence to the object
        and invokes its connect method
        """
        clientobj = clientClass(self.name, self.widgets)
        self.objects.append(clientobj)
        clientobj.connect(host, port)

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
