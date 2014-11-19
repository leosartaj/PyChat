#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

# system imports
from random import choice

# twisted imports
from twisted.python import log

# For the GUI
import gtk
from connectBoxClass import connectBoxClass

# helper modules
import helper.markup as markup # functions for formatting text
import helper.notebook as notebook # functions for handling notebook
import helper.textview as textview # functions for handling textview

# other imports
from connect import setup_factory
from helper import helperFunc as hf

class clientGUIClass:
    """ 
    Sets up the GUI interface
    """
    def __init__(self, host, port, client):

        self.load_interface() # load the interface

        self.save_objects() # save objects
        self.builder.connect_signals(self.setup_signals()) # setup signals
        self.window.show_all() # display widgets

        self.basic_markup() # setup appearances
        self.chatbox.grab_focus() # focus here
        self.scrollusers.hide() # hide users panel by default
        self.updateView('server', 'Not Connected') # Tell users if not connected

        setup_factory(self, host, port, client) # connect

    def load_interface(self):
        """
        Loads the interface
        in particular loads the glade file
        """
        fName = hf.find_file(__file__, 'clientGUI.glade')
        self.builder = gtk.Builder()
        self.builder.add_from_file(fName)

    def setup_signals(self):
        """
        Sets up the signals
        """
        sig = { 'on_MainWindow_destroy'     : self.close
              , 'on_exit_button_press_event': self.close
              , 'on_chatbox_activate'       : self.sendButton
              , 'on_sendButton_clicked'     : self.sendButton 
              , 'on_connectedusers_toggled': self.toggleUsersPanel }

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

    def basic_markup(self):
        """
        set the appearances, 'cause appearances are good
        """

        self.colors = {'me': 'white', 'server': 'white'} # client colors

        markup.background(self.textview, '#002b36') # set the background
        markup.textcolor(self.textview, 'white') # set the textcolor 

        markup.background(self.userview, '#002b36') # set the background
        markup.textcolor(self.userview, 'white') # set the textcolor 
        self.userview.get_buffer().set_text('Connected Users\n') # setup connected user panel board

    def register_color(self, name):
        """
        Register color of the user
        """
        key = choice(markup.color_dict.keys()) # select a random color
        self.colors[name] = markup.color_dict[key] # save the color

    def toggleUsersPanel(self, widget):
        """
        Toggles the connected users panel
        """
        userPanel = self.scrollusers
        if userPanel.get_property('visible'):
            userPanel.hide()
        else:
            userPanel.show()
            self.updateConnUsers('me')

    def updateConnUsers(self, name):
        """
        Updates the connected users panel
        """
        if not name in self.colors:
            self.register_color(name) # register user color

        if not self.scrollusers.get_property('visible'): # do not update if not visible
            return

        # reset the view
        userview = self.userview
        buf = userview.get_buffer()
        buf.set_text('Connected Users\n')

        # updated connected users
        users = self.client.users
        for user, ip in users:
            buf.insert(buf.get_end_iter(), user + '\n')
            markup.color_text(buf, self.colors[user]) # color the line

    def updateView(self, name, text):
        """
        Wrapper for updating textview
        """
        textview.updateTextView(self.textview, self.colors, name, text)
        textview.autoScroll(self.scroll) # Scroll Please

    def sendButton(self, button):
        """
        When the button is clicked
        """
        text = self.chatbox.get_text()
        if text:
            self.chatbox.set_text('') # clear the textbox
            self.updateView('me', text)
            self.client.send(text) # logs and sends the message
        self.chatbox.grab_focus() # focus the textbox

    def close(self, *args):
        """
        Handles Destroy Event
        """
        log.msg('Disconnected from server')
        gtk.main_quit()
