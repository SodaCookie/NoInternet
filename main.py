import os
import sys
import curses
import nointernet
import threading
import warnings
import time
import subprocess
from gamestate import GameState


def can_connect_to_internet_nout():
    try:
        hostname = "8.8.8.8" #example
        output = subprocess.check_output("ping -c 1 " + hostname, shell=True, stderr=subprocess.DEVNULL)
    except:
        return False
    return True

def can_connect_to_internet():
    """Read the function title..."""
    hostname = "8.8.8.8" #example
    response = os.system("ping -c 1 " + hostname)
    return response == 0

def connection_test_thread():
    while not can_connect_to_internet_nout():
        time.sleep(1)
    GameState.cheated = True
    GameState.running = False

if __name__ == '__main__':
    debug = False
    if len(sys.argv) >= 2:
        if sys.argv[1] == "debug":
            GameState.debug = True

    if not GameState.debug and can_connect_to_internet():
        print("You appear to be able to connect to the internet. For a more authentic experience, please disconnect you computer from the network.")
        sys.exit(1)

    # Start the check thread
    if not GameState.debug:
        thread = threading.Thread(target=connection_test_thread)
        thread.setDaemon(True)
        thread.start()

    # Start the main thread
    curses.wrapper(nointernet.main)
    if GameState.cheated:
        print("Cheating detected. You appear to be able to connect to the internet again.")
