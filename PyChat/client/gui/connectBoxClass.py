#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##


# for GUI
import gtk

# other imports
from helper import helperFunc as hf
from server import start_server
from error import __servfail__

class connectBoxClass:
    """ 
    Sets up Connect Box
    """
    def __init__(self, parent):

        self.parent = parent # save the parent caller

        self.builder = hf.load_interface(__file__, 'glade/connectBox.glade') # load the interface
        self.save_objects() # save objects
        self.builder.connect_signals(self.setup_signals()) # setup signals

        hf.center(self.window, self.parent.window) # center the window to the center of the parent

        self.window.show_all() # display widgets

        self.entry.grab_focus()

    def setup_signals(self):
        """
        Sets up the signals
        """
        sig = { 'on_mainwindow_destroy': self.close
              , 'on_entry_activate'    : self.connect
              , 'on_spinbutton_activate': self.connect
              , 'on_connect_clicked'   : self.connect
              , 'on_cancel_clicked'    : self.close }

        return sig

    def save_objects(self):
        """
        Get the required objects
        """
        self.window = self.builder.get_object('mainwindow')
        self.entry = self.builder.get_object('entry')
        self.spinbutton = self.builder.get_object('spinbutton')
        self.check = self.builder.get_object('checkbutton')

    def connect(self, button):
        """
        Handles when connect button is clicked
        """
        entry = self.entry
        buf = entry.get_buffer()
        host = buf.get_text()
        if not host or not hf.validate_host(host):
            entry.grab_focus()
            return
        spin = self.spinbutton
        buf_spin = spin.get_buffer()
        port = buf_spin.get_text()
        if not port:
            spin.grab_focus()
            return
        port = int(port)
        
        obj = self.parent.get_clientobj()
        result, factory = True, None
        if self.check.get_active():
            result, lisport, factory = start_server.listen(host, port)

        if result: # if everything goes well
            if factory: # also starts a server
                obj.set_factory(lisport, factory)
            self.parent.connect(host, port, obj) # try to connect
        else: # incase server couldnt get started
            obj.updateView('server', __servfail__)

        self.close() # close the window

    def close(self, *args):
        """
        Handles Destroy Event
        """
        self.window.destroy()
