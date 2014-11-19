#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

"""
Handles connection related functionality
"""

# Twisted imports
from twisted.internet import defer
from twisted.internet import reactor

# protocol
from protocol.ChatClientFactory import ChatClientFactory
from protocol.ChatClientProtocol import ChatClientProtocol

def start_factory(gui, host, port, client='default'):
    """
    Starts the factory
    """
    deferred = defer.Deferred()
    factory = ChatClientFactory(gui, client, deferred) # setting up the factory
    factory.protocol = ChatClientProtocol
    reactor.connectTCP(host, port, factory)
    return deferred

def setup_factory(gui, host, port, client='default'):
    """
    Sets up the factory
    sets up the deferred
    """
    deferred = start_factory(gui, host, port, client)
