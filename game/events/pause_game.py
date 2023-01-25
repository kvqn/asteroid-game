from pickle import dump
from tkinter import Button
from .. import root, GAME, loop, Get_Image, canvas
import asyncio

def pause_game(e): # called when game is paused
    GAME.clear()
    asyncio.ensure_future(animated_effect(x=270, y=150, image_object=pause_image, small_tick_delay=4))
    save_quit_button.place(x=650, y=450)
    save_quit_button.lift()
    resume_button.place(x=650, y=400)
    resume_button.lift()
    root.bind("<Escape>", resume_game)

def resume_game(e): # called when game is resumed
    GAME.set()
    save_quit_button.place_forget()
    resume_button.place_forget()
    root.bind("<Escape>", pause_game)

from ..elements import save_data

def save_and_quit():
    loop.stop()
    root.destroy()

async def animated_effect(x, y, image_object, small_tick_delay): # flashing pause text
    small_tick_delay=0.01*small_tick_delay
    await asyncio.sleep(small_tick_delay)
    tag = canvas.create_image(x, y, anchor = 'nw', image = image_object)
    for _ in range(2):
        await asyncio.sleep(small_tick_delay)
        canvas.delete(tag)
        await asyncio.sleep(small_tick_delay)
        tag = canvas.create_image(x, y, anchor = 'nw', image = image_object)
    await GAME.wait()
    for _ in range(2):
        canvas.delete(tag)
        await asyncio.sleep(small_tick_delay)
        tag = canvas.create_image(x, y, anchor = 'nw', image = image_object)
        await asyncio.sleep(small_tick_delay)
    canvas.delete(tag)

pause_image = Get_Image("assets/paused.png")
resume_button = Button(root, activebackground="gray42", bg = "gray69", font = ("LLPixel", 20), text = "RESUME GAME", command = lambda : resume_game(None), width = 20)
save_quit_button = Button(root, activebackground="gray42", bg = "gray69", font = ("LLPixel", 20), text = "SAVE AND QUIT", command = save_and_quit, width = 20)
