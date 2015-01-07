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

class serverFtpProtocol(basic.Int32StringReceiver):
    """
    Implements the server ftp protocol
    """
    def connectionMade(self):
        self.peer = self.transport.getPeer()
        self.recv = False # whether server is receiving a file
        self.sending = [] # list of clients file is getting send to
        self.factory.updateClients(self)

    def stringReceived(self, line):
        """
        Handle received messages
        """
        if not self._parse(line):
            self.relay(line, self.peername)

    def _parse(self, line):
        """
        Parse line for commands
        returns True if line contains a command
        and calls the command
        otherwise simply returns False
        """
        if line[0:3] != 'c$~':
            return False
        line = line[3:]
        index = line.index('~')
        cmd, value = line[:index], line[index + 1:]
        if cmd == 'reg':
            self.peername = value
        elif cmd == 'eof':
            self.recv = False
            self.sending = []
        else:
            return False
        return True

    def relay(self, line, name='', prefix=''):
        """
        relay the message to other clients
        """
        if not self.recv:
            self.recv = True
            self.sending = list(self.factory.getClients())
        line = prefix + name + ' ' + line
        for client in self.sending:
            if client != self:
                client.sendString(line)

    def connectionLost(self, reason):
        """
        safely disconnect user
        """
        self.factory.removeClients(self)
        self._logConnectionLost(reason)

    def _logConnectionLost(self, reason):
        """
        log when connection is lost
        """
        line = 'Disconnected ftp from %s' %(self.peer)
        log.msg(line)
        log.msg(reason.getErrorMessage())
