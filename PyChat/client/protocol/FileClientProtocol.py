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
from twisted.python import log
from twisted.protocols import basic

# user import
from FileSender import FileSender

class FileClientProtocol(basic.LineReceiver):
    """
    Implements file transfer protocol
    """
    from os import linesep as delimiter # set delimiter

    def connectionMade(self, chatproto):
        self.chatproto = self.factory.chatproto
        self.receiving = False
        self.sending = False
        self.file = [None, None]

    def lineReceived(self, line):
        """
        Handles recieved file lines
        """
        line = self._parse(line)
        if line:
            log.msg('%s' % (line))
            self.chatproto.update(line)

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
        if cmd == 'file':
            value = self._saveFile(value)
        elif cmd == 'eof':
            value = self._closeFile(value)
        else:
            return line
        return value

    def sendFile(self, fName):
        """
        Sends file to the server
        """
        log.msg('me sending %s' % (fName))
        handler = open(fName)
        self.sending = True
        fileprotocol = FileSender()
        sendfile, startsend = fileprotocol.beginFileTransfer(handler, self.transport, self.transform)
        sendfile.addCallback(self._endTransfer)
        sendfile.addErrback(self._sendingFailed)
        startsend.callback(1)

    def transform(self, line):
        """
        Transforms a line to be saved in a file
        """
        lineArr = line.split('\n')
        for index, item in enumerate(lineArr):
            item = 'c$~file~' + self.file[0] + ':' + item
            lineArr[index] = item
        fileLine = '\n'.join(lineArr)
        return fileLine

    def _endTransfer(self, *args):
        """
        End file transfer
        """
        lastline = 'c$~eof~' + self.file[0] # file sending complete
        self.sendLine(lastline)

    def _sendingFailed(self, exc):
        log.msg(exc)
        msg = 'me File Sending failed'
        self.chatproto.update(msg)

    def _initFile(self, fName='unnamed', dire=os.getcwd(), prefix='pychat_'):
        """
        opens a file
        returns the handler
        """
        path = os.path.join(dire, prefix + fName)
        handler = open(path, 'w')
        return handler

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
        if not self.receiving:
            handler = self._initFile(fName)
            self.file = [fName, handler]
            value = peername + ' Recieving: ' + fName
            self.receiving = True
        elif fName == self.file[0]:
            handler = self.file[1]
            value = None
        else:
            print 'no'
            return
        handler.write(fline + '\n')
        return value

    def _closeFile(self, value):
        """
        safely closes the file
        cleans up rfiles dict
        returns the result
        """
        index = value.index(' ')
        peername, fName = value[:index], value[index + 1:]
        handler = self.file[1]
        handler.close()
        self.file = [None, None]
        self.receiving = False
        value = peername + ' Recieved: ' + fName
        return value
