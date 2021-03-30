import tkinter
import pickle
import asyncio
from .. import canvas, root
from . import cur


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
    cur.execute("SELECT * FROM scores ORDER BY score DESC;")
    HIGHSCORES = cur.fetchall()
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

