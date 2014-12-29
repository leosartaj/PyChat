#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory
from twisted.internet.error import CannotListenError

from serverFtpFactory import serverFtpFactory
from serverFtpProtocol import serverFtpProtocol

class serverFactory(ServerFactory):
    """
    Implements the server factory
    """
    def __init__(self):
        self.clients = [] # connected clients
        self.users = [] # name and ip of connected clients

    def startFtp(self, host, port):
        self.host, self.ftp_port = host, port
        self.ftpfactory = factory = serverFtpFactory() # initialize factory
        factory.protocol = serverFtpProtocol 
        factory.server = self
        try:
            listener = reactor.listenTCP(port, factory, interface=host)
        except CannotListenError:
            log.msg('Ftp server failed to start')

    def updateClients(self, client):
        """
        Adds protocol instances of connected clients
        """
        self.clients.append(client)

    def updateUsers(self, name, ip):
        """
        Registers names and ips of connected clients
        """
        self.users.append((name, ip))

    def getClients(self):
        """
        returns list of protocol instances of connected clients
        """
        return self.clients

    def getUsers(self):
        """
        returns list of tuples of name and ip of connected clients
        """
        return self.users

    def getPeername(self, ip):
        for user in self.getUsers:
            if user[1] == ip:
                return user[0]
        return None

    def disconnect(self):
        """
        Disconnects from all the clients
        """
        for client in self.clients:
            client.transport.loseConnection()

    def removeUsers(self, name, ip):
        """
        returns list of tuples of name and ip of connected clients
        """
        index = self.users.index((name, ip))
        del self.users[index]

    def removeClients(self, client):
        """
        removes protocol instances of connected clients
        """
        index = self.clients.index(client)
        del self.clients[index]
