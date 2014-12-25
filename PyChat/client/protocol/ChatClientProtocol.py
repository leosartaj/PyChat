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
import os

# twisted imports
from twisted.python import log
from twisted.protocols import basic

# user imports
from FileClientProtocol import FileClientProtocol

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
        self.rfiles = {} # list of files being recieved

        log.msg('Connected to server at %s' % (self.peer)) # logs the connection
        self.update('server Connected')

        setName = 'c$~reg~' + self.factory.name
        self.sendLine(setName) # register with server

    def send(self, text):
        """
        Logs and sends the messages
        """
        log.msg('me %s' % (text))
        self.sendLine(text)

    def sendFile(self, fName):
        """
        Sends file to the server
        """
        log.msg('me sending %s' % (fName))
        handler = open(fName)
        self.filename = fName
        fileprotocol = FileClientProtocol()
        sendfile = fileprotocol.beginFileTransfer(handler, self.transport, self.transform)
        sendfile.addBoth(self._endTransfer, self._sendingFailed)

    def transform(self, line):
        """
        Transforms a line to be saved in a file
        """
        lineArr = line.split('\n')
        for index, item in enumerate(lineArr):
            if not item.startswith('c$~eof~'):
                item = 'c$~file~' + self.filename + ':' + item
                lineArr[index] = item
        fileLine = '\n'.join(lineArr)
        return fileLine

    def _endTransfer(self, *args):
        """
        End file transfer
        """
        lastline = 'c$~eof~' + self.filename # file sending complete
        self.sendLine(lastline)

    def _sendingFailed(self, exc):
        log.msg(exc)
        msg = 'me File Sending failed'
        self.update(msg)

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
        elif cmd == 'file':
            value = self._saveFile(value)
        elif cmd == 'eof':
            value = self._closeFile(value)
        else:
            return line
        return value

    def _saveFile(self, value):
        """
        Parses the line
        saves the line in the file
        returns the result string
        """
        index = value.index(' ')
        peername, nameline = value[:index], value[index + 1:]
        index = nameline.index(':')
        fName, fline = nameline[:index], nameline[index + 1:]
        if not self.rfiles.has_key(fName):
            handler = self._initFile(fName)
            self.rfiles[fName] = handler
            value = peername + ' Recieving: ' + fName
        else:
            handler = self.rfiles[fName]
            value = None
        handler.write(fline + '\n')
        return value

    def _closeFile(self, value):
        """
        safely closes the file
        cleans up rfiles dict
        returns the result
        """
        print 'called'
        index = value.index(' ')
        peername, fName = value[:index], value[index + 1:]
        handler = self.rfiles[fName]
        handler.close()
        del self.rfiles[fName]
        value = peername + ' Recieved: ' + fName
        return value

    def _initFile(self, fName='unnamed', dire=os.getcwd(), prefix='pychat_'):
        """
        opens a file
        returns the handler
        """
        path = os.path.join(dire, prefix + fName)
        handler = open(path, 'w')
        return handler

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
