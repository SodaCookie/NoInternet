import curses
import time
import re
import textwrap
import curses.textpad
import curses.ascii
import pygame
import random
import threading
import subprocess
import string

from gamestate import GameState
from fymediatree import fymediatree
from neighbourtree import neighbour_norm_tree
from lookuptable import lookup_table


QUOTES = [
    ["The two most powerful warriors are patience and time.", "Leo Tolstoy"],
    ["Our greatest weakness lies in giving up.", "The most certain way to succeed is always to try just one more time.", "Thomas A. Edison"],
    ["How did it get so late so soon?", "It's night before it's afternoon.", "December is here before it's June.", "My goodness how the time has flewn.", "How did it get so late so soon?", "Dr. Seuss"],
    ["Yesterday is gone.", "Tomorrow has not yet come.", "We have only today. Let us begin.", "Mother Teresa"],
    ["It is the time you have wasted for your rose", "that makes your rose so important.", "Antoine de Saint-Exupery"],
    ["They always say time changes things,", "but you actually have to change them yourself.", "Andy Warhol"],
    ["A man who dares to waste one hour of time", "has not discovered the value of life.", "Charles Darwin"],
    ["Don’t waste your time in anger, regrets, worries, and grudges.", "Life is too short to be unhappy.", "Roy T. Bennett"],
    ["Time is an illusion.", "Albert Einstein"],
    ["Those who make the worst use of their time", "are the first to complain of its brevity.", "Jean de La Bruyere"],
    ["Time is a created thing.", "To say 'I don't have time,'", "is like saying, 'I don't want to.", "Lao Tzu"],
    ["There's never enough time to do all the nothing you want.", "Bill Watterson"],
    ["Time is what we want most,", "but what we use worst.", "William Penn"],
    ["Time takes it all, whether you want it to or not.", "Stephen King"],
    ["Rivers know this: there is no hurry.", "We shall get there some day.", "A.A. Milne"],
    ["Patience is bitter, but its fruit is sweet.", "Aristotle"],
    ["Knowing trees, I understand the meaning of patience.", "Knowing grass, I can appreciate persistence.", "Hal Borland"]
]

def set_partial_network():
    GameState.network_status = "WEAK CONNECTION"

EFFECTS = {
    "partial" : set_partial_network
}

def typeout(stdscr, string, y, x, delay=0.05):
    i = 0
    for ch in string:
        stdscr.addch(y, x + i, ch)
        i += 1
        time.sleep(delay)
        stdscr.refresh()

def stop_idle_music():
    pygame.mixer.music.stop()
    GameState.phone_on = False

def wait(stdscr, quote):
    stdscr.nodelay(0)
    stdscr.erase()
    height, width = stdscr.getmaxyx()
    displace_h = (len(quote) - 1) // 2
    # Introduction
    for i, line in enumerate(quote[:-1]):
        typeout(stdscr, line, height // 2 - displace_h + i, width // 2 - len(line) // 2, 0.1)
        time.sleep(0.2)

    time.sleep(1)
    typeout(stdscr, quote[-1], height // 2 + displace_h + 2, width // 2 - len(quote[-1]) // 2, 0.1)

    stdscr.getkey()
    stdscr.nodelay(1)

def step_conversation():
    msg = GameState.conversation_tree[GameState.conversation_node]["message"]
    raw_msg = "\n".join(msg)
    conversation_globals = {
        "days" : GameState.days
    }
    processed_msg = re.sub("{(.+)}", lambda match: str(eval(match.group(1), conversation_globals)), raw_msg)
    GameState.conversation_log.append(processed_msg)

def start_conversation(dialog_tree):
    GameState.conversation_on = True
    GameState.conversation_tree = dialog_tree
    GameState.conversation_node = "main"
    GameState.conversation_log = []
    step_conversation()

def respond_conversation(index):
    node = GameState.conversation_tree[GameState.conversation_node]
    try:
        GameState.conversation_node = node["choices"][index][0]
        GameState.conversation_log.append(node["choices"][index][1])
        if "flag" in node:
            GameState.flags.add(node["flag"])
            if node["flag"] in EFFECTS:
                EFFECTS[node["flag"]]()
        if GameState.conversation_node == "exit":
            # No more choices, we exit
            GameState.conversation_on = False
            GameState.current_message = [node["choices"][index][1]]
            return False
        else:
            step_conversation()
            return True
    except IndexError:
        pass

def test_email(stdscr):
    success = random.randint(0, 9) < (2 if not GameState.debug else 10) # 20% chance
    wait(stdscr, ["Connecting to network...", "Loading browser page...", "Opening email...", "SUCCESS" if success else "UNAVAILABLE"])
    return success

def check_email(stdscr):
    if "partial" in GameState.flags:
        if test_email(stdscr):
            if "setup" in GameState.flags:
                pass
    else:
        GameState.current_message = ["You have no internet to check email."]

def start_call(dialog_tree):
    # Start the music
    pygame.mixer.music.load("elevator.wav")
    pygame.mixer.music.play()
    delay = random.randrange(10, 20)
    timer = threading.Timer(delay, stop_music)
    timer.setDaemon(True)
    timer.start()
    timer = threading.Timer(delay + 0.5, start_conversation)
    timer.setDaemon(True)
    timer.start()
    GameState.phone_on = True

def introduction(stdscr):
    stdscr.nodelay(0)
    height, width = stdscr.getmaxyx()
    # Introduction
    intro_string = "You appear to be unable to connect to the internet."
    typeout(stdscr, intro_string, height // 2 - 1, width // 2 - len(intro_string) // 2)

    quest_string = "Contact your local ISP provider to begin resolving the issue."
    typeout(stdscr, quest_string, height // 2, width // 2 - len(quest_string) // 2)
    time.sleep(1)

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
    pygame.mixer.init()
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    if not GameState.debug:
        introduction(stdscr)

    # Post introduction setup
    stdscr.nodelay(1)
    curses.noecho()
    random.shuffle(QUOTES)
    quote_index = 0

    # Create text windows
    text_window = curses.newwin(35, 82, height // 2 - 18, width // 2 - 41)
    text_height, text_width = text_window.getmaxyx()

    input_box = curses.newwin(3, 82, height // 2 + 17, width // 2 - 41)
    input_window = curses.newwin(1, 80, height // 2 + 18, width // 2 - 40)
    textbox = curses.textpad.Textbox(input_window, True)

    status_window = curses.newwin(1, 80, height // 2 - 19, width // 2 - 40)

    # Initialize the first message
    GameState.current_message = ["You moved to a new apartment complex and have no access to internet. But fear not, you are a competent, young adult! There's nothing you can't handle with a bit of resolve and patience. Your goal is to get your internet installed by FYMedia.", "", "Type 'help' for a list of commands."]

    # Game loop
    while GameState.running:
        stdscr.erase()
        if GameState.user_input:
            previous_buffer = GameState.current_message
            command = GameState.user_input.split()
            if command[0] == "exit" or command[0] == "quit":
                # Quit all event loop
                GameState.running = False
                break
            elif GameState.phone_on:
                # Redirect all messages to the screen
                GameState.current_message.append(GameState.user_input)
                GameState.current_message.append(random.choice([
                    "You're call is important to us. Please stay on the line.",
                    "Someone will be here to assist you shortly. Please stay on the line.",
                    "We're always here to help. A service representative will be with you shortly. Please stay on the line.",
                    "You are a valued customer. Someone will be able to assist you shortly. Please stay on the line."
                ]))
            elif GameState.terminal_on:
                if command[0] == "test" and GameState.debug:
                    start_conversation(neighbour_norm_tree)
                    GameState.current_message = GameState.conversation_log
                elif command[0] == "wait":
                    if not GameState.debug:
                        wait(stdscr, QUOTES[quote_index % len(QUOTES)])
                    quote_index += 1
                    GameState.days += 1
                elif command[0] == "days":
                    GameState.current_message = [
                        "It's been %d days since you haven't had internet." % int(GameState.days / 2)
                    ]
                    sass_quote = None
                    if GameState.days == 6:
                        sass_quote = "Something feels off. You've been disconnected for too long."
                    if sass_quote:
                        GameState.current_message.append(sass_quote)
                elif command[0] == "back":
                    GameState.current_message = GameState.previous_message
                elif command[0] == "email":
                    check_email(stdscr)
                elif command[0] == "conversation":
                    if GameState.conversation_on:
                        GameState.current_message = GameState.conversation_log
                    else:
                        GameState.current_message = ["You aren't holding any conversations at the moment."]
                elif command[0] == "help":
                    GameState.current_message = [
                        "lookup [thing] - Find out information about a thing\n" +
                        "call [phone number] - Calls the company.\n" +
                        "wait - Wait one day.\n" +
                        "days - Returns number of days past since no internet.\n" +
                        "back - restore the message that came before.\n" +
                        "exit/quit - Quit the game.\n" +
                        "email - Check your email (needs internet to function)" +
                        "conversation - Return to the conversation if there is one ongoing"
                    ]
                elif command[0] == "lookup":
                    if len(command) > 1:
                        query = " ".join(command[1:]).strip()
                        if query in lookup_table:
                            GameState.current_message = lookup_table[query]
                        else:
                            GameState.current_message = ["You can't seem to recall or find any information on %s." % query]
                    else:
                        GameState.current_message = ["The 'lookup' command requires one argument.", "", "Please try again or type 'help' for a list of commands."]
                elif command[0] == "call":
                    if len(command) > 1:
                        # Normalize all numbers
                        query = "".join(command[1:])
                        query = query.replace("-", "").replace("(", "").replace(")", "")
                        if query == "9932736782":
                            start_conversation(fymediatree)
                            GameState.current_message = GameState.conversation_log
                        elif query == "5662734321":
                            if "partial" in GameState.flags:
                                pass
                            elif "annoyed" in GameState.flags:
                                pass
                            else:
                                start_conversation(neighbour_norm_tree)
                            GameState.current_message = GameState.conversation_log
                        elif query.isnumeric():
                            GameState.current_message = ["The number you have dialed is currently unavailable. Ensure that you have typed the correct number then hangup and redial the number.", "", "The phone display shows '%s'" % query]
                        else:
                            GameState.current_message = ["That's not a number."]
                    else:
                        GameState.current_message = ["The 'call' command requires a phone number.", "", "Please try again or type 'help' for a list of commands."]
                else:
                    if GameState.conversation_on:
                        if command[0].isnumeric():
                            if respond_conversation(int(command[0]) - 1):
                                GameState.current_message = GameState.conversation_log
                    else:
                        # Default if missing info
                        GameState.current_message = ["'%s' is an unknown command." % GameState.user_input.split()[0], "", "Please try again or type 'help' for a list of commands."]
            GameState.previous_message = previous_buffer
        if GameState.current_message:
            text_window.erase()
            lines = [] # Buffer
            if GameState.conversation_on:
                right_justify = False
                # Special alternating justifying
                for message in GameState.current_message:
                    for split_line in message.split("\n"):
                        wrapped_message = textwrap.wrap(split_line, (text_width - 2) // 3 * 2)
                        for line in wrapped_message:
                            if right_justify:
                                line = line.rjust(text_width - 2)
                            lines.append(line)
                        if not wrapped_message:
                            lines.append("")
                    lines.append("")
                    right_justify = not right_justify
            else:
                # Default to text
                for message in GameState.current_message:
                    for split_line in message.split("\n"):
                        wrapped_message = textwrap.wrap(split_line, text_width - 2)
                        for line in wrapped_message:
                            lines.append(line)
                        if not wrapped_message:
                            lines.append("")

            # Check for overflow
            if len(lines) > text_height - 2:
                lines = lines[-(text_height - 2):]

            # Draw buffer to screen
            for i, line in enumerate(lines):
                text_window.addstr(1 + i, 1, line)

        # Draw rectangle
        text_window.border()
        input_box.border()

        # Draw status
        status_window.erase()
        length = len(GameState.network_status) + len("DAY: %d [%s]" % (GameState.days // 2 + 1, "MORNING" if not GameState.days % 2 else "EVENING"))
        status_string = GameState.network_status + (" " * (79 - length)) + "DAY: %d [%s]" % (GameState.days // 2 + 1, "MORNING" if not GameState.days % 2 else "EVENING")
        status_window.addstr(status_string)

        # Refresh the windows
        stdscr.noutrefresh()
        text_window.noutrefresh()
        input_box.noutrefresh()
        status_window.noutrefresh()
        input_window.noutrefresh()
        curses.doupdate()

        # Handle text events after displaying screen
        if GameState.terminal_on:
            GameState.user_input = textbox.edit(input_validator).lower().strip()
            input_window.erase()
