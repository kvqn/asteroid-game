import tkinter
from PIL import Image, ImageTk
from os import system
import asyncio
from random import randint, choice
import pickle
from time import time as currentTime

root = tkinter.Tk()
root.geometry("1600x1000")
root.resizable(width=False, height=False)
root.configure(bg='black')



def Get_Image(file):
    return ImageTk.PhotoImage(Image.open(file))

ship_image = Get_Image("assets/ship_final.png")

laser_image = Get_Image("assets/beam.png")

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

bar_images = [
    Get_Image("assets/bar/bar_0.png"),
    Get_Image("assets/bar/bar_1.png"),
    Get_Image("assets/bar/bar_2.png"),
    Get_Image("assets/bar/bar_3.png"),
    Get_Image("assets/bar/bar_4.png")
]

bar_canvas = tkinter.Canvas(root, width = 400, height = 61, bg='black', highlightthickness=0)

NEW_TICK_EVENT = asyncio.Event()
NEW_GAME_EVENT = asyncio.Event()

class Tick_Wait_Request_Manager:
    def __init__(self):
        self.requests = 0
    
    def acquire(self):
        self.requests+=1
    
    def release(self):
        self.requests-=1
        if self.requests == 0:
            NEW_TICK_EVENT.set()
            NEW_TICK_EVENT.clear()
            
TICK_REQUESTS = Tick_Wait_Request_Manager()

async def MaxTickSpeedManager():
    while True:
        await NEW_TICK_EVENT.wait()
        TICK_REQUESTS.acquire()
        try:
            await asyncio.sleep(0.01)
        finally:
            TICK_REQUESTS.release()

level_up_image = Get_Image("assets/level_up.png")

class AsteroidGenerationLoop():
    def __init__(self):
        self.level = tkinter.IntVar(root, 1)
        self.delay_in_seconds = 1
    
    def level_up(self):
        level = self.level.get()
        level+=1
        self.level.set(level)
        self.delay_in_seconds = self.delay_in_seconds*0.7
        asyncio.ensure_future(create_image_animated_effect(x=300, y=300, image_object=level_up_image, small_tick_delay=10, big_tick_delay=100))

    def level_reset(self):
        self.level.set(1)
        self.delay_in_seconds = 1
    
    async def coro(self):
        while True:
            await asyncio.sleep(1)
            await NEW_TICK_EVENT.wait()
            TICK_REQUESTS.acquire()
            try:
                Asteroid()
            finally:
                TICK_REQUESTS.release()

AsteroidGenerationLoop = AsteroidGenerationLoop()

class OutOfBounds(Exception):
    pass

class RangedInteger:
    def __init__(self, min, max, value, raise_border_exceptions = False):
        self.min = min
        self.max = max
        self.value = value
        self.flag = raise_border_exceptions
    
    def __add__(self, val):
        if self.min <= self.value + val <= self.max:
            self.value += val
        elif self.flag:
            raise OutOfBounds
        return self
            

    def __iadd__(self, val):
        if self.min <= self.value + val <= self.max:
            self.value += val
        elif self.flag:
            raise OutOfBounds
        return self
        
    def __sub__(self, val):
        if self.min <= self.value - val <= self.max:
            self.value -= val
        elif self.flag:
            raise OutOfBounds
        return self
    
    def __isub__(self, val):
        if self.min <= self.value - val <= self.max:
            self.value -= val
        elif self.flag:
            raise OutOfBounds
        return self
        
class Ship:
    def __init__(self):
        self.object = canvas.create_image(500,500, anchor='nw', image = ship_image)
        self.x_coord = RangedInteger(min=0, max=900 ,value=500)
        self.y_coord = RangedInteger(min=0, max=750 ,value=500)
        self.velocity_up = False
        self.velocity_down = False
        self.velocity_left = False
        self.velocity_right = False
        self.is_game_over = False
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
        root.bind("<KeyPress-space>", lambda e : asyncio.ensure_future(self.shoot_laser()))
        self.update_coro = asyncio.ensure_future(self.update_coords_loop())
        asyncio.ensure_future(self.lookout_for_new_game_event())
        # print("ship initialised")

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
        await NEW_GAME_EVENT.wait()
        self.update_coro.cancel()

    def press_up(self, event):
        self.velocity_up = True

    def press_down(self, event):
        self.velocity_down = True

    def press_left(self, event):
        self.velocity_left = True
    
    def press_right(self, event):
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
        # print("test2")
        while True:
            await NEW_TICK_EVENT.wait()
            TICK_REQUESTS.acquire()
            try:
                if self.velocity_up:
                    self.y_coord-=5
                if self.velocity_down:
                    self.y_coord+=5
                if self.velocity_left:
                    self.x_coord-=5
                if self.velocity_right:
                    self.x_coord+=5
                for i in active_asteroids:
                    if -80 < self.x_coord.value - i.x_coord < 100 and -80 < self.y_coord.value - i.y_coord.value < 100:
                        if not self.is_game_over:
                            self.is_game_over = True
                            asyncio.ensure_future(GAME_OVER())
                canvas.coords(self.object, self.x_coord.value, self.y_coord.value)
            finally:
                TICK_REQUESTS.release()

    async def shoot_laser(self):
        if bar_update.can_i_shoot_laser():
            await NEW_TICK_EVENT.wait()
            TICK_REQUESTS.acquire()
            try:
                Laser_Beam()
            finally:
                TICK_REQUESTS.release()



class Laser_Beam:
    def __init__(self):
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
            ticks = (self.y_coord.value - j.y_coord.value)//15
            asyncio.ensure_future(self.queue_detonation(ticks))
            asyncio.ensure_future(j.queue_detonation(ticks))
            active_asteroids.remove(j)
        else:
            active_beams.add(self)
        self.update_coro = asyncio.ensure_future(self.update_coords())
        self.lookout_coro = asyncio.ensure_future(self.lookout_for_new_game_event())
    
    async def lookout_for_new_game_event(self):
        await NEW_GAME_EVENT.wait()
        self.update_coro.cancel()
    
    async def queue_detonation(self, ticks):
        for _ in range(ticks):
            await NEW_TICK_EVENT.wait()
        canvas.delete(self.object)
        self.update_coro.cancel()
        self.lookout_coro.cancel()
        # print("detonated laser.")
    
    async def update_coords(self):
        try:
            while True:
                await NEW_TICK_EVENT.wait()
                TICK_REQUESTS.acquire()
                try:
                    self.y_coord -= 10
                    canvas.coords(self.object, self.x_coord, self.y_coord.value)
                finally:
                    TICK_REQUESTS.release()
        except OutOfBounds:
            canvas.delete(self.object)
            try:
                active_beams.remove(self)
            except KeyError:
                pass
            # print("Destroyed laser.")
            self.update_coro.cancel()
            self.lookout_coro.cancel()


class Asteroid:
    def __init__(self):
        self.x_coord = randint(80, 800)
        self.y_coord = RangedInteger(min=-300, max=1200, value=-200, raise_border_exceptions=True)
        self.object = canvas.create_image(self.x_coord, -200, anchor = 'nw', image = choice(asteroid_images))
        j = None
        for i in active_beams:
            if self.x_coord <= i.x_coord <= self.x_coord+120 and i.y_coord.value > self.y_coord.value:
                try:
                    if i.y_coord.value < j.y_coord.value :
                        j = i
                except AttributeError:
                    j = i
        if j:
            ticks = (j.y_coord.value - self.y_coord.value)//15
            asyncio.ensure_future(self.queue_detonation(ticks))
            asyncio.ensure_future(j.queue_detonation(ticks))
            active_beams.remove(j)
        else:
            active_asteroids.add(self)
        self.update_coro = asyncio.ensure_future(self.update_coords())
        self.lookout_coro = asyncio.ensure_future(self.lookout_for_new_game_event())

    async def lookout_for_new_game_event(self):
        await NEW_GAME_EVENT.wait()
        self.update_coro.cancel()

    async def update_coords(self):
        try:
            while True:
                await NEW_TICK_EVENT.wait()
                TICK_REQUESTS.acquire()
                try:
                    self.y_coord += 5
                    canvas.coords(self.object, self.x_coord, self.y_coord.value)
                finally:
                    TICK_REQUESTS.release()
        except OutOfBounds:
            canvas.delete(self.object)
            try:
                active_asteroids.remove(self)
            except KeyError:
                pass
            # print("Destroyed Asteroid.")
            self.update_coro.cancel()
            self.lookout_coro.cancel()

    
    async def queue_detonation(self, ticks):
        for _ in range(ticks):
            await NEW_TICK_EVENT.wait()
        # Loading destroy animation
        SCORE.set(SCORE.get()+1)
        self.explosion_images = iter(explosion_images)
        self.x_coord -= 40
        self.y_coord -= 40
        try:
            while True:
                canvas.delete(self.object)
                self.object = canvas.create_image(self.x_coord, self.y_coord.value, anchor = 'nw', image = next(self.explosion_images))
                for _ in range(10):
                    await NEW_TICK_EVENT.wait()

        except StopIteration:
            self.update_coro.cancel()
            self.lookout_coro.cancel()
            canvas.delete(self.object)
            # print("Asteroid exploded")
        





def SAVE_AND_QUIT():
    arbitrary_update_loop.stop()
    if not PLAYER_NAME in DATA.highscores or SCORE.get() > DATA.highscores[PLAYER_NAME]:
            DATA.highscores[PLAYER_NAME] = SCORE.get()
            with open("save.dat", 'wb') as file:
                pickle.dump(DATA, file)
    loop.stop()
    root.destroy()

    # quit_without_saving_button.place_forget()

#
# Pause Screen
#


pause_transparent_background_image = Get_Image("assets/50gray.png")
# save_quit_image = Get_Image("assets/savequit.png")
save_quit_button = tkinter.Button(root, activebackground="gray42", bg = "gray69", font = ("LLPixel", 20), text = "SAVE AND QUIT", command = SAVE_AND_QUIT, width = 20)
# quit_without_saving_button = tkinter.Button(root, activebackground="gray42", bg = "gray69", font = ("LLPixel", 20), text = "QUIT WITHOUT SAVING", command = QUIT_WITHOUT_SAVING, width = 20)

class arbitrary_update_loop:
    def __init__(self):
        self.is_on = False
    
    def start(self):
        asyncio.ensure_future(self.loop())
        self.is_on = True
    
    def stop(self):
        self.is_on = False
    
    async def loop(self):
        while True:
            await asyncio.sleep(0.01)
            if not self.is_on:
                break
            root.update()

arbitrary_update_loop = arbitrary_update_loop()


def PAUSE_GAME(e):
    # print("pausing")
    # await NEW_TICK_EVENT.wait()
    TICK_REQUESTS.acquire()
    #b = canvas.create_image(-100, -100, anchor = 'nw', image = pause_transparent_background_image)
    save_quit_button.place(x=650, y=450)
    save_quit_button.lift()
    # quit_without_saving_button.place(x=650, y=500)
    # quit_without_saving_button.lift()
    root.bind("<Escape>", RESUME_GAME)
    arbitrary_update_loop.start()

def RESUME_GAME(e):
    try:
        # print("resuming")
        #canvas.delete(b)
        arbitrary_update_loop.stop()
        save_quit_button.place_forget()
        # quit_without_saving_button.place_forget()
        root.bind("<Escape>", PAUSE_GAME)
    finally:
        TICK_REQUESTS.release()


def create_namespace():
    global canvas
    canvas = tkinter.Canvas(root, width = 1000, height = 800, bg = 'black')
    global active_asteroids
    active_asteroids = set()
    global active_beams
    active_beams = set()
    global ship
    ship = Ship()

async def START_GAME():
    # print(TICK_REQUESTS.requests)
    await NEW_TICK_EVENT.wait()
    # print("vbdfhv dfb")
    global time_object
    time_object = currentTime()
    canvas.place(x=300,y=100)
    root.lift(canvas)
    root.bind("<Escape>", PAUSE_GAME)
    

async def main_update_loop():
    while True:
        await NEW_TICK_EVENT.wait()
        TICK_REQUESTS.acquire()
        try:
            root.update()
        finally:
            TICK_REQUESTS.release()

class SavedData:
    def __init__(self):
        self.highscores = dict()

#
# Right side
#

ScoreHeadingLabel = tkinter.Label(root, bg='black',fg="gold", font=("LLPixel",32), text="SCORE")
SCORE = tkinter.IntVar()
SCORE.set(0)
ScoreLabel = tkinter.Label(root, bg="black", fg="white", font=("LLPixel",28), textvariable=SCORE, width=5)

#
# Left side
#

HighscoreHeadingLabel = tkinter.Label(root, bg='black', fg='gold', font=("LLPixel", 32), text="HIGHSCORES")

try:
    with open("save.dat", 'rb') as file:
        DATA = pickle.load(file)
    if not isinstance(DATA, SavedData):
        DATA = SavedData()
except FileNotFoundError:
    DATA = SavedData()
except EOFError:
    DATA = SavedData()


#
# Game Over screen
#

async def game_over_retry():
    try:
        if not PLAYER_NAME in DATA.highscores or SCORE.get() > DATA.highscores[PLAYER_NAME]:
            DATA.highscores[PLAYER_NAME] = SCORE.get()
            with open("save.dat", 'wb') as file:
                pickle.dump(DATA, file)
            evaluate_highscores()
        arbitrary_update_loop.stop() 
        SCORE.set(0)
        ship.unbind()
        canvas.place_forget()
        canvas.destroy()
        # print("oof1")
        game_over_button1.place_forget()
        game_over_button2.place_forget()
        # print("oof2")
    finally:
        TICK_REQUESTS.release()
    # await asyncio.gather(*asyncio())
    NEW_GAME_EVENT.set()
    NEW_GAME_EVENT.clear()
    # print('vdv')
    create_namespace()
    bar_update.bar_x = 10
    asyncio.ensure_future(START_GAME())
    # TICK_REQUESTS.release()
    # loop.run_forever()
    

def game_over_exit():
    if not PLAYER_NAME in DATA.highscores or SCORE.get() > DATA.highscores[PLAYER_NAME]:
        DATA.highscores[PLAYER_NAME] = SCORE.get()
        with open("save.dat", 'wb') as file:
            pickle.dump(DATA, file)
    arbitrary_update_loop.stop()
    loop.stop()
    root.destroy()
    

game_over_image = Get_Image("assets/game_over.png")
game_over_button1 = tkinter.Button(root, activebackground='gray42', bg='gray69', fg='black', font=("LLPixel", 20), text="RETRY", command = lambda : asyncio.ensure_future(game_over_retry()))
game_over_button2 = tkinter.Button(root, activebackground='gray42', bg='gray69', fg='black', font=("LLPixel", 20), text="EXIT", command = game_over_exit)

async def GAME_OVER():
    await NEW_TICK_EVENT.wait()
    TICK_REQUESTS.acquire()
    root.unbind("<Escape>")
    canvas.create_image(143, 300,anchor='nw', image=game_over_image)
    game_over_button1.place(x=643, y=540)
    game_over_button1.lift()
    game_over_button2.place(x=843, y=540)
    game_over_button2.lift()
    arbitrary_update_loop.start()


def submit_player_name():
    try:
        root.unbind("<Return>")
        player_name_input_label.place_forget()
        player_name_input_entry.place_forget()
        player_name_input_entry.configure(state='disabled')
        player_name_input_submit_button.place_forget()
        player_name_heading_label.place(x=1320, y=600)
        player_name_display_label.place(x=1310, y=700)
        global PLAYER_NAME
        PLAYER_NAME = PLAYER_NAME.get()
    finally:
        TICK_REQUESTS.release()

player_name_input_label = tkinter.Label(root, bg = 'black', fg='RoyalBlue3', font = ("LLPixel", 40), text = "PLAYER NAME")
PLAYER_NAME = tkinter.StringVar()
player_name_input_entry = tkinter.Entry(root, bg = 'black', fg = 'green3', font = ("LLPixel", 22), justify = 'center', textvariable=PLAYER_NAME, width = 12)
player_name_input_submit_button = tkinter.Button(root, activebackground='grey42', bg = 'gray69', font = ("LLPixel", 20), text = "SUBMIT", command = submit_player_name)

player_name_heading_label = tkinter.Label(root, bg = 'black', fg = 'gold', font = ("LLPixel", 28), text="PLAYING AS", width = 10)
player_name_display_label = tkinter.Label(root, bg = 'black', fg = 'white', font = ("LLPixel", 22), textvariable = PLAYER_NAME, justify = 'center', width = 12)

HighscoreLabels = []

def evaluate_highscores():
    HIGHSCORES = list(DATA.highscores.items())
    HIGHSCORES.sort(reverse=True, key= lambda e : e[1])
    global HighscoreLabels
    if HighscoreLabels:
        for _ in HighscoreLabels:
            _.place_forget()
    HighscoreLabels = []
    _ = 0
    for i in HIGHSCORES:
        _+=1
        label = tkinter.Label(root, bg="black", fg="white", font=("LLPixel",16), text=i[0], width = 10)
        label.place(x=10, y=100+_*50)
        HighscoreLabels.append(label)
        label = tkinter.Label(root, bg="black", fg="white", font=("LLPixel",16), text=str(i[1]), width=5)
        label.place(x=200, y=100+_*50)
        HighscoreLabels.append(label)
        if _ ==5 :
            break

time_stringvar = tkinter.StringVar()
time_stringvar.set('00:00')
Timer_Label = tkinter.Label(root, bg = 'black', fg = 'white', font = ("LLPixel", 32), textvariable = time_stringvar)

async def timer_update():
    while True:
        await asyncio.sleep(1)
        await NEW_TICK_EVENT.wait()
        TICK_REQUESTS.acquire()
        mins, secs = divmod(int(currentTime() - time_object), 60)
        time_stringvar.set('{:02d}:{:02d}'.format(mins, secs))
        if mins*2 + secs/30 >= AsteroidGenerationLoop.level.get():
            AsteroidGenerationLoop.level_up()
        TICK_REQUESTS.release()

async def timer_correction_new_game():
    while True:
        await NEW_GAME_EVENT.wait()
        time_stringvar.set("00:00")
        AsteroidGenerationLoop.level_reset()


class bar_update:
    def __init__(self):
        self.bar_x = 10
        self.bar_state = 0
        self.background_image = bar_canvas.create_rectangle(10,10, self.bar_x, 51, fill="red")
        self.main_image = bar_canvas.create_image(0,0, anchor='nw', image=bar_images[0])
        asyncio.ensure_future(self.coro())

    def can_i_shoot_laser(self):
        if self.bar_state > 0:
            self.bar_x-=95
            return True
        return False

    async def coro(self):
        while True:
            await NEW_TICK_EVENT.wait()
            if self.bar_x < 390:
                TICK_REQUESTS.acquire()
                self.bar_x+=0.75
                bar_canvas.coords(self.background_image, 10,10, self.bar_x, 51)
                state = 0
                if self.bar_x > 390:
                    state = 4
                elif self.bar_x > 295:
                    state = 3
                elif self.bar_x > 200:
                    state = 2
                elif self.bar_x > 105:
                    state = 1
                if not state == self.bar_state:
                    self.bar_state = state
                    bar_canvas.itemconfig(self.main_image, image = bar_images[state])
                TICK_REQUESTS.release()

bar_update = bar_update()

level_heading_label = tkinter.Label(root, bg = 'black', fg = 'gold', font = ("LLPixel", 32), text = "LEVEL")
level_indicator_label = tkinter.Label(root, bg = 'black', fg = 'white', font = ("LLPixel", 72), textvariable = AsteroidGenerationLoop.level)

async def create_image_animated_effect(x, y, image_object, small_tick_delay, big_tick_delay):
    await NEW_TICK_EVENT.wait()
    TICK_REQUESTS.acquire()
    tag = canvas.create_image(x, y, anchor = 'nw', image = image_object)
    TICK_REQUESTS.release()
    for _ in range(small_tick_delay):
        await NEW_TICK_EVENT.wait()
    TICK_REQUESTS.acquire()
    canvas.delete(tag)
    TICK_REQUESTS.release()
    for _ in range(small_tick_delay):
        await NEW_TICK_EVENT.wait()
    TICK_REQUESTS.acquire()
    tag = canvas.create_image(x, y, anchor = 'nw', image = image_object)
    TICK_REQUESTS.release()
    for _ in range(small_tick_delay):
        await NEW_TICK_EVENT.wait()
    TICK_REQUESTS.acquire()
    canvas.delete(tag)
    TICK_REQUESTS.release()
    for _ in range(small_tick_delay):
        await NEW_TICK_EVENT.wait()
    TICK_REQUESTS.acquire()
    tag = canvas.create_image(x, y, anchor = 'nw', image = image_object)
    TICK_REQUESTS.release()

    for _ in range(big_tick_delay):
        await NEW_TICK_EVENT.wait()
    
    TICK_REQUESTS.acquire()
    canvas.delete(tag)
    TICK_REQUESTS.release()
    for _ in range(small_tick_delay):
        await NEW_TICK_EVENT.wait()
    TICK_REQUESTS.acquire()
    tag = canvas.create_image(x, y, anchor = 'nw', image = image_object)
    TICK_REQUESTS.release()
    for _ in range(small_tick_delay):
        await NEW_TICK_EVENT.wait()
    TICK_REQUESTS.acquire()
    canvas.delete(tag)
    TICK_REQUESTS.release()
    for _ in range(small_tick_delay):
        await NEW_TICK_EVENT.wait()
    TICK_REQUESTS.acquire()
    tag = canvas.create_image(x, y, anchor = 'nw', image = image_object)
    TICK_REQUESTS.release()
    for _ in range(small_tick_delay):
        await NEW_TICK_EVENT.wait()
    TICK_REQUESTS.acquire()
    canvas.delete(tag)
    TICK_REQUESTS.release()




def START_WINDOW():
    TICK_REQUESTS.acquire()
    ScoreHeadingLabel.place(x=1360, y=90)
    ScoreLabel.place(x=1370, y=150)
    HighscoreHeadingLabel.place(x=10, y=90)
    Timer_Label.place(x=400, y = 920)
    bar_canvas.place(x=800, y=920)
    level_heading_label.place(x=80, y=500)
    level_indicator_label.place(x=110, y=550)
    evaluate_highscores()
    player_name_input_label.place(x=620, y=200)
    player_name_input_entry.place(x=670, y=300)
    root.bind("<Return>", lambda e : submit_player_name())
    player_name_input_submit_button.place(x=730, y=400)
    arbitrary_update_loop.start()
    create_namespace()
    asyncio.ensure_future(MaxTickSpeedManager())
    asyncio.ensure_future(AsteroidGenerationLoop.coro())
    asyncio.ensure_future(main_update_loop())
    asyncio.ensure_future(timer_update())
    asyncio.ensure_future(timer_correction_new_game())
    asyncio.ensure_future(START_GAME())
    asyncio.ensure_future(GAME_OVER())








loop = asyncio.get_event_loop()
asyncio.ensure_future(START_WINDOW())
loop.run_forever()


# tkinter.Label(master, bg, fg, font, text)
# tkinter.Entry(master, bg, fg, bd, font, justify, width)
# tkinter.Frame(master, bg, bd, height, width)
# tkinter.Button(master, activebackground, bg, fg, font, text, command)

# https://www.youtube.com/watch?v=L3RyxVOLjz8
# https://stackoverflow.com/questions/32289175/list-of-all-tkinter-events

