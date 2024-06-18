# sankalp/cli.py

import curses
import webbrowser
import pygame
import pkg_resources
import time

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

marquee_text = "Welcome to Sankalp's CLI! Stay tuned for more updates... "
marquee_pos = 0


def play_music():
    pygame.mixer.init()
    # Use pkg_resources to get the path to the music file within the package
    music_file = pkg_resources.resource_filename(__name__, "blue.mp3")
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1)


def print_menu(stdscr, selected_row_idx, marquee_pos):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    # Print the marquee text
    marquee_display = marquee_text[marquee_pos:] + marquee_text[:marquee_pos]
    stdscr.attron(curses.color_pair(2))
    stdscr.attron(curses.A_BOLD)
    stdscr.addstr(0, 0, marquee_display[:w])
    stdscr.attroff(curses.A_BOLD)
    stdscr.attroff(curses.color_pair(2))


    for idx, row in enumerate(menu_items):
        # x = w//4 - len(row)//2
        x = w // 3
        y = h//2 - len(menu_items)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    current_row = 0
    marquee_pos = 0

    print_menu(stdscr, current_row, marquee_pos)

    while True:
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_items) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if menu_items[current_row] == "exit":
                pygame.mixer.music.stop()  # Stop the music on exit
                break
            if links[current_row]:
                webbrowser.open(links[current_row])
                
        marquee_pos = (marquee_pos + 1) % len(marquee_text)
        print_menu(stdscr, current_row, marquee_pos)
        time.sleep(0.1)  # Control the speed of the marquee

def run_cli():
    play_music()
    curses.wrapper(main)

if __name__ == "__main__":
    run_cli()