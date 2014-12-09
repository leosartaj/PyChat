#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

"""
Development script
To run without actually installing
Picks up local changes
"""

# system imports
import sys
import os

# twisted imports
from twisted.internet import gtk2reactor
gtk2reactor.install() # install reactor for gui
from twisted.internet import reactor
from twisted.python import log

# Other imports
from error import __servfail__
from gui.clientGUIClass import clientGUIClass # get the main gui class
from gui.helper import helperFunc as hf
from options import parse_args

# access to server package
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
from server import start_server

if __name__ == '__main__':
    args = parse_args() # parse the arguments

    log.startLogging(sys.stdout)

    gui = clientGUIClass(args.client) # start the gui

    host, port = args.iface, args.port
    if host != None and hf.validate_host(host): # allow deafult connecting
        obj = gui.get_clientobj() # generate object
        result, factory = True, None
        if args.server:
            result, lisport, factory = start_server.listen(host, port)
        if result: # if everything goes well
            if factory: 
                obj.set_factory(lisport, factory)
            gui.connect(host, port, obj) # try to connect
        else: # incase server couldnt get started
            obj.updateView('server', __servfail__)

    reactor.run()
