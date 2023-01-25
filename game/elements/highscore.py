import tkinter
import asyncio
from .. import canvas, root
from . import JSON_SAVE_PATH
import json


HighscoreLabels = []
HighscoreHeadingLabel = tkinter.Label(root, bg='black', fg='gold', font=("LLPixel", 32), text="HIGHSCORES")


def init():
    HighscoreHeadingLabel.place(x=10, y=90)
    evaluate_highscores()

def reinit():
    global HighscoreLabels
    for i in HighscoreLabels:
        i.place_forget()
    HighscoreLabels = []
    evaluate_highscores()


def evaluate_highscores():
    try:
        with open(JSON_SAVE_PATH, 'r') as f:
            data = json.load(f)
        HIGHSCORES = list(data.items())
    except:
        HIGHSCORES = []
    j = 0
    for i in HIGHSCORES:
        j+=1
        label = tkinter.Label(root, bg="black", fg="white", font=("LLPixel",16), text=i[0], width = 10)
        label.place(x=10, y=100+j*50)
        HighscoreLabels.append(label)
        label = tkinter.Label(root, bg="black", fg="white", font=("LLPixel",16), text=str(i[1]), width=5)
        label.place(x=200, y=100+j*50)
        HighscoreLabels.append(label)
        if j ==5 :
            break

