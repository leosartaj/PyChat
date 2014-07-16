##
# PyGp
# https://github.com/leosartaj/PyGp.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

"""
using the curses module provides the useful methods for managing the display
"""
import curses, time

class screenHandler():
    """
    provides useful methods for handling screen
    """
    def setup_screen(self):
        """
        initializes curses screen
        """
        stdscr = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        stdscr.keypad(1)
        return stdscr

    def new_window(self, height, width, y, x):
        """
        makes a new 
        curses window
        """
        win = curses.newwin(height, width, y, x)
        return win

    def info_screen(self, width, name, port):
        """
        updates the general
        info tab
        """
        win = curses.newwin(5, width, 0, 0)
        win.addstr('\n You have been assigned ' + name + '\n')
        win.addstr(' listening on ' + port + '\n')
        win.addstr(' Press ctrl+d to exit')
        self.border(win)
        win.refresh()
        
    def border(self, win):
        """
        makes the border
        """
        win.border('|', '|', '-', '-', '+','+', '+', '+')

    def backspace(self, win, width):
        """
        displays the backspace functionality
        takes care of the changes
        in border
        """
        y, x = win.getyx()
        win.delch(y, x - 1)
        win.addstr(y, width - 2, ' |')
        win.move(y, x - 1)
        win.refresh()

    def addstr(self, win, message, attr = None):
        """
        adds a string
        """
        if attr == None:
            win.addstr(message)
        elif attr == 'bold':
            win.addstr(message, curses.A_BOLD)

    def getch(self, win):
        """
        returns an inputted character
        """
        key = win.getch()
        return key

    def refresh(self, win):
        """
        refreshes the screen
        """
        win.refresh()

    def clear(self, win):
        """
        clears the screen
        """
        win.clear()

    def overflow_recv(self, win_recv, keyHandle, height, limit):
        """
        checks overflow
        """
        if keyHandle.get_lines() == height - limit:
            keyHandle.lines -= 1
            y, x = win_recv.getyx()
            win_recv.move(1, 0)
            win_recv.deleteln()
            win_recv.move(y - 1, x)
            win_recv.refresh()
                
    def timestamp(self):
        """
        gives a formatted timestamp
        """
        localtime = time.localtime(time.time())
        timer = ' ~ ' + str(localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5])
        return timer

    def uprecv_win(self, win_recv, client, message):
        """
        updates the recieve 
        window
        """
        win_recv.addstr('\n| ' + client, curses.A_BOLD)
        win_recv.addstr(self.timestamp(), curses.A_DIM)
        win_recv.addstr(' >>> ', curses.A_BOLD)
        win_recv.addstr(message)
        win_recv.refresh()

    def stop_screen(self, stdscr):
        """
        stops the curses screen mode safely
        """
        curses.echo()
        curses.nocbreak()
        stdscr.keypad(0)
        curses.curs_set(1)
        curses.endwin()

class keyHandler(screenHandler):
    """
    handles the key operations
    and the message to be sent
    """
    def __init__(self, win, width):
        self.send = ''
        self.leng = 0
        self.lines = 0
        self.win = win
        self.width = width
        self.stack = []

    def get_key(self):
        """
        key input
        """
        key = chr(self.getch(self.win))
        return key

    def keyOperation(self, key):
        """
        Operation to be performed for specific keys
        """
        if key == '\x7f':
            self._backspace() # handle backspace
        elif key == '[A' or key =='\x1b':
            self._last()
        elif key == '\n':
            self._newline(key) # handle newline character
            return True
        else:
            self._display(key) # handle other keys
        self.refresh(self.win)
        return False

    def _last(self):
        """
        provides the linux like upper key functionality
        """
        leng = len(self.stack)
        if leng == 0:
            return
        self.send = ''
        self.addstr(self.win, self.send)
        self.send = self.stack[leng - 1]
        self.addstr(self.win, self.send)

    def _display(self, key):
        """
        handles the keys to be displayed
        """
        if self.leng != (self.width - 12):
            self.addstr(self.win, key)
            self.send += key
            self.leng += 1

    def _newline(self, key):
        """
        handles the newline character
        """
        if self.send == '':
            return
        self.addstr(self.win, key)
        # increase the number of lines written
        self.lines += 1
        self._push(self.send) # push on the stack

    def _backspace(self):
        """
        provides the backspace functionality
        """
        if self.send == '':
            return
        self.send = self.send[:-1]
        self.leng -= 1
        self.backspace(self.win, self.width)

    def _push(self, msg):
        """ 
        pushes on the stack
        """
        self.stack.append(msg)

    def reset(self):
        """
        rests the message
        """
        self.send = ''
        self.leng = 0

    def get_lines(self):
        return self.lines

    def get_message(self):
        return self.send

    def get_win(self):
        return self.win

    def get_width(self):
        return self.width
