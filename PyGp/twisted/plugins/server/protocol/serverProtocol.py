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
        if line[0:2] == '$$':
            self.peername = line[2:]
            log.msg('PeerName of %s is %s' %(self.peer, self.peername))
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
        self.factory.removeClients(self)
        log.msg('Disconnected from %s' %(self.peer))
        log.msg(reason.getErrorMessage())
