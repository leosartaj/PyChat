#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

# system import
import os

# twisted imports
from twisted.internet import reactor, defer
from twisted.python import log
from twisted.protocols import basic

# user imports
from FileClientFactory import FileClientFactory
from FileClientProtocol import FileClientProtocol

class ChatClientProtocol(basic.LineReceiver):
    """
    Implements the client interaction protocol
    """
    from os import linesep as delimiter # set delimiter

    def connectionMade(self):
        self.clientobj = self.factory.clientobj # refrence to the client object
        self.clientobj.protocol = self # give your refrence to the client object

        # ip address and port connection
        self.host = self.factory.host 
        self.port = self.factory.port
        self.ftp = None # refrence of the ftp protocol

        self.peer = self.transport.getPeer()
        self.users = [] # list of connnected users

        log.msg('Connected to server at %s' % (self.peer)) # logs the connection
        self.update('server Connected')

        self.setName = setName = 'c$~reg~' + self.factory.name
        self.sendLine(setName) # register with server
        self.startFtp(self.host, 6969)

    def startFtp(self, host, port):
        """
        Open up file transfer connection with server
        """
        self.ftpfactory = factory = FileClientFactory(self) # setting up the factory
        factory.protocol = FileClientProtocol
        factory.deferred = defer.Deferred()
        factory.deferred.addCallback(self.registerFtp) # Called to register ftp refrence
        reactor.connectTCP(host, port, factory)

    def forgetFtp(self):
        """
        Forgets ftp connection
        """
        self.ftp = None

    def registerFtp(self, ftp):
        """
        Registers reference to the ftp protocol
        """
        self.ftp = ftp

    def sendFile(self, fName):
        """
        Instructs the ftp protocol to send file
        """
        if self.ftp:
            if not self.ftp.status():
                msg = 'Sending File: ' + os.path.basename(fName)
                self.ftp.sendFile(fName)
            else:
                msg = 'Already sending file. Cannot send: %s' %(os.path.basename(fName))
                self.update('me ' + msg)
        else:
            msg = 'Cannot send: %s' %(os.path.basename(fName))
            msg2 = 'Not connected to ftp server'
            log.msg(msg2)
            self.update('me ' + msg2)
        log.msg(msg)
        self.update('me ' + msg)

    def send(self, text):
        """
        Logs and sends the messages
        """
        text = self._escape(text)
        log.msg('me %s' % (text))
        self.sendLine(text)

    def _escape(self, text):
        """
        Escapes commands that user may enter
        accidentally or not
        """
        if text.startswith('c$~'):
            text = '\\' + text
        return text

    def lineReceived(self, line):
        """
        Handles recieved line
        """
        line = self._parse(line)
        if line != None:
            log.msg('%s' % (line))
            self.update(line)

    def _parse(self, line):
        """
        Parse line for commands
        returns string to be logged 
        otherwise simply returns line without change
        """
        if line[0:3] != 's$~':
            return line
        newline = line[3:]
        index = newline.index('~')
        cmd, value = newline[:index], newline[index + 1:]
        if cmd == 'add' or cmd == 'rem':
            value = self._handleUser(value, cmd)
        else:
            return line
        return value

    def _handleUser(self, line, cmd=None):
        """
        Stores useful information about new connected user
        adds a tuple of name and ip address of user
        updates the client object
        """
        lineArr = line.split(' ')
        line = lineArr[0] + ' has '
        ip = ' '.join(lineArr[1:])

        if cmd == 'add':
            self.users.append((lineArr[0], ip))
            line += 'joined'
        elif cmd == 'rem':
            del self.users[self.users.index((lineArr[0], ip))]
            line += 'disconnected'

        self.clientobj.updateConnUsers(lineArr[0])

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
