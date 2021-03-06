import tkinter
import asyncio
from time import time
from .. import root, NEW_GAME_EVENT, canvas, Get_Image, GAME

time_stringvar = tkinter.StringVar()
time_stringvar.set('00:00')
Timer_Label = tkinter.Label(root, bg = 'black', fg = 'white', font = ("LLPixel", 32), textvariable = time_stringvar)
level_up_image = Get_Image("assets/level_up.png")


def init():
    Timer_Label.place(x=400, y = 920)
    asyncio.ensure_future(update_loop())
    asyncio.ensure_future(lookout_for_new_game())
    print('timer loaded')

async def update_loop():
    from ..events.start_game import start_time
    from .level import LEVEL
    while True:
        await asyncio.sleep(1)
        await GAME.wait()
        mins, secs = divmod(int(time() - start_time), 60)
        time_stringvar.set('{:02d}:{:02d}'.format(mins, secs))
        if mins*4 + secs/15 >= LEVEL.get():
            asyncio.ensure_future(create_image_animated_effect(x=300, y=300, image_object=level_up_image, small_tick_delay=4, big_tick_delay=40))
            LEVEL.set(LEVEL.get()+1)

async def lookout_for_new_game():
    while True:
        await NEW_GAME_EVENT.wait()
        time_stringvar.set("00:00")

async def create_image_animated_effect(x, y, image_object, small_tick_delay, big_tick_delay):
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