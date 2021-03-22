import asyncio
from .. import RangedInteger, root, Get_Image, canvas, NEW_GAME_EVENT, active_asteroids, GAME
from .Laser import Laser_Beam
from ..events.game_over import game_over
from ..events.pause_game import pause_game, resume_game
from ..elements.bar import can_i_shoot_laser


ship_image = Get_Image("assets/ship_final.png")

class Ship:
    def __init__(self):
        self.root = root
        self.object = canvas.create_image(500,500, anchor='nw', image = ship_image)
        self.x_coord = RangedInteger(min=0, max=900 ,value=500)
        self.y_coord = RangedInteger(min=0, max=750 ,value=500)
        self.velocity_up = False
        self.velocity_down = False
        self.velocity_left = False
        self.velocity_right = False
        self.update_future = asyncio.ensure_future(self.update_coords_loop())
        self.lookout_future = asyncio.ensure_future(self.lookout_for_new_game_event())
        self.bind()

    def bind(self):
        root.bind("<KeyPress-Up>", self.press_up)
        root.bind("<KeyPress-Down>", self.press_down)
        root.bind("<KeyPress-Left>", self.press_left)
        root.bind("<KeyPress-Right>", self.press_right)
        root.bind("<KeyRelease-Up>", self.release_up)
        root.bind("<KeyRelease-Down>", self.release_down)
        root.bind("<KeyRelease-Left>", self.release_left)
        root.bind("<KeyRelease-Right>", self.release_right)
        root.bind("<KeyPress-w>", self.press_up)
        root.bind("<KeyPress-s>", self.press_down)
        root.bind("<KeyPress-a>", self.press_left)
        root.bind("<KeyPress-d>", self.press_right)
        root.bind("<KeyRelease-w>", self.release_up)
        root.bind("<KeyRelease-s>", self.release_down)
        root.bind("<KeyRelease-a>", self.release_left)
        root.bind("<KeyRelease-d>", self.release_right)
        root.bind("<KeyPress-W>", self.press_up)
        root.bind("<KeyPress-S>", self.press_down)
        root.bind("<KeyPress-A>", self.press_left)
        root.bind("<KeyPress-D>", self.press_right)
        root.bind("<KeyRelease-W>", self.release_up)
        root.bind("<KeyRelease-S>", self.release_down)
        root.bind("<KeyRelease-A>", self.release_left)
        root.bind("<KeyRelease-D>", self.release_right)
        root.bind("<KeyPress-space>", self.shoot_laser)
    
    def unbind(self):
        root.unbind("<KeyPress-Up>")
        root.unbind("<KeyPress-Down>")
        root.unbind("<KeyPress-Left>")
        root.unbind("<KeyPress-Right>")
        root.unbind("<KeyRelease-Up>")
        root.unbind("<KeyRelease-Down>")
        root.unbind("<KeyRelease-Left>")
        root.unbind("<KeyRelease-Right>")
        root.unbind("<KeyPress-w>")
        root.unbind("<KeyPress-s>")
        root.unbind("<KeyPress-a>")
        root.unbind("<KeyPress-d>")
        root.unbind("<KeyRelease-w>")
        root.unbind("<KeyRelease-s>")
        root.unbind("<KeyRelease-a>")
        root.unbind("<KeyRelease-d>")
        root.unbind("<KeyPress-W>")
        root.unbind("<KeyPress-S>")
        root.unbind("<KeyPress-A>")
        root.unbind("<KeyPress-D>")
        root.unbind("<KeyRelease-W>")
        root.unbind("<KeyRelease-S>")
        root.unbind("<KeyRelease-A>")
        root.unbind("<KeyRelease-D>")
        root.unbind("<KeyPress-space>")
    
    async def lookout_for_new_game_event(self):
        while True:
            await NEW_GAME_EVENT.wait()
            self.x_coord.value = 500
            self.y_coord.value = 500

    def press_up(self, e):
        self.velocity_up = True

    def press_down(self, e):
        self.velocity_down = True

    def press_left(self, e):
        self.velocity_left = True
    
    def press_right(self, e):
        self.velocity_right = True

    def release_up(self, e):
        self.velocity_up = False

    def release_down(self, e):
        self.velocity_down = False
    
    def release_left(self, e):
        self.velocity_left = False

    def release_right(self, e):
        self.velocity_right = False

    async def update_coords_loop(self):
        while True:
            await asyncio.sleep(0.02)
            await GAME.wait()
            if self.velocity_up:
                self.y_coord-=8
            if self.velocity_down:
                self.y_coord+=8
            if self.velocity_left:
                self.x_coord-=8
            if self.velocity_right:
                self.x_coord+=8
            for i in active_asteroids:
                if -80 < self.x_coord.value - i.x_coord < 100 and -80 < self.y_coord.value - i.y_coord.value < 100:
                    asyncio.ensure_future(game_over())
                    break
            canvas.coords(self.object, self.x_coord.value, self.y_coord.value)
    def shoot_laser(self, e):
        if can_i_shoot_laser():
            Laser_Beam()

ship = Ship()