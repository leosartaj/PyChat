#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

"""
Contains the class for defining a client
"""

from helper import textview # helper modules
from helper import markup # helper modules
from connect import setup_factory

class clientClass:
    """
    Class for defining a client
    """
    def __init__(self, client, widgets):
        self.client = client # name of the client
        self.protocol = None # protocol instance
        self.parse_widgets(widgets)
        self.colors = markup.default_colors()

    def parse_widgets(self, widgets):
        """
        Save refrences to important widgets
        """
        self.parent = widgets[0]
        self.hpane = widgets[1]
        self.scroll = widgets[2]
        self.textview = widgets[3]
        self.scrollusers = widgets[4]
        self.userview = widgets[5]

    def send(self, text):
        """
        Sends the data over the network and updates
        the gui
        """
        self.updateView('me', text)
        self.protocol.send(text) # logs and sends the message

    def connect(self, host, port):
        """
        handles connection to the server
        """
        setup_factory(self, host, port, self.client) # connect
        self.updateConnUsers('me') # update the connected users panel

    def connectionLost(self, msg):
        """
        Handles when connection is lost
        or failed
        """
        self.updateView('server', msg)
        self.updateConnUsers('me') # update the connected users panel
        self.parent.connectionLost(self)

    def updateView(self, name, text):
        """
        Wrapper for updating textview
        """
        textview.updateTextView(self.textview, self.colors, name, text)
        textview.autoScroll(self.scroll) # Scroll Please

    def updateConnUsers(self, name):
        """
        Updates the connected users panel
        """
        if not name in self.colors:
            markup.register_color(self.colors, name) # register user color

        if not self.scrollusers.get_property('visible'): # do not update if not visible
            return

        # reset the view
        userview = self.userview
        buf = userview.get_buffer()
        if self.protocol:
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
