#!/usr/bin/env python3

import os

DEBUG = int(os.getenv("DEBUG", '0'))
LOCAL = bool(os.getenv("LOCAL", False))
def colored(st, color, background=False): return f"\u001b[{10*background+60*(color.upper() == color)+30+['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'].index(color.lower())}m{st}\u001b[0m" if color is not None else st
