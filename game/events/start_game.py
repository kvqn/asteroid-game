import asyncio
from time import time
from .. import root, canvas
from ..events.pause_game import pause_game
start_time = time()

async def start_game():    
    root.bind("<Escape>", pause_game)
    from ..objects.Ship import ship
    from ..objects.Asteroid import START_LOOP
    asyncio.ensure_future(START_LOOP())
    canvas.place(x=300,y=100)
    root.lift(canvas)