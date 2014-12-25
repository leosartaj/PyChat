#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

from twisted.python import log
from twisted.internet.protocol import ClientFactory

class FileClientFactory(ClientFactory):
    """
    Implements the client factory
    """
    def __init__(self, chatproto):
        self.chatproto = chatproto # save the chat protocols refrence

    def buildProtocoll(self, addr):
        proto = ClientFactory.buildProtocol(self, addr)
        return proto

    def clientConnectionFailed(self, connector, reason):
        log.err(reason.getErrorMessage())

    def clientConnectionLost(self, connector, reason):
        log.err(reason.getErrorMessage())
