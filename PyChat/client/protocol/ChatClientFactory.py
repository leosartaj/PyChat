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
    def __init__(self, gui, name, deferred):
        self.gui = gui
        self.name = name
        self.deferred = deferred

    def buildProtocoll(self, addr):
        proto = ClientFactory.buildProtocol(self, addr)
        return proto

    def clientConnectionFailed(self, connector, reason):
        log.err(reason.getErrorMessage())
        self._stopReactor('Could Not Connect to Server')

    def clientConnectionLost(self, connector, reason):
        log.err(reason.getErrorMessage())
        self._stopReactor('Connection to server has been lost')

    def _stopReactor(self, msg):
        """
        Fire the deferred
        """
        if self.deferred is not None:
            d, self.deferred = self.deferred, None
            d.callback(msg)
