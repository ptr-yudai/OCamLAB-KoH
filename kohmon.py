#!/usr/bin/env python
# coding: utf-8
import config
import time
import datetime
import sqlite3
import string
import random
import json
from contextlib import closing

sqlite3.register_adapter(list, lambda l: ';'.join(map(str, l)))
sqlite3.register_converter('LIST', lambda s: map(int, s.split(';')))

def checkToken():
    with open(config.tokenpath, 'r') as f:
        token_list = json.load(f)
    for script in config.scripts:
        try:
            tokens = script()
            for token in tokens:
                for team in token_list:
                    if token == token_list[team]:
                        addPoint(team, 10)
                        break
        except Exception, e:
            print("[ERROR]", e)
            
def addPoint(team, pt):
    with closing(sqlite3.connect(config.dbpath)) as conn:
        c = conn.cursor()
        c.execute(u"UPDATE account SET score=score+? WHERE username=?", (pt, team))
        print("Additional " + str(pt) + "pt to " + team)
        conn.commit()

def updateToken():
    table = string.ascii_letters + '0123456789'
    token_list = {}
    with closing(sqlite3.connect(config.dbpath)) as conn:
        c = conn.cursor()
        result = c.execute(u"SELECT username FROM account")
        for team in result:
            token = 'token-' + ''.join([random.choice(table) for i in range(32)])
            token_list[team[0]] = token
    with open(config.tokenpath, 'w') as f:
        json.dump(token_list, f)

while True:
    now = datetime.datetime.now()
    if now.minute % 5 == 0 and now.second == 0:
        print("***** Check Time! *****")
        checkToken()
        updateToken()
        time.sleep(60 * 4)
    time.sleep(1)
