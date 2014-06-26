import curses, time

def setup_screen():
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

def new_window(height, width, y, x):
    """
    makes a new 
    curses window
    """
    win = curses.newwin(height, width, y, x)
    return win

def info_screen(width, name, port):
    """
    updates the general
    info tab
    """
    win = curses.newwin(5, width, 0, 0)
    win.addstr('\n You have been assigned ' + name + '\n')
    win.addstr(' listening on ' + port + '\n')
    win.addstr(' Press ctrl+d to exit')
    border(win)
    win.refresh()
    
def border(win):
    """
    makes the border
    """
    win.border('|', '|', '-', '-', '+','+', '+', '+')

def backspace(win, width):
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

def addstr(win, message, attr = None):
    """
    adds a string
    """
    if attr == None:
        win.addstr(message)
    elif attr == 'bold':
        win.addstr(message, curses.A_BOLD)

def getch(win):
    """
    returns an inputted character
    """
    return win.getch()

def refresh(win):
    """
    refreshes the screen
    """
    win.refresh()

def clear(win):
    """
    clears the screen
    """
    win.clear()

def overflow_recv(win_recv, cli, height, limit):
    """
    checks overflow
    """
    if cli.get_lines() == height - limit:
        cli.lines -= 1
        y, x = win_recv.getyx()
        win_recv.move(1, 0)
        win_recv.deleteln()
        win_recv.move(y - 1, x)
        win_recv.refresh()
            
def timestamp():
    """
    gives a formatted timestamp
    """
    localtime = time.localtime(time.time())
    timer = ' ~ ' + str(localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5])
    return timer

def uprecv_win(win_recv, client, message):
    """
    updates the recieve 
    window
    """
    win_recv.addstr('\n| ' + client, curses.A_BOLD)
    win_recv.addstr(timestamp(), curses.A_DIM)
    win_recv.addstr(' >>> ', curses.A_BOLD)
    win_recv.addstr(message)
    win_recv.refresh()

def stop_screen(stdscr):
    """
    stops the curses screen mode safely
    """
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(0)
    curses.curs_set(1)
    curses.endwin()
