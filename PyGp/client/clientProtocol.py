#!/usr/bin/env python2

##
# PyGp
# https://github.com/leosartaj/PyGp.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

import sys
from getpass import getuser
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.protocols import basic
from twisted.internet import reactor
from twisted.internet import stdio
from twisted.python import log

class StdioChatClientProtocol(basic.LineReceiver):
    """
    logs input from server
    and sends input from user to server
    """
    from os import linesep as delimiter # set delimiter

    def lineReceived(self, line):
        if line[0:2] == '~~':
            log.msg('%s' % (line[2:]))
        else:
            self.use.sendLine(line)

class ChatClientProtocol(StdioChatClientProtocol):
    """
    Implements the client interaction protocol
    """

    def connectionMade(self):
        main = StdioChatClientProtocol()
        main.use = self
        self.std = stdio.StandardIO(main) # start Stdio
        self.name = getuser()
        self.peer = self.transport.getPeer()
        log.msg('Connected to server at %s' % (self.peer)) # logs the connection
        setName = '$$' + self.name
        self.sendLine(setName)

class ChatClientFactory(ClientFactory):
    """
    Implements the client factory
    """
    protocol = ChatClientProtocol

    def buildProtocoll(self, addr):
        proto = ClientFactory.buildProtocol(self, addr)
        return proto

    def clientConnectionFailed(self, connector, reason):
        log.err(reason.getErrorMessage())

    def clientConnectionLost(self, connector, reason):
        log.err(reason.getErrorMessage())

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    factory = ChatClientFactory()
    reactor.connectTCP('10.42.0.1', 6969, factory)
    reactor.run()
