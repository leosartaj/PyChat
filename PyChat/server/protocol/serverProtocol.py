#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

# twisted imports
from twisted.protocols import basic
from twisted.python import log

# user imports
from PyChat import command as cmd

# prefixes for commands
CLIENT_PREFIX = cmd.CLIENT_PREFIX

class serverProtocol(basic.LineReceiver):
    """
    Implements the server interaction protocol
    """
    from os import linesep as delimiter # os supported delimiter

    def connectionMade(self):
        self.peer = self.transport.getPeer()
        self.peername = 'unregistered'
        self.factory.updateClients(self)
        self.connectedUsers()
        log.msg('Connected to %s' %(self.peer))

    def lineReceived(self, line):
        """
        Handle recived lines
        """
        if not self._parse(line):
            log.msg('Received %s from %s' %(line, self.peername))
            msg = cmd.addFirst(line, self.peername)
            self.relay(msg)

    def _parse(self, line):
        """
        Parse line for commands
        returns True if line contains a command
        and calls the command
        otherwise simply returns False
        """
        comd, value = cmd.parse(line, CLIENT_PREFIX)
        if comd == 'reg':
            self.peername = value
            log.msg('PeerName of %s is %s' %(self.peer, self.peername))
            self.factory.updateUsers(self.peername, self.peer) # register name and ip with factory
            msg = cmd.addFirst(cmd.clientcmd('add', str(self.peer)), self.peername)
            self.relay(msg)
        else:
            return False
        return True

    def relay(self, line):
        """
        relay the message to other clients
        """
        #line = prefix + name + ' ' + line
        for client in self.factory.getClients():
            if client != self:
                client.sendLine(line)

    def connectedUsers(self):
        """
        Tells the client about already connected users
        """
        for name, ip in self.factory.getUsers():
            line = cmd.addFirst(cmd.clientcmd('add', str(ip)), name)
            print line
            self.sendLine(line)

    def connectionLost(self, reason):
        """
        safely disconnect user
        """
        self.factory.removeClients(self)
        self.factory.removeUsers(self.peername, self.peer)
        msg = cmd.addFirst(cmd.clientcmd('rem', str(self.peer)), self.peername)
        self.relay(msg)
        self._logConnectionLost(reason)

    def _logConnectionLost(self, reason):
        """
        log when connection is lost
        """
        line = 'Disconnected from %s' %(self.peer)
        log.msg(line)
        log.msg(reason.getErrorMessage())
