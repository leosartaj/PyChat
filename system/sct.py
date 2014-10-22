##
# PyGp
# https://github.com/leosartaj/PyGp.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

"""
handles the transmission, server and client
"""
import struct, socket
import os # for file management
from random import randint

class transmission(object):
    """
    handles the transmission
    """
    def __init__(self):
            self.si = struct.Struct('!I')

    def systemHostname(self):
        """
        returns the system hostname
        """
        return socket.gethostname()

    def listen(self, host, port):
        """
        sets up a socket for listening incoming connections
        """
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sc.bind((host, port))
        sc.listen(128)
        return sc

    def connect_sock(self, host, port):
        """
        connects to socket
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        return s

    def _recv_all(self, sock, length):
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
        lendata = self._recv_all(sock, self.si.size)
        (length,) = self.si.unpack(lendata)
        return self._recv_all(sock, length)

    def put(self, sock, message):
        """
        adds message length 
        and sends
        """
        sock.send(self.si.pack(len(message)) + message)

    def fcode(self, name):
        """
        prepares a file for sending
        """
        try:
            directory = os.path.dirname(name) # returns the directory name
            fname = os.path.basename(name) # returns the filename
            f = open(os.path.join(directory, fname))
            send = ''
            for line in f:
                send += line
        except:
            send = 'ser:error'
        return send

    def savefile(self, name, fdata, directory = '', prefix = 'PyGp', root = '/usr/local/PyGp/'):
        """
        saves a file 
        suffixes PyGp_  and a counter to the name
        """
        try:
            fname = os.path.basename(name)
            new = prefix + '_' + fname
            save = root + directory
            f = open(os.path.join(save, new), 'a')
            f.write(fdata)
            f.close()
        except:
            return 'Cannot save file'

        return 'recieved file -> ' + new

class server(transmission):
    """
    implements the server
    inherits from transmission
    """
    def __init__(self, hostname, port):
        """
        initializes various important variables
        """
        super(server, self).__init__()
        self.port = port
        self._ports = []
        self.hostname = hostname
        self.list_cli = []

    def setup(self, host):
        """
        sets up a listening socket
        """
        self.s = self.listen(host, self.port)
        self.host = host
        return self.s

    def relay_msg(self, port, client, message):
        """
        sends message to multiple clients
        """
        for cli in self.get_clients():
            if cli[1] != port:
                s = self.connect_sock(cli[2], int(cli[1]))
                self.put(s, client)
                self.put(s, message)
                s.close()

    def relay_file(self, port, client, message, fdata):
        """
        sends file data to multiple clients
        """
        for cli in self.get_clients():
            if cli[1] != port:
                s = self.connect_sock(cli[2], int(cli[1]))
                self.put(s, client)
                self.put(s, message)
                self.put(s, fdata)
                s.close()

    def add(self, client, port, cliadd):
        """
        adds a client entry
        """
        self.list_cli.append((client, port, cliadd))

    def remove(self, client, port, cliadd):
        """
        removes a client entry
        """
        index = self.list_cli.index((client, port, cliadd))
        del self.list_cli[index]

    def get_clients(self):
        return self.list_cli

    def get_hostname(self):
        return self.hostname

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def gen_port(self):
        """
        generates random port for a client
        """
        random_port = randint(9000, 60000)
        while random_port in self._ports:
            random_port = randint(9000, 60000)
        self._ports.append(random_port)
        return str(random_port)

    def close(self):
        """
        closes the socket
        """
        self.s.close()

class client(transmission):
    """
    Sets up a basic client
    inherits from transmission
    """
    def __init__(self, clientname):
        """
        initializes various important variables
        """
        super(client, self).__init__()
        self.clientname = clientname
        self.ports = []
        self.width = 0
        self.height = 0
        # number of lines written or recieved by client
        self.lines = 0

    def connect(self, host, port):
        """
        connects to the server socket
        """
        self.host = host
        self.port = port
        self.s = self.connect_sock(self.host, self.port)
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
        sc = self.connect_sock(cliadd, port)
        camd = 'ser:dis' + self.get_clientname()
        self.put(sc, camd)
        sc.close()
        self.close()

    def close(self):
        """
        closes the socket
        """
        self.s.close()
