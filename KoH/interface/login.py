# coding: utf-8
import flask
from KoH import app
from KoH.core import CTF
from KoH.core import Authentication
from KoH.core import SiteManager

@app.route("/login", methods=['GET', 'POST'])
def login():
    """ ログイン画面 """
    ctf = CTF.GetInformation()
    error = {'password': ''}
    # ログイン済み
    if Authentication.CheckLogin():
        return SiteManager.JumpToReferer()
    # ログイン試行
    if flask.request.method == 'POST':
        if 'username' in flask.request.form and 'password' in flask.request.form:
            userinfo = Authentication.TryLogin(
                flask.request.form['username'], flask.request.form['password']
            )
            if userinfo:
                flask.session['login'] = True
                flask.session['teamname'] = userinfo['teamname']
                flask.session['username'] = userinfo['username']
            else:
                error['password'] = "Invalid username or password"
    # サイトを表示する
    SiteManager.SetReferer('login')
    return flask.render_template(
        'login.html',
        ctf = ctf,
        error = error
    )
