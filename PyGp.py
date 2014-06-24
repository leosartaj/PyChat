#!/usr/bin/env python2

import chat, sys, threading

HOST = sys.argv.pop() if len(sys.argv) == 4 else '127.0.0.1'

def terminate(signal, frame):
    for thread in threads:
        thread.join()
    sys.exit()

if sys.argv[1:2] == ['server']:
    ser = chat.server(sys.argv.pop())
    s = ser.setup(HOST)
    print 'Listening at', s.getsockname()
    threads = []
    while True:
        threads_copy = threads
        for thread in threads_copy:
            if not thread.isAlive():
                index = threads.index(thread)
                del threads[index]
        try:
            sc, sockname = s.accept()
            thr = threading.Thread(target=chat.server_thread, args=(sc, ser))
            threads.append(thr)
            thr.start()
        except:
            print '\nPyGp --> Server Has been shutdown'
            for thread in threads:
                thread.join()
            sys.exit()

elif sys.argv[1:2] == ['client']:
    cli = chat.client(sys.argv.pop())
    s = cli.connect(HOST, 8001)
    client = cli.get_clientname()
    print 'You has been assigned socket name', s.getsockname()
    port = cli.get_port()
    print 'listening on port', port[0]
    print 'Press Ctrl+d to exit'
    threading.Thread(target=chat.sendbycli, args=(s, cli, port[1])).start()
    threading.Thread(target=chat.recvbycli, args=(HOST, cli, port[0])).start()

else:
    print >>sys.stderr, 'usage: ./ChatCli.py server|client [username] [host]'
