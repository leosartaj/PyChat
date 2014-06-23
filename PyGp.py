#!/usr/bin/env python2

import chat, sys, threading

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
    client = cli.get_clientname()
    chat.put(s, client)
    while True:
        send = raw_input(client + ' >>> ')
        chat.put(s, send)
        if(send == 'leobye'):
            break
    cli.close()

else:
    print >>sys.stderr, 'usage: ./ChatCli.py server|client [username] [host]'
