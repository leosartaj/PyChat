#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

"""
implements the server as a twistd plugin
"""

# twisted imports
from zope.interface import implements
from twisted.plugin import IPlugin
from twisted.application import internet, service

# user imports
from PyChat.server.protocol.serverFactory import serverFactory
from PyChat.server.protocol.serverProtocol import serverProtocol
from PyChat.server.options import Options # custom options

class ChatServiceMaker(object):
    """
    implements PyChat as a twistd plugin
    """
    implements(service.IServiceMaker, IPlugin)

    tapname = "PyChat"
    description = "A Chat Client"
    options = Options

    def makeService(self, options):
        top_service = service.MultiService() # parent service

        factory = serverFactory() # initialize factory
        factory.protocol = serverProtocol 

        tcp_service = internet.TCPServer(int(options['port']), factory, interface=options['iface'])
        tcp_service.setServiceParent(top_service) # add the service

        return top_service

service_maker = ChatServiceMaker() # initializing
