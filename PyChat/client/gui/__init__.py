#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

import sys
from os.path import realpath, dirname

sys.path.append(dirname(realpath(__file__)) + '/..')
import error # access to error module

sys.path.append(dirname(realpath(__file__)) + '/../..')
import server # access to server package
