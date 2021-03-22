import tkinter
import pickle
import asyncio
from .. import canvas, root, NEW_GAME_EVENT
from . import DATA


HighscoreLabels = []
HighscoreHeadingLabel = tkinter.Label(root, bg='black', fg='gold', font=("LLPixel", 32), text="HIGHSCORES")


def init():
    HighscoreHeadingLabel.place(x=10, y=90)
    evaluate_highscores()
    asyncio.ensure_future(lookout_for_new_game())

async def lookout_for_new_game():
    global HighscoreLabels
    while True:
        await NEW_GAME_EVENT.wait()
        for i in HighscoreLabels:
            i.place_forget()
        HighscoreLabels = []
        evaluate_highscores()
    

def evaluate_highscores():
    HIGHSCORES = list(DATA.highscores.items())
    HIGHSCORES.sort(reverse=True, key= lambda e : e[1])
    _ = 0
    for i in HIGHSCORES:
        _+=1
        label = tkinter.Label(root, bg="black", fg="white", font=("LLPixel",16), text=i[0], width = 10)
        label.place(x=10, y=100+_*50)
        HighscoreLabels.append(label)
        label = tkinter.Label(root, bg="black", fg="white", font=("LLPixel",16), text=str(i[1]), width=5)
        label.place(x=200, y=100+_*50)
        HighscoreLabels.append(label)
        if _ ==5 :
            break

