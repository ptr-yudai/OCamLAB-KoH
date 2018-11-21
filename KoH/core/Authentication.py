# coding: utf-8
import flask
import hashlib
import Configure
import Database

def CheckLogin():
    """ ログイン済みかを確認する """
    if 'login' in flask.session and flask.session['login'] == True:
        return True
    return False


def TryRegisterUser():
    """ ユーザー登録を試行する """
    return


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
    return result
