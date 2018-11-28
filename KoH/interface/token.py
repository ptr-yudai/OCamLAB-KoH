# coding: utf-8
import flask
from KoH import app
from KoH.core import CTF
from KoH.core import Configure
from KoH.core import Authentication
from KoH.core import Token
from KoH.core import SiteManager

@app.route("/token")
def token():
    """ ログイン画面 """
    ctf = CTF.GetInformation()
    config = Configure.LoadConfig()
    # ログイン済み
    if not Authentication.CheckLogin():
        SiteManager.SetReferer('token')
        return SiteManager.JumpToPage('login')
    # トークンを取得
    path = config['koh']['path']
    tokens = Token.GetTokens(path)
    # サイトを表示する
    return flask.render_template(
        'token.html',
        ctf = ctf,
        tokens = tokens
    )
