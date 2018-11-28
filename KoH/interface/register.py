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
    error = {'username': '', 'password': '', 'teamcode': ''}
    # ログイン済み
    if Authentication.CheckLogin():
        return SiteManager.JumpToReferer()
    # 登録試行
    if flask.request.method == 'POST':
        form = flask.request.form
        if 'user' in form and 'username' in form and 'password' in form and 'password-confirm' in form and 'country' in form:
            # ユーザー登録
            if form['password'] == form['password-confirm']:
                if ctf['team']:
                    # チームに参加
                    if 'teamcode' in form and 'teamname' in form:
                        result = Authentication.TryRegisterUser(
                            form['username'], form['password'], form['teamname'], form['teamcode'], form['country']
                        )
                        error[result[0]] = result[1]
                        if result[1] == '':
                            return SiteManager.JumpToReferer()
                else:
                    # 個人で参加
                    result = Authentication.TryRegisterUser(
                        form['username'], form['password'], None, None, form['country']
                    )
                    error[result[0]] = result[1]
                    if result[1] == '':
                        return SiteManager.JumpToReferer()
            else:
                # パスワードミス
                error['password'] = 'Confirm your password'
        elif 'team' in form and 'teamname' in form and 'teamcode' in form and ctf['team']:
            # チーム登録
            result = Authentication.TryRegisterTeam(form['teamname'], form['teamcode'])
    # サイトを表示する
    return flask.render_template(
        'register.html',
        ctf = ctf,
        error = error
    )
