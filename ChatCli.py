#!/usr/bin/env python2
# Foundations of Python Network Programming - Chapter 3 - 
# Simple TCP client and server that send and receive 16 octets

import socket, sys, struct

si = struct.Struct('!I')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = sys.argv.pop() if len(sys.argv) == 4 else '127.0.0.1'
PORT = 1060

def recv_all(sock, length):
    data = ''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('socket closed %d bytes into a %d-byte message' % (len(data), length))
        data += more
    return data

def get(sock):
    lendata = recv_all(sock, si.size)
    (length,) = si.unpack(lendata)
    return recv_all(sock, length)

def put(sock, message):
    sock.send(si.pack(len(message)) + message)

if sys.argv[1:2] == ['server']:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    print 'Listening at', s.getsockname()
    sc, sockname = s.accept()
    print 'We have accepted a connection from', sockname 
    print 'Socket connects', sc.getsockname(), 'and', sc.getpeername()
    server = sys.argv.pop()
    put(sc, server)
    client = get(sc)
    while True:
        message = get(sc)
        if(message == 'leobye'):
            break
        print client, '>>>', repr(message)
        send = raw_input(server + ' >>> ')
        put(sc, send)
        if(send == 'leobye'):
            break
    sc.close()
    s.close()

elif sys.argv[1:2] == ['client']:
    s.connect((HOST, PORT))
    print 'Client has been assigned socket name', s.getsockname()
    client = sys.argv.pop()
    server = get(s)
    put(s, client)
    while True:
        send = raw_input(client + ' >>> ')
        put(s, send)
        if(send == 'leobye'):
            break
        reply = get(s)
        if(reply == 'leobye'):
            break
        print server, '>>>', repr(reply)
    s.close()

else:
    print >>sys.stderr, 'usage: tcp_local.py server|client [host]'
