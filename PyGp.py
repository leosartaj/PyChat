#!/usr/bin/env python2

##
# PyGp
# https://github.com/leosartaj/PyGp.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

"""
This file initializes the server or the client
"""
import sys, threading, time
import signal # signal handling
from time import asctime
from time import time
from threading import Thread
sys.path.insert(0, '/usr/local/PyGp/system/') # allows importing modules from different directory
import chat, sct, screen, csig

HOST = sys.argv.pop() if len(sys.argv) == 4 else '127.0.0.1'

if sys.argv[1:2] == ['server']:
    ser = sct.server(sys.argv.pop())
    try:
        s = ser.setup(HOST)
    except Exception as e:
        print 'Cannot start server on', HOST # exit if cannot assign address
        sys.exit()
    startTime = time()
    disp = 'Listening at ' + str(s.getsockname()) + '\n' 
    logdata =  10 * '-' + '\n' + asctime() + '\n' + disp # data printed on start
    print logdata
    ser.savefile('log.txt', logdata, 'PyGp_server') # logging new session
    threads = []
    while True:
        threads_copy = threads
        # remove dead threads
        for thread in threads_copy:
            if not thread.isAlive():
                index = threads.index(thread)
                del threads[index]
        try:
            sc, sockname = s.accept()
            # start a new server thread
            thr = Thread(target=chat.server_thread, args=(sc, ser))
            threads.append(thr)
            thr.start() 
        except:
            shutTime = time()
            logdata =  '\nPyGp --> Server Has been shutdown ~ ' + asctime() + ' (running time ~ ' + str((shutTime - startTime) / 3600.0) + ' hrs)\n' 
            ser.savefile('log.txt', logdata, 'PyGp_server')
            print logdata
            for thread in threads:
                thread.join()
            sys.exit()

elif sys.argv[1:2] == ['client']:

    signal.signal(signal.SIGWINCH, csig.sigwinch_handler) # setup sigwinch handler

    # connecting to server
    cli = sct.client(sys.argv.pop())
    try:
        s = cli.connect(HOST, 8001) # connect to server
    except:
        print 'Could Not Connect to Server at', HOST # Exit of connection failed
        sys.exit()
    client = cli.get_clientname()
    port = cli.get(s)
    port_int = int(port)
    name = ' '.join(str(name) for name in s.getsockname())
    # setting up curses
    handle = screen.screenHandler() # initializes the screen handler
    stdscr = handle.setup_screen()
    # Welcome screen
    try:
        handle.welcome(stdscr)
        handle.getch(stdscr)
    except Exception, e: # if cannot start curses
        handle.stop_screen(stdscr)
        cli.close()
        raise(e)
    handle.clear(stdscr)
    handle.refresh(stdscr)
    # Setting up the main window
    cli.height, cli.width = stdscr.getmaxyx()
    height, width = cli.get_height(), cli.get_width()
    handle.info_screen(width, name, port)
    win_recv = handle.new_window(height - 12, width, 6, 0)
    # new client thread for sending
    Thread(target=chat.sendbycli, args=(s, cli, port_int, stdscr, win_recv)).start()
    # new client thread for listening
    Thread(target=chat.recvbycli, args=(s.getsockname()[0], cli, port_int, height, stdscr, win_recv)).start()

else:
    print >>sys.stderr, 'usage: pygp [server|client] [username] [host]'
