# coding: utf-8
import flask
import hashlib
import sqlite3
import Configure
import Database

def CheckLogin():
    """ ログイン済みかを確認する """
    if 'login' in flask.session and flask.session['login'] == True:
        return True
    return False


def TryRegisterTeam(teamname, teamcode):
    """ チーム登録を試行する """
    if not 4 < len(teamcode) < 32:
        return ('teamcode', 'The length of invitation code must be between 4 and 32')
    try:
        Database.Query(
            "INSERT INTO team(teamname, teamcode) VALUES(?, ?)",
            (teamname, teamcode)
        )
    except sqlite3.IntegrityError, error:
        return ('teamname', 'The teamname is already taken')
    return ('username', '')

def TryRegisterUser(username, password, teamname, teamcode, country):
    """ ユーザー登録を試行する """
    # パスワードのハッシュを取得
    sha256 = hashlib.sha256()
    sha256.update(password)
    password_hash = sha256.hexdigest()
    if teamcode is None:
        # 個人で参加
        try:
            Database.Query(
                "INSERT INTO team(teamname, teamcode, country) VALUES(?, ?, ?)",
                (username, '', country)
            )
            Database.Query(
                "INSERT INTO account(teamname, username, password, country) VALUES(?, ?, ?, ?)",
                (username, username, password_hash, country)
            )
        except sqlite3.IntegrityError:
            return ('username', 'The username is already taken')
    else:
        # チームに参加
        result = Database.Query(
            "SELECT teamname, email FROM team WHERE teamcode=? AND teamname=?",
            (teamcode, teamname)
        )
        if result:
            try:
                Database.Query(
                    "INSERT INTO account(teamname, username, password, country) VALUES(?, ?, ?, ?)",
                    (result[0]['teamname'], username, password_hash, country)
                )
            except sqlite3.IntegrityError:
                return ('username', 'The username is already taken')
        else:
            return ('teamcode', 'Team code is invalid')
    return ('username', '')


def TryLogin(username, password):
    """ ログインを試行する """
    # パスワードのハッシュを取得
    sha256 = hashlib.sha256()
    sha256.update(password)
    password_hash = sha256.hexdigest()
    # クエリ発行
    result = Database.Query(
        "SELECT * FROM account WHERE username=? and password=?",
        (username, password_hash)
    )
    if result:
        return result[0]
    else:
        return None
