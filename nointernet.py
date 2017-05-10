import curses
import time
import textwrap
import curses.textpad
import curses.ascii


def typeout(stdscr, string, y, x, delay=50):
    i = 0
    for ch in string:
        stdscr.addch(y, x + i, ch)
        i += 1
        curses.napms(delay)
        stdscr.refresh()

def introduction(stdscr):
    height, width = stdscr.getmaxyx()
    # Introduction
    intro_string = "You appear to be unable to connect to the internet."
    typeout(stdscr, intro_string, height // 2 - 1, width // 2 - len(intro_string) // 2)

    quest_string = "Contact your local ISP provider to begin resolving the issue."
    typeout(stdscr, quest_string, height // 2, width // 2 - len(quest_string) // 2)
    curses.napms(1000)

    end_string = "Based on a true story."
    typeout(stdscr, end_string, height // 2 + 2, width // 2 - len(end_string) // 2)
    stdscr.getkey()

def input_validator(key):
    if key == 127:
        # Mac fix for backspace
        return curses.KEY_BACKSPACE
    return key

def main(stdscr):
    # Setup
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    # introduction(stdscr)

    # Post introduction setup
    stdscr.nodelay(1)
    curses.noecho()

    # Create text windows
    text_window = curses.newwin(38, 82, height // 2 - 21, width // 2 - 41)
    text_height, text_width = text_window.getmaxyx()

    input_box = curses.newwin(3, 82, height // 2 + 17, width // 2 - 41)
    input_window = curses.newwin(1, 80, height // 2 + 18, width // 2 - 40)
    textbox = curses.textpad.Textbox(input_window, True)

    # Variables
    running = True
    days = 0
    user_input = ""
    get_input = True
    current_message = ["You moved to a new apartment complex and have no access to internet. But fear not, you are a competent, young adult! There's nothing you can't handle with a bit of resolve and patience. Your goal is to get your internet installed by FYMedia.", "", "Type 'help' for a list of commands."]
    options = []

    # Game loop
    while running:
        stdscr.erase()
        if user_input:
            command = user_input.split()
            if command[0] == "exit" or command[0] == "quit":
                # Quit all recieving input and quit
                running = False
                get_input = False
            elif command[0] == "help":
                current_message = [
                    "lookup [thing] - Find out information about a thing",
                    "call [phone number] - Calls the company.",
                    "wait - Wait one day.",
                    "days - Returns number of days past since no internet.",
                    "exit/quit - Quit the game"
                ]
            elif command[0] == "lookup":
                if len(command) > 1:
                    query = " ".join(command[1:]).strip()
                    if query == "fymedia":
                        current_message = [
                            "Luckily you were smart enough to write down the contact info of FYMedia before you didn't have access to internet. Scribbled on the back of a unopenned envelope you see:",
                            "",
                            "Phone: (993) 273-6782",
                            "Website: www.fymediaconnect.com",
                        ]
                    elif query == "cux" or query == "cux cable":
                        current_message = [
                            "You recall the website of CUX Cable but don't have the phone number on hand:",
                            "",
                            "Website: www.thecuxprovider.com"
                        ]
                    elif query == "sodacookie":
                        current_message = [
                            "The God of Curses."
                        ]
                    else:
                        current_message = ["You can't seem to recall or find any information on %s." % query]
                else:
                    current_message = ["The 'lookup' command requires one argument.", "", "Please try again or type 'help' for a list of commands."]
            else:
                # Default if missing info
                current_message = ["'%s' is an unknown command." % user_input.split()[0], "", "Please try again or type 'help' for a list of commands."]

        if current_message:
            text_window.erase()
            h = 0
            for message in current_message:
                i = 0
                wrapped_message = textwrap.wrap(message, text_width - 2)
                for i, line in enumerate(wrapped_message):
                    text_window.addstr(1 + i + h, 1, line)
                h += i + 1

        # Draw rectangle
        text_window.border()
        input_box.border()

        # Refresh the windows
        stdscr.noutrefresh()
        text_window.noutrefresh()
        input_box.noutrefresh()
        input_window.noutrefresh()
        curses.doupdate()

        # Handle text events after displaying screen
        if get_input:
            user_input = textbox.edit(input_validator).lower().strip()
            input_window.erase()
