# coding: utf-8
import flask
import sqlite3
import datetime
import Database

def GetRecentLog(n=20):
    """解答ログを取得する"""
    result = Database.Query(
        "SELECT * FROM log ORDER BY timestamp DESC LIMIT ?",
        (n,)
    )
    return result

def AddPoint(cid, chall, teamname, username):
    """加点する"""
    Database.Query(
        "UPDATE team SET score=score+?,lastlog=?,solved=solved||? WHERE teamname=?",
        (chall['score'], datetime.datetime.now(), str(cid)+',', teamname)
    )
    Database.Query(
        "UPDATE challenge SET solved=solved+1 WHERE id=?",
        (cid,)
    )
    Database.Query(
        "INSERT INTO log(title, teamname, username, score) VALUES(?, ?, ?, ?)",
        (chall['title'], teamname, username, chall['score'])
    )


def GetAllChallenges():
    """全ての問題を取得する"""
    challs = Database.Query(
        "SELECT * FROM challenge ORDER BY category"
    )
    return challs


def GetChallenge(cid):
    """問題情報を取得する"""
    chall = Database.Query(
        "SELECT * FROM challenge WHERE id=?",
        (cid,)
    )
    if chall:
        return chall[0]
    else:
        return None


def GetSolved(teamname):
    """解答済みの問題を取得する"""
    solved = Database.Query(
        "SELECT solved FROM team WHERE teamname=?",
        (teamname,)
    )
    solved_list = []
    if solved:
        for i in solved[0]['solved'].split(','):
            try:
                solved_list.append(int(i))
            except:
                pass
    return solved_list


def IsSolved(cid, teamname):
    """ユーザーが解答済みかを確認する"""
    if cid in GetSolved(teamname):
        return True
    else:
        return False

