import tkinter
import asyncio
import pickle
from .. import Get_Image, root, canvas, NEW_GAME_EVENT, loop, GAME, active_asteroids, active_beams

game_over_image = Get_Image("assets/game_over.png")

async def game_over(): # called when ship collides with asteroid
    GAME.clear()
    root.unbind("<Escape>")
    global game_over_image_tag
    game_over_image_tag = canvas.create_image(143, 300,anchor='nw', image=game_over_image)
    game_over_button1.place(x=643, y=540)
    game_over_button1.lift()
    game_over_button2.place(x=843, y=540)
    game_over_button2.lift()

from ..elements import save_data
from .pause_game import pause_game

def game_over_retry(): # called when player hits retry
    save_data()
    root.bind("<Escape>", pause_game)
    active_beams.clear()
    active_asteroids.clear()
    global game_over_image_tag
    canvas.delete(game_over_image_tag)
    game_over_button1.place_forget()
    game_over_button2.place_forget()
    NEW_GAME_EVENT.set()
    NEW_GAME_EVENT.clear()
    GAME.set()

from .pause_game import save_and_quit

game_over_button1 = tkinter.Button(root, activebackground='gray42', bg='gray69', fg='black', font=("LLPixel", 20), text="RETRY", command = game_over_retry)
game_over_button2 = tkinter.Button(root, activebackground='gray42', bg='gray69', fg='black', font=("LLPixel", 20), text="EXIT", command = save_and_quit)