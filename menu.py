## TODO
"""
 
touch menu.py

SECTION 4 - MENU & MAIN PROGRAM LOOP
OWNED BY: M-0321 (Docs / Error-Handling Lead)

YOUR TASK: Tie everything together. Build the menu, collect user input,
call the other sections in order, and handle every failure gracefully -
the program should NEVER crash, only print an error and return to the menu.
"""

def get_reviews_from_user():
    """
    Collects multi-line review input from the user until they type DONE.

    Must return:
        str: all entered lines joined together (e.g. with "\\n")
    """
    print("Enter your reviews, one per line. Type DONE when finished.")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "DONE":
            break
        lines.append(line)
    return "\n".join(lines)


def choose_tone():
    """
    Shows a menu asking the user to pick a reply tone.

    Must return:
        str: either "formal" or "friendly"
    """
    print("choose_tone func")


def main_menu():
    """
    Shows the main menu (1. Analyse reviews, 2. Exit).

    Must return:
        str: the raw text the user typed (e.g. "1" or "2")
    """
    print("main_menu func")

def main():
    """
    The main program loop. Ties Sections 1-3 together via the menu.
    Must never crash - every failure path should print a message and
    return to the menu instead of raising an unhandled exception.
    """

    print ("from menu file main func")