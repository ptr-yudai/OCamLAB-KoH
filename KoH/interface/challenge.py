# coding: utf-8
import flask
from KoH import app
from KoH.core import CTF
from KoH.core import Authentication
from KoH.core import Database
from KoH.core import DatetimeManager
from KoH.core import SiteManager
from KoH.core import Challenge

@app.route("/challenge", methods=['GET', 'POST'])
def challenge():
    """ 問題一覧 """
    ctf = CTF.GetInformation()
    message = ''
    status = 0
    # ログイン済み
    if not Authentication.CheckLogin():
        SiteManager.SetReferer('challenges')
        return SiteManager.JumpToPage('login')
    # 問題番号取得
    cid = flask.request.args.get('id', -1, type=int)
    # 問題取得
    chall = Challenge.GetChallenge(cid)
    if chall is None:
        return SiteManager.JumpToPage('challenges')
    # 開催中か
    running = DatetimeManager.CheckDuration()
    if running == 1:
        return SiteManager.JumpToPage('challenges')
    elif running == 2 and ctf['over-open'] is False:
        return SiteManager.JumpToPage('challenges')
    # フラグ投稿
    if flask.request.method == 'POST' and 'flag' in flask.request.form:
        flag = flask.request.form['flag'].strip()
        if flag == chall['flag']:
            message = 'The flag is correct.'
            status = 1
            if running == 0:
                # 加点
                if Challenge.IsSolved(cid, flask.session['teamname']):
                    message += ' (You have already solved this challenge.)'
                    status = 2
                else:
                    Challenge.AddPoint(cid, chall, flask.session['teamname'], flask.session['username'])
            else:
                # 終了表示
                message += " (The CTF is over.)"
                status = 2
        else:
            message = 'The flag is wrong.'
            if running == 2:
                # 終了表示
                message += " (The CTF is over.)"
                status = 2
    # サイトを表示する
    return flask.render_template(
        'challenge.tmpl',
        ctf = ctf,
        chall = chall,
        status = status,
        message = message
    )
