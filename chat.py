import socket, struct
from random import randint

si = struct.Struct('!I')

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
    sock.send(si.pack(len(message)) + message.encode('utf-8'))

def relay_msg(clients, host, port, client, message):
    for cli in clients:
        if cli[1] != port:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, int(cli[1])))
            put(s, client)
            put(s, message)
            s.close

def server_thread(sc, ser):
    info = sc.getsockname()
    client = get(sc)
    port = get(sc)
    list_clients = ' '.join(str(cli[0]) for cli in ser.get_clients())
    put(sc, list_clients)
    print 'Connected server', info, 'and', client, sc.getpeername(), 'listening on', port
    ser.list_cli.append((client, port))
    print 'Clients', ser.get_clients()
    relay_msg(ser.get_clients(), info[0], port, client, 'has connected')
    while True:
        try:
            message = get(sc)
        except EOFError:
            print '>>>', client, 'has been disconnected >>>', sc.getpeername()
            relay_msg(ser.get_clients(), info[0], port, client, 'has been disconnected')
            sc.close()
            index = ser.list_cli.index((client, port))
            del ser.list_cli[index]
            return
        relay_msg(ser.get_clients(), info[0], port, client, message)
        print client, port, '>>>', repr(message)

def sendbycli(s, cli, port):
    client = cli.get_clientname()
    host = s.getsockname()[0]
    put(s, client)
    put(s, port)
    active = get(s)
    if len(active) != 0:
        print 'Active users -->', active 
    while True:
        try:
            send = raw_input('Me >>> ')
        except EOFError:
            print '\nThank you for using PyGp'
            print 'Contribute --> https://github.com/leosartaj/PyGp\n'
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.connect((host, int(port)))
            put(sc, client + '   ')
            sc.close()
            cli.close()
            return
        put(s, send)

def recvbycli(host, cli, port):
    clientname = cli.get_clientname()
    sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sc.bind((host, port))
    sc.listen(128)
    while True:
        s, sockname = sc.accept()
        client = get(s)
        if client == clientname + '   ':
            s.close()
            sc.close()
            return
        message = get(s)
        print '\n', client, '>>>', message, '<<<'
        s.close()

class server:
    def __init__(self, hostname):
        self.port = 8001
        self.hostname = hostname
        self.list_cli = []

    def setup(self, host):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host, self.port))
        self.s.listen(128)
        return self.s

    def get_clients(self):
        return self.list_cli

    def get_hostname(self):
        return self.hostname

    def get_port(self):
        return self.port

    def close(self):
        self.s.close()

class client:
    def __init__(self, clientname):
        self.clientname = clientname
        self.ports = []

    def connect(self, host, port):
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))
        return self.s

    def get_port(self):
        random_port = randint(9000, 60000)
        while random_port in self.ports:
            random_port = randint(9000, 60000)
        self.ports.append(random_port)
        return (random_port, str(random_port))

    def get_clientname(self):
        return self.clientname

    def get_host(self):
        return self.host

    def close(self):
        self.s.close()
