#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

"""
Contains helper functions for parsing arguments
"""

import argparse # parsing the options
from getpass import getuser

try:
    from PyChat import __desc__ # try to get version number
except ImportError:
    __desc__ = 'UNKNOWN'

def parse_args():
    """
    Parses the arguments
    """
    parser = argparse.ArgumentParser(description='Asynchronous Chat Client based on Twisted and gtk')

    help = "Current version of PyChat"
    parser.add_argument('--version', '-v',  action='version', help=help, version=__desc__)

    help = "The Interface to bind on."
    parser.add_argument('--iface', help=help, default=None)

    help = "The port to listen/connect on."
    parser.add_argument('--port', '-p', type=int, help=help, default=8001)

    help = "The name of client. Defaults to username."
    parser.add_argument('--client', '-c', type=str, help=help, default=getuser())

    help = "The name of log file. Defaults to pychat.log in cwd."
    parser.add_argument('--log', '-l', help=help, default='pychat.log')

    args = parser.parse_args()

    return args
