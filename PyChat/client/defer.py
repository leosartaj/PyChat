#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

"""
Contains the Callbacks and Errbacks
"""

from twisted.internet import reactor
from twisted.python import log

def stop_log(msg):
    """
    Log if connection lost
    """
    log.msg(msg)
    log.msg('Closing Connection')

def stop_reactor(_):
    """
    stop the reactor
    """
    if reactor.running:
        reactor.stop()
