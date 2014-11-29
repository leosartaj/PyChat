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

def add_page(notebook, child, label=None, position=-1):
    """
    Adds a new page with the child
    in a notebook
    can add page to any given position
    by default appends the page
    """
    if position != -1:
        pages = notebook.get_n_pages()
        notebook.insert_page(child, label, position)
    else:
        notebook.append_page(child, label)
    notebook.set_current_page(position) # focus on the new page
    
def remove_page(notebook, child):
    """
    finds the page number and deletes the page
    """
    pagenum = notebook.page_num(child)
    notebook.remove_page(pagenum)
