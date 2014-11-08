#!/usr/bin/env python2

##
# PyGp
# https://github.com/leosartaj/PyGp.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

from twisted.internet import stdio
from twisted.python import log
from StdioChatClientProtocol import StdioChatClientProtocol

class ChatClientProtocol(StdioChatClientProtocol):
    """
    Implements the client interaction protocol
    """
    def connectionMade(self):
        main = StdioChatClientProtocol()
        main.use = self
        self.std = stdio.StandardIO(main) # start Stdio
        self.peer = self.transport.getPeer()
        log.msg('Connected to server at %s' % (self.peer)) # logs the connection
        setName = '$$' + self.factory.name
        self.sendLine(setName)
