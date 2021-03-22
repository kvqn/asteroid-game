import tkinter
import asyncio
from time import time
from .. import root, NEW_GAME_EVENT, canvas, Get_Image, GAME

time_stringvar = tkinter.StringVar()
time_stringvar.set('00:00')
Timer_Label = tkinter.Label(root, bg = 'black', fg = 'white', font = ("LLPixel", 32), textvariable = time_stringvar)
level_up_image = Get_Image("assets/level_up.png")
mins, secs = 0,0

def init():
    Timer_Label.place(x=400, y = 920)
    asyncio.ensure_future(update_loop())
    asyncio.ensure_future(lookout_for_new_game())

async def update_loop():
    from .level import LEVEL
    global mins, secs
    while True:
        await asyncio.sleep(1)
        await GAME.wait()
        secs +=1
        if secs==60:
            secs=0
            mins+=1
        time_stringvar.set("{:02d}:{:02d}".format(mins, secs))
        if mins*4 + secs/15 >= LEVEL.get():
            asyncio.ensure_future(animated_effect(x=300, y=300, image_object=level_up_image, small_tick_delay=4, big_tick_delay=40))
            LEVEL.set(LEVEL.get()+1)

async def lookout_for_new_game():
    global mins, secs
    while True:
        await NEW_GAME_EVENT.wait()
        mins, secs = 0,0

async def animated_effect(x, y, image_object, small_tick_delay, big_tick_delay): # Flashing level up text
    small_tick_delay=0.01*small_tick_delay
    big_tick_delay=0.01*big_tick_delay
    await asyncio.sleep(small_tick_delay)
    await GAME.wait()
    tag = canvas.create_image(x, y, anchor = 'nw', image = image_object)
    for _ in range(2):
        await asyncio.sleep(small_tick_delay)
        await GAME.wait()
        canvas.delete(tag)
        await asyncio.sleep(small_tick_delay)
        await GAME.wait()
        tag = canvas.create_image(x, y, anchor = 'nw', image = image_object)
    await asyncio.sleep(big_tick_delay)
    await GAME.wait()
    for _ in range(2):
        canvas.delete(tag)
        await asyncio.sleep(small_tick_delay)
        await GAME.wait()
        tag = canvas.create_image(x, y, anchor = 'nw', image = image_object)
        await asyncio.sleep(small_tick_delay)
        await GAME.wait()
    canvas.delete(tag)