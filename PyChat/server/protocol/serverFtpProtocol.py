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

class serverFtpProtocol(basic.LineReceiver):
    """
    Implements the server ftp protocol
    """
    from os import linesep as delimiter # os supported delimiter

    def connectionMade(self):
        self.peer = self.transport.getPeer()
        self.factory.updateClients(self)

    def lineReceived(self, line):
        """
        Handle recived lines
        """
        self._parse(line)

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
        elif cmd == 'file' or cmd == 'eof' or cmd == 'fail':
            prefix = 's$~' + cmd + '~'
            self.relay(value, self.peername, prefix)
        else:
            return False
        return True

    def relay(self, line, name='', prefix=''):
        """
        relay the message to other clients
        """
        line = prefix + name + ' ' + line
        for client in self.factory.getClients():
            if client != self:
                client.sendLine(line)

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
