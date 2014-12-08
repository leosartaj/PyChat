#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

"""
Helper functions for starting a server
"""

# Twisted Imports
from twisted.internet import reactor
from twisted.internet.error import CannotListenError

# user imports
from protocol.serverFactory import serverFactory
from protocol.serverProtocol import serverProtocol

def listen(host, port):
    """
    Starts the server listening
    on the host and port
    returns True if server is setup
    otherwise returns False
    """
    factory = serverFactory() # initialize factory
    factory.protocol = serverProtocol 
    try:
        listener = reactor.listenTCP(port, factory, interface=host)
    except CannotListenError:
        return False, None, None # could not start
    return True, listener, factory
