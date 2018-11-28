#!/usr/bin/env python
# coding: utf-8
import importlib
import time
import datetime
import glob
import threading
import string
import random
import json
from KoH.core import Configure
from KoH.core import Database

def NewTokens():
    """新しいトークンを生成する"""
    teamlist = Database.Query(
        "SELECT teamname FROM team"
    )
    data = {}
    table = string.ascii_letters + "0123456789"
    for team in teamlist:
        token = "token-" + ''.join(random.choice(table) for i in range(32))
        data[team['teamname']] = token
    return data


def GetTokens(path):
    """古いトークンを取得する"""
    try:
        with open(path) as f:
            data = json.load(f)
    except:
        return {}
    return data


def UpdateTokens(data, path):
    """既存のトークンを上書きする"""
    with open(path, 'w') as f:
        json.dump(data, f)


def AddPoint(teamname, title, score):
    """防御点を追加する"""
    Database.Query(
        "UPDATE team SET score=score+?, lastlog=? WHERE teamname=?",
        (score, datatime.datetime.now(), teamname)
    )
    Database.Query(
        "INSERT INTO log(title, teamname, username, score) VALUES(?, ?, ?, ?)",
        (title, teamname, teamname, score)
    )
    print("[*] {0}pt --> {1} [{2}]".format(score, teamname, title))

        
def CheckDefense():
    """防御点を確認する"""
    config = Configure.LoadConfig()
    score = config['koh']['score']
    path = 'tokens.json'
    # トークン取得
    new_tokens = NewTokens()
    old_tokens = GetTokens(path)
    print("[+] Checking defense points...")
    # 各問題のトークンの調査
    for module in glob.glob("scripts/*.py"):
        module = module.replace("/", ".")[:-3]
        mod = importlib.import_module(module)
        try:
            mod_tokens = getattr(mod, "tokens")
            mod_title  = getattr(mod, "title")
            token_list = mod_tokens(new_tokens)
            title      = mod_title()
        except Exception, e:
            print("[-] Error in {0}".format(mod))
            print(e)
            continue
        for token in token_list:
            for teamname in old_tokens:
                if token == old_tokens[teamname]:
                    # 加点
                    AddPoint(teamname, title, score)
    # トークン上書き
    UpdateTokens(new_tokens, path)

    
if __name__ == '__main__':
    config = Configure.LoadConfig()
    interval = config['koh']['interval']
    if interval <= 0:
        print("[-] Invalid interval")
        exit(1)
    # スケジューラの起動
    base_time = time.time()
    while True:
        t = threading.Thread(target=CheckDefense)
        t.start()
        next_time = ((base_time - time.time()) % interval) or interval
        time.sleep(next_time)
