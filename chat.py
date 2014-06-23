import socket, struct

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

def run_thread(sc, ser):
    print 'We have accepted a connection from', sc.getpeername()
    print 'Socket connects', sc.getsockname(), 'and', sc.getpeername()
    name = ser.get_hostname()
    info = sc.getsockname()
    client = get(sc)
    port = get(sc)
    ser.list_cli.append((client, port))
    while True:
        message = get(sc)
        for cli in ser.get_clients():
            if cli[0] != client:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((info[0], int(cli[1])))
                put(s, client)
                put(s, message)
                s.close()
        print client, '>>>', repr(message)
    sc.close()

def sendbycli(s, cli, port):
    client = cli.get_clientname()
    put(s, client)
    put(s, port)
    while True:
        send = raw_input(client + ' >>> ')
        put(s, send)
        if(send == 'leobye'):
            break
    cli.close()

def recvbycli(host, cli, port):
    sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sc.bind((host, port))
    sc.listen(128)
    while True:
        s, sockname = sc.accept()
        client = get(s)
        message = get(s)
        print '\n', client, '>>>', message, '<<<'
        s.close()

class server:
    def __init__(self, hostname):
        self.port = 8001
        self.hostname = hostname
        self.list_cli = []
        self.ids = 6968

    def setup(self, host):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host, self.port))
        self.s.listen(128)
        return self.s

    def get_newid(self):
        self.ids += 1
        return self.ids

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
        self.ports = 9000
        self.num = 0

    def connect(self, host, port):
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))
        return self.s

    def get_port(self):
        self.ports += 1
        return self.ports

    def get_clientname(self):
        return self.clientname

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def get_ip(self):
        self.num += 1
        return '192.168.0.' + str(self.num)

    def close(self):
        self.s.close()
