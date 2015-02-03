#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

"""
Sets up the command system
Provides helper functions for commands
"""

# prefixes for commands
SERVER_PREFIX = 's$' 
CLIENT_PREFIX = 'c$'
# separator for command value pairs
SEPARATOR = '~'

def validate(line, prefix=''):
    """
    Validates if the line starts with the prefix
    returns True if success
    or False if fail
    """
    len_prefix = len(prefix)
    if line[0:len_prefix] != prefix:
        return False
    return True

def parse(line, prefix='', sep=SEPARATOR):
    """
    Parses a line
    checks if the line starts with prefix
    if not returns None, line
    removes the prefix + sep
    then divides the line into two parts
    returns cmd, value
    if line cannot be divided again 
    returns None, line
    """
    
    if not validate(line, prefix):
        return None, line
    total_len = len(prefix) + len(sep)
    rem_line = line[total_len:]
    index = rem_line.find(sep)
    if index == -1:
        return None, line
    comd, value = rem_line[:index], rem_line[index + len(sep):]
    return comd, value

def extractFirst(line, sep=SEPARATOR):
    """
    Extracts the first item before a sep
    returns first, rem
    if not possible
    returns None, line
    """
    index = line.find(sep)
    if index == -1:
        return None, line
    first, rem = line[:index], line[index + len(sep):]
    return first, rem

def addFirst(line, add, sep=SEPARATOR):
    """
    Prepends an item followed by a sep
    """
    msg = ''
    if add:
        msg += add + sep
    msg += line
    return msg

def cmd(command, value, prefix='', sep=SEPARATOR):
    """
    Makes a command
    join prefix, command, value
    separated by sep
    """
    msg = prefix + sep + command + sep + value
    return msg

def servercmd(command, value):
    """
    returns command to send to the server
    """
    msg = cmd(command, value, CLIENT_PREFIX, SEPARATOR)
    return msg

def clientcmd(command, value, name=''):
    """
    returns command to send to the client
    """
    msg = cmd(command, value, SERVER_PREFIX, SEPARATOR)
    return msg
