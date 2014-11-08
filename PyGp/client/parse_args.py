#!/usr/bin/env python2

##
# PyGp
# https://github.com/leosartaj/PyGp.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

import optparse # parsing the options
from getpass import getuser

def parse_args():
    """
    Parses the arguments
    """
    usage = """
"""
    parser = optparse.OptionParser(usage)

    help = "The port to listen/connect on."
    parser.add_option('-p', '--port', type='int', help=help, default=8001)

    help = "The name of client. Defaults to username."
    parser.add_option('-n', '--name', help=help, default=getuser())

    options, args = parser.parse_args()

    if len(args) == 1:
        HOST = args[0]
    elif len(args) == 0:
        HOST = '127.0.0.1'
    else:
        parser.error('Invalid number of arguments, got ' + str(len(args)) + ' args expecting 0/1')

    return options, HOST
