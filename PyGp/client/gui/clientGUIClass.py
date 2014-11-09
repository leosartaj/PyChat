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

        self.load_interface() # load the interface

        self.save_objects() # save objects

        self.color() # setup appearances

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
        self.textview = self.builder.get_object('textview') 
        self.chatbox = self.builder.get_object('chatbox') 
        self.scroll = self.builder.get_object('scrolledwindow')

    def color(self):
        """
        set the appearances, 'cause appearances are good

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

        self.textview.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('#002b36')) 
        self.textview.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse('#2aa198'))

    def updateTextView(self, name, msg):
        """
        Updates the Textview appropriately
        """
        msg = self.formatMsg(name, msg) # get the formatted message

        text = self.textview

        buf = text.get_buffer()
        buf.insert(buf.get_end_iter(), msg)

        self.autoScroll() # Scroll Please

    def formatMsg(self, name, msg):
        """
        Format The received Message
        """
        return name + ' >>> ' + msg + '\n'

    def autoScroll(self):
        """
        Autoscroll TextView
        """
        obj = self.scroll.get_vadjustment() # get the adjustment, returns the adjustment object
        obj.set_value(obj.upper - obj.page_size)

    def sendButton(self, button):
        """
        When the button is clicked
        """
        text = self.chatbox.get_text()
        if text:
            self.chatbox.set_text('') # clear the textbox and focus it
            self.updateTextView('me', text)
            self.client.sendLine(text)
        self.chatbox.grab_focus()

    def close(self, *args):
        """
        Handles Destroy Event
        """
        log.msg('Disconnected from server')
        gtk.main_quit()
