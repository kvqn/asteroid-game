import tkinter
import asyncio

from .. import root, GAME

player_name_input_label = tkinter.Label(root, bg = 'black', fg='RoyalBlue3', font = ("LLPixel", 40), text = "PLAYER NAME")

player_name_heading_label = tkinter.Label(root, bg = 'black', fg = 'gold', font = ("LLPixel", 28), text="PLAYING AS", width = 10)

from . import PLAYER_NAME
player_name_input_entry = tkinter.Entry(root, bg = 'black', fg = 'green3', font = ("LLPixel", 22), justify = 'center', textvariable=PLAYER_NAME, width = 12)
player_name_display_label = tkinter.Label(root, bg = 'black', fg = 'white', font = ("LLPixel", 22), textvariable = PLAYER_NAME, justify = 'center', width = 12)

# from ..events import secondary_update_loop, secondary_event_loop


def submit_player_name():
    root.unbind("<Return>")
    player_name_input_label.place_forget()
    player_name_input_entry.place_forget()
    player_name_input_entry.configure(state='disabled')
    player_name_input_submit_button.place_forget()
    player_name_heading_label.place(x=1330, y=600)
    player_name_display_label.place(x=1330, y=700)
    from ..events.start_game import start_game
    asyncio.ensure_future(start_game())
    GAME.set()
    # print('got playername')

def init():
    GAME.clear()
    player_name_input_label.place(x=620, y=200)
    player_name_input_entry.place(x=670, y=300)
    root.bind("<Return>", lambda e : submit_player_name())
    player_name_input_submit_button.place(x=730, y=400)
    # print('getting playername')

player_name_input_submit_button = tkinter.Button(root, activebackground='grey42', bg = 'gray69', font = ("LLPixel", 20), text = "SUBMIT", command = submit_player_name)