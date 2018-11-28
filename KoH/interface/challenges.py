# coding: utf-8
import flask
from KoH import app
from KoH.core import CTF
from KoH.core import Authentication
from KoH.core import Database
from KoH.core import DatetimeManager
from KoH.core import SiteManager
from KoH.core import Challenge

@app.route("/challenges")
def challenges():
    """ 問題一覧 """
    ctf = CTF.GetInformation()
    # ログイン済み
    if not Authentication.CheckLogin():
        SiteManager.SetReferer('challenges')
        return SiteManager.JumpToPage('login')
    # 問題一覧取得
    challs = Challenge.GetAllChallenges()
    solved = Challenge.GetSolved(flask.session['teamname'])
    # 開催中か
    running = DatetimeManager.CheckDuration()
    # サイトを表示する
    return flask.render_template(
        'challenges.html',
        ctf = ctf,
        running = running,
        challs = challs,
        solved = solved
    )
