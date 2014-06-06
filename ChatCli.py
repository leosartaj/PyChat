#!/usr/bin/env python2
# Foundations of Python Network Programming - Chapter 3 - 
# Simple TCP client and server that send and receive 16 octets

import socket, sys, struct

si = struct.Struct('!I')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = sys.argv.pop() if len(sys.argv) == 3 else '127.0.0.1'
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

if sys.argv[1:] == ['server']:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    print 'Listening at', s.getsockname()
    sc, sockname = s.accept()
    print 'We have accepted a connection from', sockname 
    print 'Socket connects', sc.getsockname(), 'and', sc.getpeername()
    while True:
        message = get(sc)
        if(message == 'leobye'):
            break
        print 'The incoming message says', repr(message)
        send = raw_input('>>> ')
        put(sc, send)
        if(send == 'leobye'):
            break
    sc.close()
    s.close()

elif sys.argv[1:] == ['client']:
    s.connect((HOST, PORT))
    print 'Client has been assigned socket name', s.getsockname()
    while True:
        send = raw_input('>>> ')
        put(s, send)
        if(send == 'leobye'):
            break
        reply = get(s)
        if(reply == 'leobye'):
            break
        print 'The server said', repr(reply)
    s.close()

else:
    print >>sys.stderr, 'usage: tcp_local.py server|client [host]'
