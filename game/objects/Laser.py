import asyncio
from .. import Get_Image, RangedInteger, active_asteroids, active_beams, canvas, NEW_GAME_EVENT, OutOfBounds, GAME
from ..elements.score import SCORE

laser_image = Get_Image("assets/beam.png")

class Laser_Beam:
    def __init__(self):
        from .Ship import ship
        self.x_coord = ship.x_coord.value + 50
        self.y_coord = RangedInteger(min = -200, max = 800, value = ship.y_coord.value, raise_border_exceptions=True)
        self.object = canvas.create_image(self.x_coord, self.y_coord.value, anchor = 'nw', image = laser_image)
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
            asyncio.ensure_future(self.queue_detonation(ticks))
            asyncio.ensure_future(j.queue_detonation(ticks))
            SCORE.set(SCORE.get() + 1)
            active_asteroids.remove(j)
        else:
            active_beams.add(self)
        self.update_task = asyncio.ensure_future(self.update_coords())
        self.lookout_task = asyncio.ensure_future(self.lookout_for_new_game_event())
    
    def delete(self):
        self.update_task.cancel()
        self.lookout_task.cancel()
    
    async def lookout_for_new_game_event(self):
        await NEW_GAME_EVENT.wait()
        self.update_task.cancel()
    
    async def queue_detonation(self, ticks):
        for _ in range(ticks):
            await asyncio.sleep(0.02)
            await GAME.wait()
        canvas.delete(self.object)
        self.delete()
        # print("detonated laser.")
    
    async def update_coords(self):
        try:
            while True:
                await asyncio.sleep(0.02)
                await GAME.wait()
                self.y_coord -= 16
                canvas.coords(self.object, self.x_coord, self.y_coord.value)
        except OutOfBounds:
            canvas.delete(self.object)
            try:
                active_beams.remove(self)
            except KeyError:
                pass
            # print("Destroyed laser.")
            self.delete()
