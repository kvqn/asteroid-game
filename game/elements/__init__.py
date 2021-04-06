# This file contains all the variables and functions that are used by other files.
# The other files in this folder deal with loading different UI elements

import tkinter


SCORE = tkinter.IntVar(value=0)
LEVEL = tkinter.IntVar(value=1)
PLAYER_NAME = tkinter.StringVar()

import pymysql

conn = pymysql.connect(user='root', password='password', host='localhost', database='asteroidgame')

cur = conn.cursor()
cur.execute("create table if not exists scores(name char(20) unique, score int(3));")
conn.commit()

def save_data():
    if not PLAYER_NAME.get() == '':
        cur.execute(f"""INSERT INTO scores (name, score) VALUES ("{PLAYER_NAME.get()}", {str(SCORE.get())}) ON DUPLICATE KEY UPDATE score=VALUES(score);""")
        conn.commit()

def Init():
    from .bar import init
    init()
    from .highscore import init
    init()
    from .level import init
    init()
    from .score import init
    init()
    from .timer import init
    init()
    from .playername import init
    init()

