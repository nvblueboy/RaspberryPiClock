## Display a clock on the screen and use a text-message based reminder system.

from clock import *

import logger

if __name__ == "__main__":
    mainClock = Clock()
    mainClock.win.run()
