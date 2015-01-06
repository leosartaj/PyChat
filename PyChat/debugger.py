#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

"""
Development script
To run without actually installing
Picks up local changes
"""

# system imports
import sys

# twisted imports
from twisted.internet import gtk2reactor
gtk2reactor.install() # install reactor for gui
from twisted.internet import reactor

# Other imports
import main
from client import options

if __name__ == '__main__':
    args = options.parse_args() # parse the arguments

    addresses = []
    client = args.client
    host, port, server = args.iface, args.port, args.server
    if host != None:
        addresses.append((host, port, server))
    try:
        main.run(client, sys.stdout, addresses)
    except Exception, e:
        print 'Cannot Start PyChat'
        print e
        sys.exit(1)

    reactor.run()
