import tkinter
import asyncio
from .. import root, Get_Image, NEW_GAME_EVENT
from . import LEVEL


level_heading_label = tkinter.Label(root, bg = 'black', fg = 'gold', font = ("LLPixel", 32), text = "LEVEL")
level_indicator_label = tkinter.Label(root, bg = 'black', fg = 'white', font = ("LLPixel", 72), textvariable = LEVEL)


def init():
    level_heading_label.place(x=80, y=500)
    level_indicator_label.place(x=110, y=550)
    asyncio.ensure_future(lookout_for_new_game())

async def lookout_for_new_game():
    while True:
        await NEW_GAME_EVENT.wait()
        LEVEL.set(1)