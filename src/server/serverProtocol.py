#!/usr/bin/env python2

##
# PyGp
# https://github.com/leosartaj/PyGp.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

from twisted.protocols import basic
from twisted.internet.protocol import ServerFactory
from twisted.python import log

class serverProtocol(basic.LineReceiver):
    """
    Implements the server interaction protocol
    """
    def connectionMade(self):
        self.peer = self.transport.getPeer()
        self.factory.updateClients(self)
        log.msg('Connected to %s' %(self.peer))

    def lineReceived(self, line):
        if line[0:2] == '$$':
            self.peerName = line[2:]
            log.msg('PeerName of %s is %s' %(self.peer, self.peerName))
        else:
            log.msg('Received %s' %(line))
            self.relay(line)

    def relay(self, line):
        for client in self.factory.getClients():
            if client != self:
                client.sendLine(line)

    def connectionLost(self, reason):
        self.factory.removeClients(self)
        log.msg('Disconnected from %s' %(self.peer))
        log.msg(reason.getErrorMessage())

class serverFactory(ServerFactory):
    """
    Implements the server factory
    """
    protocol = serverProtocol

    def __init__(self):
        self.clients = []

    def updateClients(self, client):
        self.clients.append(client)

    def getClients(self):
        return self.clients

    def removeClients(self, client):
        index = self.clients.index(client)
        del self.clients[index]
