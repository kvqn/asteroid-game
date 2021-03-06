import tkinter
import asyncio
import pickle
from .. import Get_Image, root, canvas, NEW_GAME_EVENT, loop, GAME


game_over_image = Get_Image("assets/game_over.png")

# NEW_GAME_EVENT = asyncio.Event()


async def game_over():
    GAME.clear()
    root.unbind("<Escape>")
    canvas.create_image(143, 300,anchor='nw', image=game_over_image)
    game_over_button1.place(x=643, y=540)
    game_over_button1.lift()
    game_over_button2.place(x=843, y=540)
    game_over_button2.lift()

from ..elements import save_data

def game_over_retry():
    save_data()
    # evaluate_highscores()
    NEW_GAME_EVENT.set()
    NEW_GAME_EVENT.clear()
    game_over_button1.place_forget()
    game_over_button2.place_forget()
    GAME.set()
    # asyncio.ensure_future(START_GAME())

from .pause_game import save_and_quit

game_over_button1 = tkinter.Button(root, activebackground='gray42', bg='gray69', fg='black', font=("LLPixel", 20), text="RETRY", command = game_over_retry)
game_over_button2 = tkinter.Button(root, activebackground='gray42', bg='gray69', fg='black', font=("LLPixel", 20), text="EXIT", command = save_and_quit)