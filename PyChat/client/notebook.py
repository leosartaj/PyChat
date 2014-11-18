#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

"""
Handles functionality of notebook widget
"""

def show_tabs(notebook, num=1):
    """
    Shows or hides tabs in a notebook
    if tabs increase over a certain threshold
    tabs become visible
    """
    tabs = notebook.get_n_pages()
    state = notebook.get_show_tabs()

    if tabs > num and not state:
        notebook.set_show_tabs(True)
    elif tabs <= num and state:
        notebook.set_show_tabs(False)
