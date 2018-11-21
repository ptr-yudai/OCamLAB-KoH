# coding: utf-8
import flask
from KoH import app
from KoH.core import CTF
from KoH.core import Authentication
from KoH.core import SiteManager

@app.route("/register", methods=['GET', 'POST'])
def register():
    """ 登録画面 """
    ctf = CTF.GetInformation()
    error = {'username': '', 'password': ''}
    # ログイン済み
    if Authentication.CheckLogin():
        return SiteManager.JumpToReferer()
    # 登録試行
    if flask.request.method == 'POST':
        if 'username' in flask.request.form and 'password' in flask.request.form:
            userinfo = Authentication.TryLogin(
                flask.request.form['username'], flask.request.form['password']
            )
            if userinfo:
                flask.session['login'] = True
                flask.session['teamname'] = userinfo['teamname']
                flask.session['username'] = userinfo['username']
                return SiteManager.JumpToPage('login')
            else:
                error['password'] = "Invalid username or password"
    # サイトを表示する
    return flask.render_template(
        'register.html',
        ctf = ctf,
        error = error
    )
