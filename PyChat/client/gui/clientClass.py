#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##


"""
Contains the class for defining a client
"""

from helper import textview # helper modules
from helper import markup # helper modules
try:
    from connect import setup_factory
except ImportError:
    from PyChat.client.connect import setup_factory

class clientClass:
    """
    Class for defining a client
    """
    def __init__(self, client, widgets):
        self.client = client # name of the client 
        self.protocol = None # protocol instance
        self.server = [False, None, None] # if it creates a server
        self.host = None
        self.port = None

        self.parse_widgets(widgets)
        self.colors = markup.default_colors()

    def parse_widgets(self, widgets):
        """
        Save refrences to important widgets
        """
        self.parent = widgets[0]
        self.page = widgets[1]
        self.hpane = widgets[2]
        self.scroll = widgets[3]
        self.textview = widgets[4]
        self.scrollusers = widgets[5]
        self.userview = widgets[6]

    def set_factory(self, lisport, factory):
        """
        saves the factory
        saves the lisport
        and makes it
        the server creating class
        """
        self.server = [True, lisport, factory]

    def get_host(self):
        """
        Returns the host address
        """
        return self.host

    def get_port(self):
        """
        Returns the connection port 
        """
        return self.port

    def send(self, text):
        """
        Sends the data over the network and updates
        the gui
        """
        self.updateView('me', text)
        if self.protocol:
            self.protocol.send(text) # logs and sends the message

    def connect(self, host, port):
        """
        handles connection to the server
        """
        self.host = host
        self.port = port

        setup_factory(self, host, port, self.client) # connect
        self.updateConnUsers('me') # update the connected users panel

    def connectionLost(self, msg):
        """
        Handles when connection is lost
        or failed
        """
        self.stop_server_factory()
        self.updateView('server', msg)
        self.updateConnUsers('me') # update the connected users panel

    def loseConnection(self):
        """
        Loses connection with the server
        """
        if self.protocol:
            self.protocol.transport.loseConnection()
            self.protocol = None
        self.stop_server_factory()

    def stop_server_factory(self):
        """
        If server class
        then stops the server factory
        else does nothing at all
        """
        if self.server[0]:
            self.server[1].stopListening()
            self.server[2].disconnect() # close all connections
            self.server = [False, None, None]

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
            markup.color_text(buf, self.colors[name]) # color the line
