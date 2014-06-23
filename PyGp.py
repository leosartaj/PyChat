#!/usr/bin/env python2

import chat, sys, threading
from random import randint

HOST = sys.argv.pop() if len(sys.argv) == 4 else '127.0.0.1'

if sys.argv[1:2] == ['server']:
    ser = chat.server(sys.argv.pop())
    s = ser.setup(HOST)
    print 'Listening at', s.getsockname()
    while True:
        sc, sockname = s.accept()
        threading.Thread(target=chat.run_thread, args=(sc, ser)).start()
    ser.close()

elif sys.argv[1:2] == ['client']:
    cli = chat.client(sys.argv.pop())
    s = cli.connect(HOST, 8001)
    print 'Client has been assigned socket name', s.getsockname()
    port = randint(9000, 10000)
    threading.Thread(target=chat.sendbycli, args=(s, cli, str(port))).start()
    threading.Thread(target=chat.recvbycli, args=(HOST, cli, port)).start()

else:
    print >>sys.stderr, 'usage: ./ChatCli.py server|client [username] [host]'
