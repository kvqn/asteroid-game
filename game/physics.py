import asyncio
from threading import Thread
from . import active_asteroids, active_beams, GAME, NEW_GAME_EVENT
from .objects.Ship import ship

class thread(Thread):
    def __init__(self):
        super().__init__(name="PhysicsThread")
        loop=asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    def ensure_future(self, coro):
        return asyncio.ensure_future(coro)