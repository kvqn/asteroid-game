# This file contains all the variables and functions that are used by other files.
# The other files in this folder deal with loading different UI elements

import tkinter
import traceback
import json
import os
import game


SCORE = tkinter.IntVar(value=0)
LEVEL = tkinter.IntVar(value=1)
PLAYER_NAME = tkinter.StringVar()
JSON_SAVE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(game.__file__))), 'scores.json')

def save_data():
    name = PLAYER_NAME.get()
    if not name == '':
        try:
            with open(JSON_SAVE_PATH, 'r') as f:
                data = json.load(f)
            if name in data:
                if data[name] < SCORE.get():
                    data[name] = SCORE.get()
            else:
                data[name] = SCORE.get()
        except FileNotFoundError:
            data = {name: SCORE.get()}

        with open(JSON_SAVE_PATH, 'w') as f:
            json.dump(data, f, indent=4)

def Init():
    from .bar import init
    init()
    from .highscore import init
    init()
    from .level import init
    init()
    from .score import init
    init()
    from .timer import init
    init()
    from .playername import init
    init()

