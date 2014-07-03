import struct, socket
from random import randint

class transmission(object):
    """
    handles the transmission
    """
    def __init__(self):
            self.si = struct.Struct('!I')

    def listen(self, host, port):
        """
        sets up a socket for listening incoming connections
        """
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sc.bind((host, port))
        sc.listen(128)
        return sc

    def recv_all(self, sock, length):
        """
        recieves the message until
        the given length is
        recieved
        """
        data = ''
        while len(data) < length:
            more = sock.recv(length - len(data))
            if not more:
                raise EOFError('socket closed %d bytes into a %d-byte message' % (len(data), length))
            data += more
        return data

    def get(self, sock):
        """
        decides the length
        of the message
        """
        lendata = self.recv_all(sock, self.si.size)
        (length,) = self.si.unpack(lendata)
        return self.recv_all(sock, length)

    def put(self, sock, message):
        """
        adds message length 
        and sends to the server
        """
        sock.send(self.si.pack(len(message)) + message.encode('utf-8'))

class server(transmission):
    """
    implements the server
    """
    def __init__(self, hostname):
        super(server, self).__init__()
        self.port = 8001
        self.ports = []
        self.hostname = hostname
        self.list_cli = []

    def setup(self, host):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host, self.port))
        self.s.listen(128)
        self.host = host
        return self.s

    def relay_msg(self, port, client, message):
        """
        sends message to multiple clients
        """
        for cli in self.get_clients():
            if cli[1] != port:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((cli[2], int(cli[1])))
                self.put(s, client)
                self.put(s, message)
                s.close()

    def get_clients(self):
        return self.list_cli

    def get_hostname(self):
        return self.hostname

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def gen_port(self):
        # generates random port for a client
        random_port = randint(9000, 60000)
        while random_port in self.ports:
            random_port = randint(9000, 60000)
        self.ports.append(random_port)
        return str(random_port)

    def close(self):
        self.s.close()

class client(transmission):
    """
    Sets up a basic client
    """
    def __init__(self, clientname):
        super(client, self).__init__()
        self.clientname = clientname
        self.ports = []
        self.width = 0
        self.height = 0
        # number of lines written or recieved by client
        self.lines = 0

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

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_lines(self):
        return self.lines

    def shutdown(self, cliadd, port):
        """
        helps to shutdown recieve client thread safely
        """
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.connect((cliadd, port))
        camd = 'ser:dis' + self.get_clientname()
        self.put(sc, camd)
        sc.close()
        self.close()

    def close(self):
        self.s.close()
