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
from PyChat.client.error import __ftpfail__, __ftplost__

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
        self._notify(__ftpfail__)

    def clientConnectionLost(self, connector, reason):
        log.err(reason.getErrorMessage())
        self.chatproto.forgetFtp() # lose the reference
        self._notify(__ftplost__)

    def _notify(self, msg):
        """
        notify
        """
        self.chatproto.update('server', msg)
