# coding: utf-8
import json
import os
import os.path
import sqlite3
from contextlib import closing
import Database

def LoadConfig():
    """ 設定ファイルを読み込む """
    cd = os.path.dirname(__file__)
    config_path = os.path.join(cd, "../../config.json")
    try:
        f = open(config_path, "r")
        config = json.load(f)
        if config['server']['secret'] == '':
            config['server']['secret'] = os.urandom(24)
        elif len(config['server']['secret']) != 24:
            print("[-] config.json: server->secret must be 24 bytes long.")
            exit(1)
        return config
    except IOError:
        print("[-] config.json: File not found")
        exit(1)
    except ValueError:
        print("[-] config.json: Invalid JSON syntax")
        exit(1)


def GetDatabasePath():
    """ データベースのパスを返す """
    cd = os.path.dirname(__file__)
    db_path = os.path.join(cd, "../../database.db")
    return os.path.normpath(db_path)
        

def InitializeDatabase():
    """ データベースを初期化する """
    # accountテーブルの作成
    res = Database.Query("SELECT name FROM sqlite_master WHERE type='table' AND name='account'")
    if not res:
        create_table = """
        CREATE TABLE account(
        id       INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        teamname CHAR(32) NOT NULL,
        usericon BLOB,
        username CHAR(32) NOT NULL UNIQUE,
        password CHAR(128) NOT NULL,
        country  CHAR(64) NOT NULL
        )
        """
        Database.Query(create_table)
        print("[+] `account` table is created")
    # teamテーブルの作成
    res = Database.Query("SELECT name FROM sqlite_master WHERE type='table' AND name='team'")
    if not res:
        create_table = """
        CREATE TABLE team(
        id       INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        teamname CHAR(32) NOT NULL UNIQUE,
        teamcode CHAR(64) NOT NULL,
        teamicon BLOB,
        country  CHAR(64) NOT NULL DEFAULT '',
        score    INTEGER NOT NULL DEFAULT 0,
        solved   TEXT DEFAULT '',
        lastlog  TIMESTAMP DEFAULT (DATETIME('now','localtime'))
        )
        """
        Database.Query(create_table)
        print("[+] `team` table is created")
    # challengeテーブルの作成
    res = Database.Query("SELECT name FROM sqlite_master WHERE type='table' AND name='challenge'")
    if not res:
        create_table = """
        CREATE TABLE challenge(
        id       INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        title    CHAR(128) NOT NULL UNIQUE,
        problem  TEXT NOT NULL,
        score    INT NOT NULL,
        category CHAR(32) NOT NULL,
        flag     CHAR(64) NOT NULL,
        solved   INT NOT NULL DEFAULT 0
        )
        """
        Database.Query(create_table)
        print("[+] `challenge` table is created")
    # logテーブルの作成
    res = Database.Query("SELECT name FROM sqlite_master WHERE type='table' AND name='log'")
    if not res:
        create_table = """
        CREATE TABLE log(
        id        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        timestamp TIMESTAMP DEFAULT (DATETIME('now','localtime')),
        title     CHAR(128) NOT NULL,
        teamname  CHAR(64) NOT NULL,
        username  CHAR(64) NOT NULL,
        score     INT NOT NULL
        )
        """
        Database.Query(create_table)
        print("[+] `log` table is created")
