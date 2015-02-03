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
from PyChat import command as cmd

# prefixes for commands
SERVER_PREFIX = cmd.SERVER_PREFIX
CLIENT_PREFIX = cmd.CLIENT_PREFIX

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
        self.update('server', 'Connected')

        self.setName = setName = cmd.servercmd('reg', self.factory.name)
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
                self.update('me', msg)
        else:
            msg = 'Cannot send: %s' %(os.path.basename(fName))
            msg2 = 'Not connected to ftp server'
            log.msg(msg2)
            self.update('me', msg2)
        log.msg(msg)
        self.update('me', msg)

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
        if text.startswith(CLIENT_PREFIX):
            text = '\\' + text
        return text

    def lineReceived(self, line):
        """
        Handles recieved line
        """
        peername, line = self._parse(line)
        if line != None:
            log.msg('%s %s' % (peername, line))
            self.update(peername, line)

    def _parse(self, line):
        """
        Parse line for commands
        returns string to be logged 
        otherwise simply returns line without change
        """
        peername, line = cmd.extractFirst(line)
        comd, value = cmd.parse(line, SERVER_PREFIX)
        if comd == 'add' or comd == 'rem':
            value = self._handleUser(peername, value, comd)
        else:
            return peername, line
        return peername, value

    def _handleUser(self, peername, line, comd=None):
        """
        Stores useful information about new connected user
        adds a tuple of name and ip address of user
        updates the client object
        """
        lineArr = line.split(' ')
        ip = ' '.join(lineArr)
        line = 'has '

        if comd == 'add':
            self.users.append((peername, ip))
            line += 'joined'
        elif comd == 'rem':
            del self.users[self.users.index((peername, ip))]
            line += 'disconnected'

        self.clientobj.updateConnUsers(peername)

        return line

    def update(self, name, msg):
        """
        updates on the big screen
        """
        self.clientobj.updateView(name, msg)
