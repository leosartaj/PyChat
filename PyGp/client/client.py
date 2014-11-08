#!/usr/bin/env python2

##
# PyGp
# https://github.com/leosartaj/PyGp.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

"""
Runs the client 
"""

# system imports
import sys
from twisted.internet import reactor
from twisted.python import log
from twisted.internet import defer

# user imports
from protocol.ChatClientFactory import ChatClientFactory
from protocol.ChatClientProtocol import ChatClientProtocol
from defer import * # import all the callbacks and errbacks
from parse_args import parse_args

def start_factory(options):
    """
    Starts the factory
    """
    deferred = defer.Deferred()
    factory = ChatClientFactory(options.name, deferred) # setting up the factory
    factory.protocol = ChatClientProtocol
    reactor.connectTCP(HOST, options.port, factory)
    return deferred


if __name__ == '__main__':
    options, HOST = parse_args() # parse the arguments

    deferred = start_factory(options)
    deferred.addBoth(stop_log) 
    deferred.addBoth(stop_reactor) 

    log.startLogging(sys.stdout) 
    reactor.run()
