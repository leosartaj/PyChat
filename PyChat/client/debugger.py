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
from gui.clientGUIClass import clientGUIClass # get the main gui class
from gui.helper import helperFunc as hf
from options import parse_args

if __name__ == '__main__':
    args = parse_args() # parse the arguments

    log.startLogging(sys.stdout)

    gui = clientGUIClass(args.client) # start the gui

    if args.iface != None: # allow deafult connecting
        if hf.validate_host(args.iface):
            gui.connect(args.iface, args.port)

    reactor.run()

