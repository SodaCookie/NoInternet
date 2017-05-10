import os
import sys
import curses
import nointernet
import threading

def can_connect_to_internet():
    """Read the function title..."""
    hostname = "8.8.8.8" #example
    response = os.system("ping -c 1 " + hostname)
    return response == 0

if __name__ == '__main__':
    # if can_connect_to_internet():
    #     print("You appear to be able to connect to the internet. For a more authentic experience, please disconnect you computer from the network.")
    #     sys.exit(1)
    curses.wrapper(nointernet.main)
