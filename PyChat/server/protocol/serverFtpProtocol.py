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
import command as cmd

# prefix for commands
CLIENT_PREFIX = cmd.CLIENT_PREFIX

class serverFtpProtocol(basic.Int32StringReceiver):
    """
    Implements the server ftp protocol
    """
    def connectionMade(self):
        self.peer = self.transport.getPeer()
        self.recv = False # whether server is receiving a file
        self.sendingto = [] # list of clients file is getting send to
        self.factory.updateClients(self)

    def stringReceived(self, line):
        """
        Handle received messages
        """
        if not self._parse(line):
            tosend = cmd.addFirst(line, self.peername)
            self.relay(tosend)

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
        elif comd == 'eof':
            self._reset()
            msg = cmd.clientcmd(comd, value)
            msg = cmd.addFirst(msg, self.peername)
            self.sendString(msg)
        elif comd = 'fail':
            self._reset()
        else:
            return False
        return True

    def relay(self, line):
        """
        relay the message to other clients
        """
        if not self.recv:
            self.recv = True
            self.sendingto = list(self.factory.getClients())
        for client in self.sendingto:
            if client != self:
                client.sendString(line)

    def _reset(self):
        """
        Reset variables
        """
        self.recv = False
        self.sendingto = []

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
