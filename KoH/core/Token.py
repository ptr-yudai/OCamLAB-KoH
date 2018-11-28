# coding: utf-8
import string
import random
import json
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
