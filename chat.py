##
# PyGp
# https://github.com/leosartaj/PyGp.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

"""
contains the main logic
"""
import sys, screen

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
    print 'Connected server', info, 'and', client, sc.getpeername(), 'listening on', port
    ser.list_cli.append((client, port, cliadd))
    print 'Clients', ser.get_clients()
    ser.relay_msg(port, client, 'has connected')
    while True:
        try:
            message = ser.get(sc)
        except EOFError:
            print '>>>', client, 'has been disconnected >>>', sc.getpeername()
            ser.relay_msg(port, client, 'has been disconnected')
            sc.close()
            index = ser.list_cli.index((client, port, cliadd))
            del ser.list_cli[index]
            return
        ser.relay_msg(port, client, message)
        print client, port, '>>>', repr(message)

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
    height, width = cli.get_height(), cli.get_width()
    win = screen.new_window(5, width, height - 5, 0)
    screen.addstr(win, '\n')
    screen.border(win)
    screen.refresh(win)
    if len(active) != 0:
        screen.addstr(win, '  Active users --> ' + active + '\n')
    prev = ''
    while True:
        key = ''
        send = ''
        leng = 0
        if prev != '':
            screen.addstr(win, '  Sent >>> ' + prev + '\n')
        screen.addstr(win, '  Me >>> ', 'bold')
        screen.border(win)
        screen.refresh(win)
        while True:
            key = win.getch()
            key = chr(key)
            if key == '\x7f':
                if send == '':
                    continue
                send = send[:-1]
                leng -= 1
                screen.backspace(win, width)
            elif key == '\n':
                if send == '':
                    continue
                screen.addstr(win, key)
                cli.lines += 1
                break
            elif key == '\x04':
                # shutting down when ctrl+d pressed
                cliadd = s.getsockname()[0]
                cli.shutdown(cliadd, port)
                screen.stop_screen(stdscr)
                print 'Thank you for using PyGp'
                print 'Contribute --> https://github.com/leosartaj/PyGp'
                return
            else:
                if leng != (width - 12):
                    screen.addstr(win, key)
                    send += key
                    leng += 1
            screen.refresh(win)
        screen.clear(win)
        screen.addstr(win, '\n')
        screen.uprecv_win(win_recv, 'Me', send)
        screen.overflow_recv(win_recv, cli, height, 13)
        prev = send
        cli.put(s, send)


def recvbycli(host, cli, port, height, win_recv):
    """
    listens on an assigned port
    for messages from other
    clients
    """
    clientname = cli.get_clientname()
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
        cli.lines += 1
        screen.uprecv_win(win_recv, client, message)
        screen.overflow_recv(win_recv, cli, height, 13)
        s.close()
