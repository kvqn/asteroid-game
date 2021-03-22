import tkinter
import asyncio
from random import randint, choice
from .. import Get_Image, active_beams, active_asteroids, NEW_GAME_EVENT, canvas, root, GAME
from ..elements.level import LEVEL
from . import RangedInteger, OutOfBounds

# Loading images

asteroid_images = (
    Get_Image("assets/asteroids/asteroid_1.png"),
    Get_Image("assets/asteroids/asteroid_2.png"),
    Get_Image("assets/asteroids/asteroid_3.png"),
    Get_Image("assets/asteroids/asteroid_4.png"),
    Get_Image("assets/asteroids/asteroid_5.png"),
    Get_Image("assets/asteroids/asteroid_6.png"),
    Get_Image("assets/asteroids/asteroid_7.png"),
    Get_Image("assets/asteroids/asteroid_8.png"),
    Get_Image("assets/asteroids/asteroid_9.png"),
    Get_Image("assets/asteroids/asteroid_10.png"),
    Get_Image("assets/asteroids/asteroid_11.png"),
    Get_Image("assets/asteroids/asteroid_12.png"),
    Get_Image("assets/asteroids/asteroid_13.png"),
    Get_Image("assets/asteroids/asteroid_14.png"),
    Get_Image("assets/asteroids/asteroid_15.png"),
    Get_Image("assets/asteroids/asteroid_16.png")
)

explosion_images = (
    Get_Image("assets/explosions/explosion_1.png"),
    Get_Image("assets/explosions/explosion_2.png"),
    Get_Image("assets/explosions/explosion_3.png"),
    Get_Image("assets/explosions/explosion_4.png"),
    Get_Image("assets/explosions/explosion_5.png"),
    Get_Image("assets/explosions/explosion_6.png"),
    Get_Image("assets/explosions/explosion_7.png")
)

level_up_image = Get_Image("assets/level_up.png")

class Asteroid: # Asteroid class that takes care of all its properties
    def __init__(self):
        self.x_coord = randint(80, 800)
        self.y_coord = RangedInteger(min=-300, max=1200, value=-200, raise_border_exceptions=True)
        self.tag = canvas.create_image(self.x_coord, -200, anchor = 'nw', image = choice(asteroid_images))
        j = None
        for i in active_beams:
            if self.x_coord <= i.x_coord <= self.x_coord+120 and i.y_coord.value > self.y_coord.value:
                try:
                    if i.y_coord.value < j.y_coord.value :
                        j = i
                except AttributeError:
                    j = i
        if j:
            ticks = (j.y_coord.value - self.y_coord.value)//24
            self.queue_detonation(ticks)
            j.queue_detonation(ticks)
            active_beams.remove(j)
        else:
            active_asteroids.add(self)
        self.update_task = asyncio.ensure_future(self.update_coords())
        self.lookout_task = asyncio.ensure_future(self.lookout_for_new_game_event())

    async def lookout_for_new_game_event(self):
        await NEW_GAME_EVENT.wait()
        self.update_task.cancel()
        try:
            self.detonation_task.cancel()
        except:
            pass
        canvas.delete(self.tag)
        del self
            

    async def update_coords(self):
        try:
            while True:
                await asyncio.sleep(0.02)
                await GAME.wait()
                self.y_coord += 8
                canvas.coords(self.tag, self.x_coord, self.y_coord.value)
        except OutOfBounds:
            canvas.delete(self.tag)
            try:
                active_asteroids.remove(self)
            except KeyError:
                pass
            self.lookout_task.cancel()
            try:
                self.detonation_task.cancel()
            except:
                pass
            del self
    
    async def detonation_coro(self, ticks):
        for _ in range(ticks):
            await asyncio.sleep(0.02)
            await GAME.wait()
        self.explosion_images = iter(explosion_images)
        self.x_coord -= 40
        self.y_coord -= 40
        try:
            while True:
                canvas.delete(self.tag)
                self.tag = canvas.create_image(self.x_coord, self.y_coord.value, anchor = 'nw', image = next(self.explosion_images))
                await asyncio.sleep(0.1)
                await GAME.wait()

        except StopIteration:
            self.update_task.cancel()
            self.lookout_task.cancel()
            canvas.delete(self.tag)
            del self

    def queue_detonation(self, ticks):
        self.detonation_task = asyncio.ensure_future(self.detonation_coro(ticks))

async def AsteroidGenerationLoop(): # Generates asteroid
    while True:
        await asyncio.sleep(2/LEVEL.get())
        await GAME.wait()
        Asteroid()


async def START_LOOP():
    loop_task = asyncio.ensure_future(AsteroidGenerationLoop())
    while True:
        await NEW_GAME_EVENT.wait()
        loop_task.cancel()
        loop_task = asyncio.ensure_future(AsteroidGenerationLoop())
