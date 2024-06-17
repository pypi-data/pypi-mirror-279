# sankalp/cli.py

import curses
import webbrowser

menu_items = [
    "Sankalp Shrivastava",
    "I'm a technologist and an entrepreneur.",
    "Some thoughts here",
    "twitter",
    "github",
    "bento",
    "email: s@sankalp.sh",
    "exit"
]

links = [
    "",
    "",
    "https://sankalp.sh/thoughts.html",
    "https://twitter.com/1sankalp",
    "https://github.com/1Sankalp",
    "https://bento.me/1sankalp",
    "mailto:s@sankalp.sh",
    ""
]

def load_ascii_art(filename):
    with open(filename, 'r') as file:
        return file.readlines()
    
ascii_art = load_ascii_art("me.txt")

def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    for idx, line in enumerate(ascii_art):
        stdscr.addstr(idx, 0, line.strip())

    menu_x = max(len(line) for line in ascii_art) + 2 

    for idx, row in enumerate(menu_items):
        # x = w//4 - len(row)//2
        x = menu_x
        # x = w // 3
        y = h//2 - len(menu_items)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()

def run_cli():
    curses.wrapper(main)

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    current_row = 0

    print_menu(stdscr, current_row)

    while True:
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_items) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if menu_items[current_row] == "exit":
                break
            if links[current_row]:
                webbrowser.open(links[current_row])
        print_menu(stdscr, current_row)

if __name__ == "__main__":
    run_cli()