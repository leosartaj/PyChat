#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

# system imports
import os
from random import choice

# For the GUI
import gtk
import markup # functions for formatting text

# twisted imports
from twisted.python import log

class clientGUIClass:
    """ 
    Sets up the GUI interface
    """
    def __init__(self, client):

        self.client = client # remember the client

        self.load_interface() # load the interface

        self.save_objects() # save objects

        self.basic_markup() # setup appearances

        self.chatbox.grab_focus() # focus here

        self.builder.connect_signals(self.setup_signals()) # setup signals

        self.window.show_all() # display everything

    def load_interface(self):
        """
        Loads the interface
        in particular loads the glade file
        """
        fName = os.path.join(os.path.dirname(__file__), 'clientGUI.glade') # hack for loading the glade file
        self.builder = gtk.Builder()
        self.builder.add_from_file(fName)

    def setup_signals(self):
        """
        Sets up the signals
        """
        sig = { 'on_MainWindow_destroy'     : self.close
              , 'on_exit_button_press_event': self.close
              , 'on_chatbox_activate'       : self.sendButton
              , 'on_sendButton_clicked'     : self.sendButton }

        return sig

    def save_objects(self):
        """
        Get the required objects
        """
        self.window = self.builder.get_object('MainWindow')

        # main chat area
        self.textview = self.builder.get_object('textview') 
        self.scroll = self.builder.get_object('scrolledwindow')

        # Connected Users board
        self.userview = self.builder.get_object('userview') 
        self.scrollusers = self.builder.get_object('scrolledwindow1')

        self.chatbox = self.builder.get_object('chatbox') 

    def basic_markup(self):
        """
        set the appearances, 'cause appearances are good
        """

        self.colors = {'me': 'white', 'server': 'white'} # client colors
        markup.background(self.textview, '#002b36') # set the background
        markup.textcolor(self.textview, 'white') # set the textcolor 

    def register_color(self, name):
        """
        Register color of the user
        """
        key = choice(markup.color_dict.keys()) # select a random color
        self.colors[name] = markup.color_dict[key] # save the color

    def updateConnUsers(self):
        """
        Updates the connected users panel
        """
        if not self.scrollusers.get_property('visible'): # do not update if not visible
            return

        # reset the view
        userview = self.userview
        buf = userview.get_buffer()
        buf.set_text('Connected Users\n')

        # updated connected users
        users = self.client.users
        for user in users:
            buf.insert(buf.get_end_iter(), user[0] + '\n')

    def formatMsg(self, name, msg):
        """
        Format The received Message
        """
        return name + ' >>> ' + msg + '\n'

    def updateTextView(self, name, msg):
        """
        Updates the Textview appropriately
        """
        msg = self.formatMsg(name, msg) # get the formatted message

        text = self.textview

        buf = text.get_buffer()
        buf.insert(buf.get_end_iter(), msg)
        
        if not name in self.colors:
            self.register_color(name)

        markup.color_text(buf, self.colors[name]) # color the line

        self.autoScroll(self.scroll) # Scroll Please

    def autoScroll(self, scroll):
        """
        Autoscroll TextView
        """
        obj = scroll.get_vadjustment() # get the adjustment, returns the adjustment object
        obj.set_value(obj.upper - obj.page_size)

    def sendButton(self, button):
        """
        When the button is clicked
        """
        text = self.chatbox.get_text()
        if text:
            self.chatbox.set_text('') # clear the textbox
            self.updateTextView('me', text)
            self.client.send(text) # logs and sends the message
        self.chatbox.grab_focus() # focus the textbox

    def close(self, *args):
        """
        Handles Destroy Event
        """
        log.msg('Disconnected from server')
        gtk.main_quit()
