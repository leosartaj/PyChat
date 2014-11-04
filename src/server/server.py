#!/usr/bin/env python2

##
# PyGp
# https://github.com/leosartaj/PyGp.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

import sys
from twisted.python import log
from twisted.internet import reactor
from serverProtocol import serverFactory

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    factory = serverFactory()
    reactor.listenTCP(8001, factory, interface='localhost')
    reactor.run()
