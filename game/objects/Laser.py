import asyncio
from .. import Get_Image, RangedInteger, active_asteroids, active_beams, canvas, NEW_GAME_EVENT, OutOfBounds, GAME
from ..elements.score import SCORE

laser_image = Get_Image("assets/beam.png")

class Laser_Beam:
    def __init__(self):
        from .Ship import ship
        self.x_coord = ship.x_coord.value + 50
        self.y_coord = RangedInteger(min = -200, max = 800, value = ship.y_coord.value, raise_border_exceptions=True)
        self.tag = canvas.create_image(self.x_coord, self.y_coord.value, anchor = 'nw', image = laser_image)
        j = None
        for i in active_asteroids:
            if i.x_coord <= self.x_coord <= i.x_coord+120 and i.y_coord.value < self.y_coord.value:
                try:
                    if i.y_coord.value > j.y_coord.value:
                        j = i
                except AttributeError:
                    j = i
        if j:
            ticks = (self.y_coord.value - j.y_coord.value)//24
            self.queue_detonation(ticks)
            j.queue_detonation(ticks)
            # SCORE.set(SCORE.get() + 1)
            active_asteroids.remove(j)
        else:
            active_beams.add(self)
        self.update_task = asyncio.ensure_future(self.update_coords())
        self.lookout_task = asyncio.ensure_future(self.lookout_for_new_game_event())
    
    async def lookout_for_new_game_event(self):
        await NEW_GAME_EVENT.wait()
        self.update_task.cancel()
        canvas.delete(self.tag)
        try:
            self.detonation_task.cancel()
        except:
            pass
        del self
    
    async def detonation_coro(self, ticks):
        for _ in range(ticks):
            await asyncio.sleep(0.02)
            await GAME.wait()
        SCORE.set(SCORE.get() + 1)
        self.update_task.cancel()
        self.lookout_task.cancel()
        canvas.delete(self.tag)
        # print("detonated laser.")
        del self

    def queue_detonation(self, ticks):
        self.detonation_task = asyncio.ensure_future(self.detonation_coro(ticks))
    
    async def update_coords(self):
        try:
            while True:
                await asyncio.sleep(0.02)
                await GAME.wait()
                self.y_coord -= 16
                canvas.coords(self.tag, self.x_coord, self.y_coord.value)
        except OutOfBounds:
            canvas.delete(self.tag)
            try:
                active_beams.remove(self)
            except KeyError:
                pass
            # print("Destroyed laser.")
            self.lookout_task.cancel()
            try:
                self.detonation_task.cancel()
            except:
                pass
            canvas.delete(self.tag)
            del self

