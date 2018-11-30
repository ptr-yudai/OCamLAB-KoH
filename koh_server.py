#!/usr/bin/env python
# coding: utf-8
import importlib
import time
import datetime
import glob
import threading
from KoH.core import Configure
from KoH.core import Database
from KoH.core import Token

def AddPoint(teamname, title, score):
    """防御点を追加する"""
    Database.Query(
        "UPDATE team SET score=score+?, lastlog=? WHERE teamname=?",
        (score, datetime.datetime.now(), teamname)
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
    path = config['koh']['path']
    # トークン取得
    new_tokens = Token.NewTokens()
    old_tokens = Token.GetTokens(path)
    print("[+] Checking defense points ({0})".format(datetime.datetime.now()))
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
        print(token_list)
        for token in token_list:
            for teamname in old_tokens:
                if token == old_tokens[teamname]:
                    # 加点
                    AddPoint(teamname, title, score)
    # トークン上書き
    Token.UpdateTokens(new_tokens, path)

    
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
