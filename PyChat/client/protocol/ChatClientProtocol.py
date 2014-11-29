#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

# system import
import sys

# twisted imports
from twisted.python import log
from twisted.protocols import basic 

class ChatClientProtocol(basic.LineReceiver):
    """
    Implements the client interaction protocol
    """
    from os import linesep as delimiter # set delimiter

    def connectionMade(self):
        self.clientobj = self.factory.clientobj # refrence to the client object
        self.clientobj.protocol = self # give your refrence to the client object

        self.peer = self.transport.getPeer()
        self.users = [] # list of connnected users

        log.msg('Connected to server at %s' % (self.peer)) # logs the connection
        self.update('server Connected')

        setName = 'c$~' + self.factory.name
        self.sendLine(setName) # register with server

    def send(self, text):
        """
        Logs and sends the messages
        """
        log.msg('me %s' % (text))
        self.sendLine(text)

    def lineReceived(self, line):
        if line[0:3] == 's$~':
            line = self.handleUser(line[3:])
        log.msg('%s' % (line))
        self.update(line)

    def handleUser(self, line):
        """
        Stores useful information about new connected user
        adds a tuple of name and ip address of user
        updates the client object
        """
        lineArr = line.split(' ')
        line = lineArr[1] + ' has '
        ip = ' '.join(lineArr[2:])

        if lineArr[0] == 'add':
            self.users.append((lineArr[1], ip))
            line += 'joined'
        elif lineArr[0] == 'rem':
            del self.users[self.users.index((lineArr[1], ip))]
            line += 'disconnected'

        self.clientobj.updateConnUsers(lineArr[1])

        return line

    def update(self, line):
        """
        Extracts name and message
        updates on the big screen
        """
        line = line.split(' ')
        name = line[0]
        msg = ' '.join(line[1:])

        self.clientobj.updateView(name, msg)
