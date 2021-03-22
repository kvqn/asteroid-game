# This file contains all the variables and functions that are used by other files.
# The other files in this folder deal with loading different UI elements

import tkinter


SCORE = tkinter.IntVar(value=0)
LEVEL = tkinter.IntVar(value=1)
PLAYER_NAME = tkinter.StringVar()

import pickle

try:
    with open("save.dat", 'rb') as file:
        DATA = pickle.load(file)
    if not isinstance(DATA, dict):
        DATA = dict()
except FileNotFoundError:
    DATA = dict()
except EOFError:
    DATA = dict()

def save_data():
    if not PLAYER_NAME.get() in DATA or SCORE.get() > DATA[PLAYER_NAME.get()]:
        DATA[PLAYER_NAME.get()] = SCORE.get()
        with open("save.dat", 'wb') as file:
            pickle.dump(DATA, file)

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

