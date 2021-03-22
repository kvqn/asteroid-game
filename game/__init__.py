import tkinter
root = tkinter.Tk()
from .install import INSTALL

INSTALL() # Making sure dependencies are installed.

import asyncio
import pickle
from time import time
from PIL import Image, ImageTk

def Get_Image(file):
    return ImageTk.PhotoImage(Image.open(file))

root.geometry("1600x1000")
root.resizable(width=False, height=False)
root.configure(bg='black')
NEW_GAME_EVENT = asyncio.Event() # Set when user starts a new game
GAME = asyncio.Event() # Set when the game is running (not paused)

active_asteroids = set()
active_beams = set()

canvas = tkinter.Canvas(root, width = 1000, height = 800, bg = 'black')

loop = asyncio.get_event_loop()

def closing_protocol(): # This will be executed when the window is closed.
    from .elements import save_data
    GAME.clear()
    loop.stop()
    save_data()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", closing_protocol)


async def main_update_loop(): # Loop for keeping the window alive
    while True:
        await asyncio.sleep(0.01)
        root.update()


def START():
    GAME.set()
    from .elements import Init
    asyncio.ensure_future(main_update_loop())
    root.update()
    Init() # Initiates UI elements
    loop.run_forever()