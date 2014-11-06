#!/usr/bin/env python2

##
# PyGp
# https://github.com/leosartaj/PyGp.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

from twisted.internet.protocol import ServerFactory

class serverFactory(ServerFactory):
    """
    Implements the server factory
    """
    def __init__(self):
        self.clients = []

    def updateClients(self, client):
        self.clients.append(client)

    def getClients(self):
        return self.clients

    def removeClients(self, client):
        index = self.clients.index(client)
        del self.clients[index]
