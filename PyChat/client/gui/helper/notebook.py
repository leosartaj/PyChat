#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##


"""
Handles functionality of notebook widget
"""

import helperFunc as hf

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

def find_page(notebook, child):
    """
    Find a page based on its child
    """
    pagenum = notebook.page_num(child)
    return pagenum

def add_page(notebook, child, label=None, position=-1):
    """
    Adds a new page with the child
    in a notebook
    can add page to any given position
    by default appends the page
    """
    if position == -1:
        pages = notebook.get_n_pages()
        position = pages - 1
    notebook.insert_page(child, label, position)
    notebook.set_tab_reorderable(child, True) # let the tab be reorderable
    notebook.set_current_page(position) # focus on the new page
    return find_page(notebook, child)
