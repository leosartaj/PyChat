#!/usr/bin/env python2

##
# PyGp
# https://github.com/leosartaj/PyGp.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

from twisted.protocols import basic
from twisted.python import log

class serverProtocol(basic.LineReceiver):
    """
    Implements the server interaction protocol
    """
    from os import linesep as delimiter # os supported delimiter

    def connectionMade(self):
        self.peer = self.transport.getPeer()
        self.factory.updateClients(self)
        log.msg('Connected to %s' %(self.peer))

    def lineReceived(self, line):
        """
        Handle recived lines
        """
        if line[0:2] == '$$':
            self.peername = line[2:]
            log.msg('PeerName of %s is %s' %(self.peer, self.peername))
            self.relay('has joined')
        else:
            log.msg('Received %s' %(line))
            self.relay(line)

    def relay(self, line):
        """
        relay the message to other clients
        """
        line = '~~' + self.peername + ' >>> ' + line
        for client in self.factory.getClients():
            if client != self:
                client.sendLine(line)

    def connectionLost(self, reason):
        """
        safely disconnect user
        """
        self.factory.removeClients(self)
        self.relay('has been disconnected')
        self._logConnectionLost(reason)

    def _logConnectionLost(self, reason):
        """
        log when connection is lost
        """
        line = 'Disconnected from %s' %(self.peer)
        log.msg(line)
        log.msg(reason.getErrorMessage())
