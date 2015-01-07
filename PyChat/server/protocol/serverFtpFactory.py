#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

from twisted.internet.protocol import ServerFactory

class serverFtpFactory(ServerFactory):
    """
    Implements the server Ftp factory
    """
    def __init__(self):
        self.clients = []

    def updateClients(self, client):
        """
        Adds protocol instances of connected clients
        """
        self.clients.append(client)

    def getClients(self):
        """
        returns list of protocol instances of connected clients
        """
        return self.clients

    def disconnect(self):
        """
        Disconnects from all the clients
        """
        for client in self.clients:
            client.transport.loseConnection()

    def removeClients(self, client):
        """
        removes protocol instances of connected clients
        """
        index = self.clients.index(client)
        del self.clients[index]
