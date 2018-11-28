# coding: utf-8
import flask
from KoH import app
from KoH.core import CTF
from KoH.core import DatetimeManager
from KoH.core import Authentication
from KoH.core import SiteManager

@app.route("/")
def index():
    ctf = CTF.GetInformation()
    duration = DatetimeManager.GetDurationSet()
    login = Authentication.CheckLogin()
    # サイトを表示する
    SiteManager.SetReferer('index')
    return flask.render_template(
        'index.html',
        ctf = ctf,
        duration = duration,
        login = login
    )
