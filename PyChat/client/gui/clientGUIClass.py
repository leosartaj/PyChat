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
from helper.stack import stack

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
        self.updateView('server', 'Not Connected') # Tell users if not connected

        self.stack = stack() # for upper key and lower key functionality

        # variables
        self.protocol = None # when connected has the refrence to protocol
        self.connected = False

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

    def basic_markup(self):
        """
        set the appearances, 'cause appearances are good
        """

        self.colors = self.reset_color()

        markup.background(self.textview, '#002b36') # set the background
        markup.textcolor(self.textview, 'white') # set the textcolor 

        markup.background(self.userview, '#002b36') # set the background
        markup.textcolor(self.userview, 'white') # set the textcolor 
        self.userview.get_buffer().set_text('Not connected\n') # setup connected user panel board

    def reset_color(self, color={}):
        """
        Resets the color dict to default
        """
        colors = {'me': 'white', 'server': 'white'} # client colors
        return colors

    def register_color(self, name):
        """
        Register color of the user
        """
        key = choice(markup.color_dict.keys()) # select a random color
        self.colors[name] = markup.color_dict[key] # save the color

    def remove_color(self, name):
        """
        Remove color of the disconnected user
        """
        del self.colors[name]

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
        if self.connected:
            buf.set_text('Connected Users\n')
        else:
            buf.set_text('Not Connected\n') # tell if not connected
            return

        if not self.protocol:
            return

        # updated connected users
        users = self.protocol.users
        for user, ip in users:
            buf.insert(buf.get_end_iter(), user + '\n')
            markup.color_text(buf, self.colors[user]) # color the line

    def set_connect_box(self, menuitem):
        """
        sets up the connection box
        """
        connectBoxClass(self)

    def connect(self, host, port):
        """
        handles connection to the server
        """
        if self.connected: # hack for now
            self.protocol.transport.loseConnection()
        self.connected = True
        setup_factory(self, host, port, self.name) # connect
        self.updateConnUsers('me') # update the connected users panel

    def connectionLost(self, msg):
        """
        Handles when connection is lost
        or failed
        """
        self.connected = False
        self.protocol = None # reset to refrence to None
        self.colors = self.reset_color(self.colors)
        self.updateView('server', msg)
        self.updateConnUsers('me') # update the connected users panel

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
            self.stack.push(text) # push the text on stack
            self.chatbox.set_text('') # clear the textbox
            self.updateView('me', text)
            if self.connected:
                self.protocol.send(text) # logs and sends the message
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
