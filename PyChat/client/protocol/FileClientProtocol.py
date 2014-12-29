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

    def connectionMade(self):
        self.chatproto = self.factory.chatproto
        self.register()
        self.receiving = False
        self.sending = False
        self.sfile = [None, None]
        self.rfile = {}

    def register(self):
        """
        Register with the ftp server
        send the refrence to the chatproto
        """
        self.sendLine(self.chatproto.setName)
        if self.factory.deferred:
            deferred, self.factory.deferred = self.factory.deferred, None
            deferred.callback(self)

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
        elif cmd == 'fail':
            value = self._closeFile(value, False)
        else:
            return line
        return value

    def sendFile(self, fName):
        """
        Sends file to the server
        """
        handler = open(fName)
        self.sending = True
        self.sfile = [fName, handler]
        fileprotocol = FileSender()
        sendfile, startsend = fileprotocol.beginFileTransfer(handler, self.transport, self.transform)
        sendfile.addCallback(self._endTransfer)
        sendfile.addErrback(self._sendingFailed)
        sendfile.addBoth(self._reset)
        startsend.callback(1)

    def transform(self, line):
        """
        Transforms a line to be saved in a file
        """
        line = line.strip('\n')
        lineArr = line.split('\n')
        for index, item in enumerate(lineArr):
            item = 'c$~file~' + self.sfile[0] + ':' + item
            lineArr[index] = item
        fileLine = '\n'.join(lineArr)
        return fileLine

    def _endTransfer(self, *args):
        """
        End file transfer
        """
        # Buggy
        # dont know why the lastline goes through the transform function
        lastline = 'c$~eof~' + self.sfile[0] + ':' # file sending complete
        self.sendLine('')
        self.sendLine(lastline)

    def _sendingFailed(self, exc):
        log.msg(exc)
        msg = 'me File Sending failed'
        self.chatproto.update(msg)
        self.sendLine('')
        failed = 'c$~fail~' + self.sfile[0] + ':'
        self.sendLine(failed)

    def _reset(self, *args):
        """
        Reset the variables
        """
        self.sending = False
        self.sfile = [None, None]

    def _initFile(self, fName='unnamed', dire=os.getcwd(), prefix='pychat_'):
        """
        opens a file
        returns the handler
        """
        path = os.path.join(dire, prefix + fName)
        handler = open(path, 'w')
        return handler

    def _parseFileline(self, fline):
        """
        Parses the fline
        extracts information
        """
        parsed = {}
        index = fline.index(' ')
        parsed['peername'], nameline = fline[:index], fline[index + 1:]
        index = nameline.index(':')
        parsed['fName'], parsed['fline'] = nameline[:index], nameline[index + 1:]
        return parsed

    def _saveFile(self, value):
        """
        Parses the line
        saves the line in the file
        returns the result string
        """
        parsed = self._parseFileline(value)
        peername, fName, fline = parsed['peername'], parsed['fName'], parsed['fline']
        if not self.receiving:
            handler = self._initFile(fName)
            self.rfile[fName] = handler
            value = peername + ' Recieving: ' + fName
            self.receiving = True
        elif self.rfile.has_key(fName):
            handler = self.rfile[fName]
            value = None
        else:
            return
        handler.write(fline + '\n')
        return value

    def _closeFile(self, parsed, status=True):
        """
        safely closes the file
        cleans up rfiles dict
        returns the result
        """
        self.receiving = False
        parsed = self._parseFileline(parsed)
        peername, fName = parsed['peername'], parsed['fName']
        handler = self.rfile[fName]
        handler.close()
        del self.rfile[fName]
        if status:
            value = peername + ' Recieved: ' + fName
        else:
            value = peername + ' File could not be received: ' + fName
        return value
