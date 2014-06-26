#!/usr/bin/env python2

import chat, sys, threading, screen

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
    stdscr = screen.setup_screen()
    cli = chat.client(sys.argv.pop())
    s = cli.connect(HOST, 8001)
    client = cli.get_clientname()
    port = cli.get_port()
    name = ' '.join(str(name) for name in s.getsockname())
    cli.height, cli.width = stdscr.getmaxyx()
    height, width = cli.get_height(), cli.get_width()
    screen.info_screen(width, name, port[1])
    # new client threads for listening and sending
    win_recv = screen.new_window(height - 12, width, 6, 0)
    threading.Thread(target=chat.sendbycli, args=(s, cli, port[1], stdscr, win_recv)).start()
    threading.Thread(target=chat.recvbycli, args=(HOST, cli, port[0], height, win_recv)).start()

else:
    print >>sys.stderr, 'usage: ./ChatCli.py server|client [username] [host]'
