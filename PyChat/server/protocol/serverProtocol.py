#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
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
        self.connectedUsers()
        log.msg('Connected to %s' %(self.peer))

    def lineReceived(self, line):
        """
        Handle recived lines
        """
        if line[0:3] == 'c$~':
            self.peername = line[3:]
            log.msg('PeerName of %s is %s' %(self.peer, self.peername))
            self.factory.updateUsers(self.peername, self.peer) # register name and ip with factory
            self.relay(str(self.peer), self.peername, 's$~add ')
        else:
            log.msg('Received %s from %s' %(line, self.peername))
            self.relay(line, self.peername)

    def relay(self, line, name='', prefix=''):
        """
        relay the message to other clients
        """
        line = prefix + name + ' ' + line
        for client in self.factory.getClients():
            if client != self:
                client.sendLine(line)

    def connectedUsers(self):
        """
        Tells the client about already connected users
        """
        for name, ip in self.factory.getUsers():
            line = 's$~add ' + name + ' ' + str(ip)
            self.sendLine(line)

    def connectionLost(self, reason):
        """
        safely disconnect user
        """
        self.factory.removeClients(self)
        self.factory.removeUsers(self.peername, self.peer)
        self.relay(str(self.peer), self.peername, 's$~rem ')
        self._logConnectionLost(reason)

    def _logConnectionLost(self, reason):
        """
        log when connection is lost
        """
        line = 'Disconnected from %s' %(self.peer)
        log.msg(line)
        log.msg(reason.getErrorMessage())
