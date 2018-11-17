import sqlite3
import config
from contextlib import closing

#title = 'ziplist'
#problem = 'http://ocamlab.jp:4214/<br><a href="/static/challs/ziplist.zip">ziplist.zip</a>'
#score = 300
#category = 'KoH'
#flag = "flag-hogehogehogehogehugahugahugahuga"

title = 'sample'
problem = 'This is a <strong>sample</strong> problem.'
score = 100
category = 'misc'
flag = "flag-hogehogehogehogehugahugahugahuga"

with closing(sqlite3.connect(config.dbpath)) as conn:
    c = conn.cursor()
    c.execute(
        "INSERT INTO challenge(title, problem, score, category, flag) VALUES(?, ?, ?, ?, ?)",
        (title, problem, score, category, flag)
    )
    conn.commit()
