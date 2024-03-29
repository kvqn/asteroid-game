import asyncio
from time import time
from .. import root, canvas
from ..events.pause_game import pause_game

async def start_game():    
    root.bind("<Escape>", pause_game)
    from ..objects.Ship import ship # initialising ship
    from ..objects.Asteroid import START_LOOP
    asyncio.ensure_future(START_LOOP()) # initialising asteroid generation loop
    canvas.place(x=320,y=100)
    root.lift(canvas)