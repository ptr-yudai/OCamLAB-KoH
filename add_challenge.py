import sqlite3
import config
from contextlib import closing

title = 'BoF'
problem = "nc 192.168.205.1"
score = 200
category = 'pwn'
flag = "flag-hogehogehogehogehugahugahugahuga"

sqlite3.register_adapter(list, lambda l: ';'.join(map(str, l)))
sqlite3.register_converter('LIST', lambda s: map(int, s.split(';')))
with closing(sqlite3.connect(config.dbpath)) as conn:
    c = conn.cursor()
    c.execute(
        "INSERT INTO challenge(title, problem, score, category, flag) VALUES(?, ?, ?, ?, ?)",
        (title, problem, score, category, flag)
    )
    conn.commit()
