#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

from twisted.internet import stdio
from twisted.python import log
from twisted.protocols import basic

import sys
try:
    from PyChat.client.gui.clientGUIClass import clientGUIClass
except ImportError: # for debugging
    sys.path.insert(0, '../gui') # allows importing modules from different directory
    from gui.clientGUIClass import clientGUIClass

class ChatClientProtocol(basic.LineReceiver):
    """
    Implements the client interaction protocol
    """
    from os import linesep as delimiter # set delimiter

    def connectionMade(self):
        self.gui = clientGUIClass(self)
        self.peer = self.transport.getPeer()
        log.msg('Connected to server at %s' % (self.peer)) # logs the connection
        setName = '$$' + self.factory.name
        self.sendLine(setName)

    def lineReceived(self, line):
        log.msg('%s' % (line))

        # extract name and message
        line = line.split(' ')
        name = line[0] 
        msg = ' '.join(line[1:])

        self.gui.updateTextView(name, msg)
