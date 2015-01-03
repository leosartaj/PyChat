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
import struct
import cPickle as pickle

# twisted imports
from twisted.python import log
from twisted.protocols import basic

# user import
from FileSender import FileSender

def dict_to_pickle(pickle_dict):
    """
    convert from a dictionary to pickle
    """
    return pickle.dumps(pickle_dict)

def pickle_to_dict(pickle_str):
    """
    convert from pickle to dictionary
    """
    return pickle.loads(pickle_str)

class FileClientProtocol(basic.Int32StringReceiver):
    """
    Implements file transfer protocol
    """
    def connectionMade(self):
        self.chatproto = self.factory.chatproto
        self._register()
        self.sending = False
        self.sfile = [None, None]
        self.rfile = {}

    def _register(self):
        """
        Register with the ftp server
        send the refrence to the chatproto
        """
        self.sendString(self.chatproto.setName)
        if self.factory.deferred:
            deferred, self.factory.deferred = self.factory.deferred, None
            deferred.callback(self)

    def stringReceived(self, line):
        """
        Handles recieved file lines
        """
        line = self._parse(line)
        if line:
            log.msg('%s' % (line))
            self.chatproto.update(line)

    def _parseline(self, fline):
        """
        Parses the fline
        extracts information
        """
        index = fline.index(' ')
        peername, pickle_str = fline[:index], fline[index + 1:]
        return peername, pickle_str

    def _parse(self, line):
        """
        Parse line for commands
        returns string to be logged 
        otherwise simply returns line without change
        """
        peername, pickle_str = self._parseline(line)
        pickle_dict = pickle_to_dict(pickle_str)
        value = self._parseDict(peername, pickle_dict)
        return value

    def _parseDict(self, peername, pickle_dict):
        """
        Parses the pickle_dict
        Takes measures on the files
        """
        fName = pickle_dict['filename']
        if pickle_dict.has_key('eof'):
            value = self._closeFile(peername, fName)
        elif pickle_dict.has_key('fail'):
            value = self._closeFile(peername, fName, False)
        elif pickle_dict.has_key('line'):
            saveline = pickle_dict['line']
            value = self._saveFile(peername, fName, saveline)
        else:
            return None
        return value

    def status(self):
        """
        gives the status of sending and receiving
        returns a tuple sending(bool)
        """
        return self.sending

    def sendFile(self, fName):
        """
        Sends file to the server
        """
        self.sending = True
        filename = os.path.basename(fName)
        self.sfile = filename
        fileprotocol = FileSender()
        sendfile, startsend = fileprotocol.beginFileTransfer(fName, self.transport, self.transform)
        sendfile.addCallback(self._endTransfer)
        sendfile.addErrback(self._sendingFailed)
        sendfile.addBoth(self._reset)
        startsend.callback(1)

    def _getDict(self):
        """
        Returns a dictionary
        """
        pickle_dict = {}
        pickle_dict['filename'] = self.sfile
        return pickle_dict

    def transform(self, line):
        """
        Transforms a line to be saved in a file
        """
        pickle_dict = self._getDict()
        pickle_dict['line'] = line
        pickle_str = dict_to_pickle(pickle_dict) 
        # prefix, for the protocol as file sender does not use sendString
        prefix = struct.pack(self.structFormat, len(pickle_str))
        pickle_str = prefix + pickle_str
        return pickle_str

    def _endTransfer(self, *args):
        """
        End file transfer
        """
        msg = 'File sent: %s' %(self.sfile)
        log.msg(msg)
        self.chatproto.update('me ' + msg)
        pickle_dict = self._getDict()
        pickle_dict['eof'] = True
        pickle_str = dict_to_pickle(pickle_dict)
        self.sendString(pickle_str)

    def _sendingFailed(self, exc):
        log.msg(exc)
        msg = 'me File Sending failed'
        self.chatproto.update(msg)
        pickle_dict = self._getDict()
        pickle_dict['fail'] = True
        pickle_str = dict_to_pickle(pickle_dict)
        self.sendString(pickle_str)

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
        filename = os.path.basename(fName)
        path = os.path.join(dire, prefix + filename)
        handler = open(path, 'w')
        return handler

    def _saveFile(self, peername, fName, fline):
        """
        Parses the line
        saves the line in the file
        returns the result string
        """
        if not self.rfile.has_key(fName):
            handler = self._initFile(fName)
            self.rfile[fName] = handler
            value = peername + ' Recieving: ' + fName
        elif self.rfile.has_key(fName):
            handler = self.rfile[fName]
            value = None
        else:
            return
        handler.write(fline)
        return value

    def _closeFile(self, peername, fName, status=True):
        """
        safely closes the file
        cleans up rfiles dict
        returns the result
        """
        handler = self.rfile[fName]
        handler.close()
        del self.rfile[fName]
        if status:
            value = peername + ' Recieved: ' + fName
        else:
            value = peername + ' File could not be received: ' + fName
        return value
