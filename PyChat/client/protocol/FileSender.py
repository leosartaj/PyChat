#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

from twisted.protocols import basic
from twisted.internet import defer, interfaces
from zope.interface import implements 

def filterArgs(func):
    """
    Decorator to call only call function with the first argument passed
    """
    def _wrapper(*args, **kwargs):
        func(args[0])
    return _wrapper

class FileSender(object):
    """
    Sends a file
    """
    implements(interfaces.IPushProducer)

    CHUNK_SIZE = 2 ** 14 - 384

    lastSent = ''
    deferred = None
    start, end = None, None

    def beginFileTransfer(self, fName, consumer, transform=None, start=None, end=None):
        """
        Starts file transfer of a file
        """
        self.start = start
        self.end = end
        self.file = open(fName, 'rb')
        if start:
            self.file.seek(start)
        self.consumer = consumer
        self.transform = transform
        self._paused = False
        self.consumer.registerProducer(self, streaming=True) # register for streaming
        self.resume = defer.Deferred()
        self.resume.addCallback(self.resumeProducing)
        self.deferred = defer.Deferred()
        return (self.deferred, self.resume)

    @filterArgs
    def resumeProducing(self):
        """
        Sends a chunk to the server
        """
        self._paused = False
        chunk = ''
        if self.file:
            #chunk = self.file.read(self.CHUNK_SIZE)
            chunk = self.readChunk()
        if not chunk:
            self._cleanup()
            self._complete()
            return
        if self.transform: # if transform function is defined
            chunk = self.transform(chunk)
        self.consumer.write(chunk)
        self.lastSent = chunk[-1:]
        if not self._paused:
            self.resume.addCallback(self.resumeProducing)

    def readChunk(self):
        """
        Reads the chunk from a file
        """
        size = self.CHUNK_SIZE
        if self.start == None or self.end == None:
            chunk = self.file.read(size)
            return chunk
        limit = self.end - self.start
        if limit <= 0:
            return ''
        if size <= limit:
            chunk = self.file.read(size)
        else:
            chunk = self.file.read(limit)
        self.start += size
        return chunk

    def _cleanup(self):
        """
        Cleans up everything
        """
        if self.file:
            self.file.close()
            self.file = None
        self.consumer.unregisterProducer()

    def _complete(self):
        """
        Completes the file transfer process
        """
        if self.deferred:
            deferred, self.deferred = self.deferred, None
            deferred.callback(self.lastSent)

    def pauseProducing(self):
        self._paused = True

    def stopProducing(self):
        self._cleanup()
        if self.deferred:
            self.deferred.errback(Exception("File transfer stopped"))
            self.deferred = None
