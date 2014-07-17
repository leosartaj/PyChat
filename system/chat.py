##
# PyGp
# https://github.com/leosartaj/PyGp.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

"""
runs PyGp on the terminal
"""
import screen

def server_thread(sc, ser):
    """
    New server thread created
    when connected to a client
    """
    info = sc.getsockname()
    port = ser.gen_port()
    ser.put(sc, port)
    client = ser.get(sc)
    cliadd = sc.getpeername()[0]
    list_clients = ', '.join(str(cli[0]) for cli in ser.get_clients())
    ser.put(sc, list_clients)
    ser.add(client, port, cliadd)
    conn = 'Connected server ' + str(info) + ' and ' + client + ' ' + str(sc.getpeername()) + ' listening on ' + port
    clientlist = 'Clients ' + str(ser.get_clients())
    logdata = conn + '\n' + clientlist + '\n'
    print conn
    print clientlist
    ser.savefile('log.txt', logdata, 'PyGp_server') # saves server data
    ser.relay_msg(port, client, 'has connected')
    while True:
        try:
            message = ser.get(sc)
        except EOFError:
            disconnect =  '>>> ' + client + ' has been disconnected >>> ' + str(sc.getpeername())
            ser.savefile('log.txt', disconnect, 'PyGp_server') # saves server data
            print disconnect
            ser.relay_msg(port, client, 'has been disconnected')
            sc.close()
            ser.remove(client, port, cliadd)
            return
        if message[:5] == 'file:':
            msg = 'Sending file -> ' + message[5:]
            fdata = ser.get(sc)
            if fdata != 'ser:error':
                print client, port, '>>>', repr(msg)
                ser.relay_file(port, client, message, fdata) # sends files
            else:
                print client, port, '>>>', repr(msg), fdata
        else:
            print client, port, '>>>', repr(message)
            ser.relay_msg(port, client, message) # sends messages
        logdata = client + ' ' + port + ' ' + message + '\n'
        ser.savefile('log.txt', logdata, 'PyGp_server')

def sendbycli(s, cli, port, stdscr, win_recv):
    """
    Sends the messages
    to the server
    """
    client = cli.get_clientname()
    host = s.getsockname()[0]
    cli.put(s, client)
    active = cli.get(s)
    # setting up window
    handle = screen.screenHandler() # initialiizes the screen handler
    height, width = cli.get_height(), cli.get_width()
    win = handle.new_window(5, width, height - 5, 0)
    handle.addstr(win, '\n')
    handle.border(win)
    handle.refresh(win)
    if len(active) != 0:
        handle.addstr(win, '  Active users --> ' + active + '\n')
    prev = ''
    keyHandle = screen.keyHandler(win, width) # handles inputting
    while True:
        if prev != '':
            handle.addstr(win, '  Sent >>> ' + prev + '\n')
        handle.addstr(win, '  Me >>> ', 'bold')
        handle.border(win)
        handle.refresh(win)
        keyHandle.reset()
        while True:
            key = keyHandle.get_key() # inputted character
            if key == '\x04': # shutting down when ctrl+d pressed
                cli.shutdown(s.getsockname()[0], port)
                handle.stop_screen(stdscr)
                print 'Thank you for using PyGp'
                print 'Contribute --> https://github.com/leosartaj/PyGp'
                return
            if keyHandle.keyOperation(key): # Handle different keys
                break
        handle.clear(win)
        handle.addstr(win, '\n')
        send = keyHandle.get_message() # return the message
        # update the recv win
        handle.uprecv_win(win_recv, 'Me', send)
        # handle overflow
        handle.overflow_recv(win_recv, keyHandle, height, 13)
        prev = send
        if send[:5] == 'file:': # handle if file is sent
            cli.put(s, send)
            send = cli.fcode(send[5:])
        cli.put(s, send)

def recvbycli(host, cli, port, height, win_recv):
    """
    listens on an assigned port
    for messages from other
    clients
    """
    clientname = cli.get_clientname()
    handle = screen.screenHandler() # initialiizes the screen handler
    # begin listening
    sc = cli.listen(host, port)
    while True:
        s, sockname = sc.accept()
        client = cli.get(s)
        if client == 'ser:dis' + clientname:
            s.close()
            sc.close()
            return
        message = cli.get(s)
        if message[:5] == 'file:': # checks if incoming message is a file
            message = cli.savefile(message[5:], cli.get(s), 'PyGp_recv') # saves the file on the disk
        cli.lines += 1
        handle.uprecv_win(win_recv, client, message)
        handle.overflow_recv(win_recv, cli, height, 13)
        s.close()
