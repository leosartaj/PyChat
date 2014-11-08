#!/usr/bin/env python2

##
# PyGp
# https://github.com/leosartaj/PyGp.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

# For the GUI
from gtk import Builder
from signals import clientGUISignals

class clientGUIClass:
    """ 
    Sets up the GUI interface
    """
    def __init__(self, fName):
        builder = Builder()
        builder.add_from_file(fName)
        builder.connect_signals(clientGUISignals())
        window = builder.get_object('MainWindow')
        window.show_all()
