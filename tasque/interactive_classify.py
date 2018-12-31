"""
This module contains an interactive auto-classification procedure.

It is very nice.
"""

import sys
import string
import tty
import termios

# TODO: undo
def classify_list(initial_options=[], strs_to_print_gen=[]):
    """
    Given a generator of strings to print, this list classification
    gives an easy-to-interact manual classification interaction in
    the terminal.

    Returns a generator for the user's answers.

    Accepts initial options, which should be prioritized (higher
    priority -- earlier shown)
    """

    running_options = initial_options # maps to age

    results = []
    history = []
    grabnext = []

    for to_print in left_leaning_chain(grabnext, strs_to_print_gen):
        print()
        print('*' * 79)
        print(to_print)
        history.append(to_print)
        print()

        selected_option = None
        sorted_options = sorted(
            running_options, key=running_options.get, reverse=True)
        option_offset = 0
        while True:
            letters = "fjdk"
            for i, letter in enumerate(letters):
                option_idx = option_offset + i
                if option_idx < len(sorted_options):
                    option = sorted_options[option_idx]
                else:
                    option = None
                print('{}:{}'.format(
                    letter, '<fill>' if option is None else ' ' + option))
            print('special: q - exit, <spc> - show next options, u - undo')
            c = getch()
            if c in letters:
                option_idx = option_offset + letters.index(c)
                if option_idx < len(running_options):
                    selected_option = sorted_options[option_idx]
                    print("\n--->", selected_option)
                else:
                    selected_option = _get_new_option()
                break
            elif c == ' ':
                option_offset += len(letters)
            elif c == 'q' or ord(c) == 4:
                raise StopIteration
            elif ord(c) == 3:
                # ctrl-c
                raise ValueError("user ctrl-c")
            elif c == 'u':
                if len(history) == 1:
                    continue
                results.pop()
                # repeat is intentional!
                grabnext.append(history.pop())
                grabnext.append(history.pop())
                break

        if selected_option is None:
            continue # must've undone

        oldmax = max(running_options.values()) if running_options else 0
        newmax = oldmax + 1
        running_options[selected_option] = newmax

        results.append(selected_option)


def getch():
    """
    Fetches a single character from stdin. If EOF is encountered
    then it is replaced with 'q'.
    """
    # https://stackoverflow.com/questions/510357
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    except EOFError:
        ch = 'q'
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def _get_new_option():
    """
    Print \n--> and wait for input
    """
    print("\n---> ", end='')
    sys.stdout.flush()
    try:
        selection = input()
    except EOFError:
        selection = '<empty>'
    return selection

def left_leaning_chain(a, b):
    for x in b:
        while a:
            yield a.pop()
        yield x
