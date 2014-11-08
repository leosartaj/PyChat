#!/usr/bin/env python2

##
# PyGp
# https://github.com/leosartaj/PyGp.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

from twisted.protocols import basic
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
