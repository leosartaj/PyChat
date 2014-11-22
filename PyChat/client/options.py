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

import optparse # parsing the options
from getpass import getuser

def parse_args():
    """
    Parses the arguments
    """
    usage = """usage: %prog [host] [options]

    Run 
    pychat -h/--help
    For help
"""
    parser = optparse.OptionParser(usage)

    help = "The port to listen/connect on."
    parser.add_option('--port', '-p', type='int', help=help, default=None)

    help = "The name of client. Defaults to username."
    parser.add_option('--client', '-c', type='str', help=help, default=getuser())

    help = "The name of log file. Defaults to pychat.log in cwd."
    parser.add_option('--log', '-l', help=help, default='pychat.log')

    options, args = parser.parse_args()

    if len(args) == 1:
        HOST = args[0]
    elif len(args) == 0:
        HOST = None
    else:
        parser.error('Invalid number of arguments, got ' + str(len(args)) + ' args expecting 0/1')

    return options, HOST
