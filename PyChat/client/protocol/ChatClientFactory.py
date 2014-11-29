#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

from twisted.python import log
from twisted.internet.protocol import ClientFactory

class ChatClientFactory(ClientFactory):
    """
    Implements the client factory
    """
    def __init__(self, clientobj, name, deferred):
        self.clientobj = clientobj
        self.name = name
        self.deferred = deferred

    def buildProtocoll(self, addr):
        proto = ClientFactory.buildProtocol(self, addr)
        return proto

    def clientConnectionFailed(self, connector, reason):
        log.err(reason.getErrorMessage())
        self._notify('Could Not Connect to Server')

    def clientConnectionLost(self, connector, reason):
        log.err(reason.getErrorMessage())
        self._notify('Connection to server has been lost')

    def _notify(self, msg):
        """
        Update the clientobj
        """
        self.clientobj.connectionLost(msg)
