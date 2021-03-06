import tkinter


SCORE = tkinter.IntVar(value=0)
LEVEL = tkinter.IntVar(value=1)
PLAYER_NAME = tkinter.StringVar()

class SavedData:
    def __init__(self):
        self.highscores = dict()

import pickle

try:
    with open("save.dat", 'rb') as file:
        DATA = pickle.load(file)
    if not isinstance(DATA, SavedData):
        DATA = SavedData()
except FileNotFoundError:
    DATA = SavedData()
except EOFError:
    DATA = SavedData()

def save_data():
    if not PLAYER_NAME.get() in DATA.highscores or SCORE.get() > DATA.highscores[PLAYER_NAME.get()]:
        DATA.highscores[PLAYER_NAME.get()] = SCORE.get()
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

