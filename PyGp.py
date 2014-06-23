#!/usr/bin/env python2
# Foundations of Python Network Programming - Chapter 3 - 
# Simple TCP client and server that send and receive 16 octets

import chat, sys

HOST = sys.argv.pop() if len(sys.argv) == 4 else '127.0.0.1'

if sys.argv[1:2] == ['server']:
    ser = chat.server(sys.argv.pop())
    s = ser.setup(HOST)
    print 'Listening at', s.getsockname()
    sc, sockname = s.accept()
    print 'We have accepted a connection from', sockname 
    print 'Socket connects', sc.getsockname(), 'and', sc.getpeername()
    server = ser.get_hostname()
    chat.put(sc, server)
    client = chat.get(sc)
    while True:
        message = chat.get(sc)
        if(message == 'leobye'):
            break
        print client, '>>>', repr(message)
        send = raw_input(server + ' >>> ')
        chat.put(sc, send)
        if(send == 'leobye'):
            break
    sc.close()
    ser.close()

elif sys.argv[1:2] == ['client']:
    cli = chat.client(sys.argv.pop())
    s = cli.connect(HOST, 8001)
    print 'Client has been assigned socket name', s.getsockname()
    client = cli.get_clientname()
    server = chat.get(s)
    chat.put(s, client)
    while True:
        send = raw_input(client + ' >>> ')
        chat.put(s, send)
        if(send == 'leobye'):
            break
        reply = chat.get(s)
        if(reply == 'leobye'):
            break
        print server, '>>>', repr(reply)
    cli.close()

else:
    print >>sys.stderr, 'usage: ./ChatCli.py server|client [username] [host]'
