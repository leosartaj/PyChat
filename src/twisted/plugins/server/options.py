#!/usr/bin/env python2

##
# PyGp
# https://github.com/leosartaj/PyGp.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

from twisted.python.usage import Options

class Options(Options):
    """
    user defined options
    """
    optParameters = [
        ['port', 'p', 8001, 'The port number to listen on.'],
        ['iface', 'i', 'localhost', 'The interface to listen on.'],
        ]
