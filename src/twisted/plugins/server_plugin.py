#!/usr/bin/env python2

##
# PyGp
# https://github.com/leosartaj/PyGp.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

from zope.interface import implements
from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application import internet, service
import sys
#sys.path.insert(0, os.path.abspath(os.getcwd()))
from server.serverFactory import serverFactory
from server.serverProtocol import serverProtocol

class Options(usage.Options):

    optParameters = [
        ['port', 'p', 8001, 'The port number to listen on.'],
        ['iface', 'i', 'localhost', 'The interface to listen on.'],
        ]

class ChatServiceMaker(object):

    implements(service.IServiceMaker, IPlugin)

    tapname = "PyGp"
    description = "A Chat Client"
    options = Options

    def makeService(self, options):
        top_service = service.MultiService()

        factory = serverFactory()
        factory.protocol = serverProtocol

        tcp_service = internet.TCPServer(int(options['port']), factory, interface=options['iface'])
        tcp_service.setServiceParent(top_service)

        return top_service

service_maker = ChatServiceMaker()
