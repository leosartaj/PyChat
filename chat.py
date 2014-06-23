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
    client = get(sc)
    ser.list_cli.append(ser.get_newid())
    while True:
        message = get(sc)
        if(message == 'leobye'):
            break
        print client, '>>>', repr(message)
    sc.close()

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

    def connect(self, host, port):
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))
        return self.s

    def get_clientname(self):
        return self.clientname

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def close(self):
        self.s.close()
