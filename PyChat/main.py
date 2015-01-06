#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

# system imports
import sys

# twisted imports
from twisted.python import log

# Other imports
from client.error import __servfail__
from client.gui.clientGUIClass import clientGUIClass # get the main gui class
from client.gui.helper import helperFunc as hf
from server import start_server

def startGui(clientname):
    """
    Starts Gui
    returns the gui reference
    """
    gui = clientGUIClass(clientname) # start the gui
    return gui

def connect(gui, host, port, server=False):
    """
    Create a new connection
    """
    if not hf.validate_host(host): # allow deafult connecting
        return
    obj = gui.get_clientobj() # generate object
    result, factory = True, None
    if server:
        result, lisport, factory = start_server.listen(host, port)
    if result: # if everything goes well
        if factory: 
            obj.set_factory(lisport, factory)
        gui.connect(host, port, obj) # try to connect
    else: # incase server couldnt get started
        obj.updateView('server', __servfail__)

def startLog(handle):
    """
    Starts the logging
    """
    log.startLogging(handle)

def run(clientname, handle=sys.stdout, addresses=[]):
    """
    Runs the Gui
    address is a list of tuples(host, port, server)
    host:port is the ip:port to connect to
    server is a boolean definig whether to start a server or not
    """
    startLog(handle)
    gui = startGui(clientname)
    for host, port, server in addresses:
        connect(gui, host, port, server)
