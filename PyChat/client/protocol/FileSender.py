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
from zope.interface import implements, implementer

def filterArgs(func):
    """
    Decorator to call only call function with the first argument passed
    """
    def _wrapper(*args, **kwargs):
        func(args[0])
    return _wrapper

class FileSender(object):
    implements(interfaces.IPushProducer)

    CHUNK_SIZE = 2 ** 14

    lastSent = ''
    deferred = None

    def beginFileTransfer(self, file, consumer, transform=None):
        self.file = file
        self.consumer = consumer
        self.transform = transform

        self._paused = False
        self.consumer.registerProducer(self, streaming=True)
        self.resume = defer.Deferred()
        self.resume.addCallback(self.resumeProducing)
        self.deferred = defer.Deferred()
        return self.deferred, self.resume

    @filterArgs
    def resumeProducing(self):
        self._paused = False
        chunk = ''
        if self.file:
            chunk = self.file.read(self.CHUNK_SIZE)
        if not chunk:
            #print 'done'
            self._complete()
            return
        if self.transform:
            chunk = self.transform(chunk)
        self.consumer.write(chunk)
        self.lastSent = chunk[-1:]
        if not self._paused:
            self.resume.addCallback(self.resumeProducing)
        #print 'sent'

    def _complete(self):
        self.file = None
        self.consumer.unregisterProducer()
        if self.deferred:
            self.deferred.callback(self.lastSent)
            self.deferred = None

    def pauseProducing(self):
        #print 'paused'
        self._paused = True

    def stopProducing(self):
        if self.deferred:
            self.deferred.errback(Exception("File transfer stopped"))
            self.deferred = None
