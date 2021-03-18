import tkinter
import asyncio
from .. import Get_Image, root, NEW_GAME_EVENT, GAME

bar_images = [
    Get_Image("assets/bar/bar_0.png"),
    Get_Image("assets/bar/bar_1.png"),
    Get_Image("assets/bar/bar_2.png"),
    Get_Image("assets/bar/bar_3.png"),
    Get_Image("assets/bar/bar_4.png")
]


bar_x = 10
bar_state = 0

def can_i_shoot_laser():
    if bar_state > 0:
        global bar_x
        bar_x-=95
        return True
    return False

canvas = tkinter.Canvas(root, width = 400, height = 61, bg='black', highlightthickness=0)
background_image = canvas.create_rectangle(10,10, bar_x, 51, fill="red")
main_image = canvas.create_image(0,0, anchor='nw', image=bar_images[0])


def init():
    canvas.place(x=800, y=920)
    asyncio.ensure_future(update_loop())
    asyncio.ensure_future(lookout_for_new_game())
    # print('bar loaded')

async def update_loop():
    global bar_x
    global bar_state
    while True:
        await asyncio.sleep(0.02)
        await GAME.wait()
        if bar_x < 390:
            bar_x+=0.75
            canvas.coords(background_image, 10,10, bar_x, 51)
            state = 0
            if bar_x > 390:
                state = 4
            elif bar_x > 295:
                state = 3
            elif bar_x > 200:
                state = 2
            elif bar_x > 105:
                state = 1
            if not state == bar_state:
                bar_state = state
                canvas.itemconfig(main_image, image = bar_images[state])

async def lookout_for_new_game():
    global bar_x
    while True:
        await NEW_GAME_EVENT.wait()
        bar_x = 10