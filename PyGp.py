#!/usr/bin/env python2

import chat, sys, threading, curses

HOST = sys.argv.pop() if len(sys.argv) == 4 else '127.0.0.1'

if sys.argv[1:2] == ['server']:
    ser = chat.server(sys.argv.pop())
    s = ser.setup(HOST)
    print 'Listening at', s.getsockname()
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
            thr = threading.Thread(target=chat.server_thread, args=(sc, ser))
            threads.append(thr)
            thr.start()
        except:
            print '\nPyGp --> Server Has been shutdown'
            for thread in threads:
                thread.join()
            sys.exit()

elif sys.argv[1:2] == ['client']:
    stdscr = chat.setup_screen()
    cli = chat.client(sys.argv.pop())
    s = cli.connect(HOST, 8001)
    client = cli.get_clientname()
    port = cli.get_port()
    #print 'You have been assigned socket name', s.getsockname()
    #print 'listening on port', port[0]
    #print 'Press Ctrl+d to exit'
    name = ' '.join(str(name) for name in s.getsockname())
    height, width = stdscr.getmaxyx()
    win = curses.newwin(height / 4, width, 0, 0)
    win.addstr('You have been assigned socket ' + name + '\n', curses.A_BOLD)
    win.addstr('listening on port ' + port[1] + '\n', curses.A_BOLD)
    win.addstr('Press ctrl+d to exit\n', curses.A_BOLD)
    win.refresh()
    # new client threads for listening and sending
    threading.Thread(target=chat.sendbycli, args=(s, cli, port[1], stdscr)).start()
    threading.Thread(target=chat.recvbycli, args=(HOST, cli, port[0], stdscr)).start()

else:
    print >>sys.stderr, 'usage: ./ChatCli.py server|client [username] [host]'
