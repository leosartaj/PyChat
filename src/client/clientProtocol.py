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
from twisted.internet.protocol import ClientFactory
from twisted.protocols import basic
from twisted.internet import reactor
from twisted.python import log

class clientProtocol(basic.LineReceiver):
    """
    Implements the client interaction protocol
    """
    def connectionMade(self):
        self.name = getuser()
        self.peer = self.transport.getPeer()
        log.msg('Connected to server at %s' % (self.peer))
        setName = '$$' + self.name
        self.sendLine(setName)

    def lineReceived(self, line):
        log.msg('%s' % (line))


class clientFactory(ClientFactory):
    """
    Implements the client factory
    """
    protocol = clientProtocol

    def clientConnectionFailed(self, connector, reason):
        log.err(reason.getErrorMessage())

    def clientConnectionLost(self, connector, reason):
        log.err(reason.getErrorMessage())

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    factory = clientFactory()
    reactor.connectTCP('127.0.0.1', 8001, factory)
    reactor.run()
