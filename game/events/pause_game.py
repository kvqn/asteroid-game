# import asyncio
from pickle import dump
from tkinter import Button
from .. import root, GAME, loop
# from ..objects.Ship import ship
# from . import secondary_event_loop, secondary_update_loop

def pause_game(e):
    GAME.clear()
    # ship.unbind()
    save_quit_button.place(x=650, y=450)
    save_quit_button.lift()
    root.bind("<Escape>", resume_game)

def resume_game(e):
    # ship.bind()
    GAME.set()
    save_quit_button.place_forget()
    root.bind("<Escape>", pause_game)

from ..elements import save_data
 
def save_and_quit():
    save_data()
    loop.stop()
    # await asyncio.sleep(5)
    root.destroy()

save_quit_button = Button(root, activebackground="gray42", bg = "gray69", font = ("LLPixel", 20), text = "SAVE AND QUIT", command = save_and_quit, width = 20)