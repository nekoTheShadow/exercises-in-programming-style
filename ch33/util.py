import os, sys, tty, termios

def cls():
    os.system('clear')

class GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

getch = GetchUnix()
interactive = True
def get_input():
    global interactive
    if not interactive:
        return True

    while True:
        key = ord(getch())
        if key == 32: # space bar
            return True
        elif key == 27: # ESC
            interactive = False
            return True