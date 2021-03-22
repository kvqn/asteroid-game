import tkinter
import asyncio
from .. import root, NEW_GAME_EVENT
from . import SCORE

ScoreHeadingLabel = tkinter.Label(root, bg='black',fg="gold", font=("LLPixel",32), text="SCORE")
ScoreLabel = tkinter.Label(root, bg="black", fg="white", font=("LLPixel",28), textvariable=SCORE, width=5)

def init():
    ScoreHeadingLabel.place(x=1380, y=90)
    ScoreLabel.place(x=1390, y=150)
    asyncio.ensure_future(lookout_for_new_game())

async def lookout_for_new_game():
    while True:
        await NEW_GAME_EVENT.wait()
        SCORE.set(0)