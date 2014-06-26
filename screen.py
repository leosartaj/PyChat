import curses, time

def setup_screen():
    stdscr = curses.initscr()
    curses.start_color()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.keypad(1)
    return stdscr

def draw_line(stdscr, width):
    header = '+' + (width - 2) * '-' + '+'
    stdscr.addstr(header)

def new_window(height, width, y, x):
    win = curses.newwin(height, width, y, x)
    return win

def info_screen(width, name, port):
    win = curses.newwin(5, width, 0, 0)
    win.addstr('\n You have been assigned ' + name + '\n')
    win.addstr(' listening on ' + port + '\n')
    win.addstr(' Press ctrl+d to exit')
    win.border('|', '|', '-', '-', '+','+', '+', '+') 
    win.refresh()
    
def overflow_recv(win_recv, cli, height):
    if cli.get_lines() == height - 13:
        cli.lines -= 1
        y, x = win_recv.getyx()
        win_recv.move(1, 0)
        win_recv.deleteln()
        win_recv.move(y - 1, x)
        win_recv.refresh()
            
def timestamp():
    localtime = time.localtime(time.time())
    timer = ' ~ ' + str(localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5])
    return timer

def uprecv_win(win_recv, client, message):
        win_recv.addstr('\n| ' + client, curses.A_BOLD)
        win_recv.addstr(timestamp(), curses.A_DIM)
        win_recv.addstr(' >>> ', curses.A_BOLD)
        win_recv.addstr(message)
        win_recv.refresh()

def stop_screen(stdscr):
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(0)
    curses.curs_set(1)
    curses.endwin()

