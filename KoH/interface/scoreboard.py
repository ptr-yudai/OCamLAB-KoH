# coding: utf-8
import flask
from KoH import app
from KoH.core import CTF
from KoH.core import Authentication
from KoH.core import Database
from KoH.core import SiteManager

@app.route("/score")
def scoreboard():
    """ スコアボード """
    ctf = CTF.GetInformation()
    # ログイン済み
    if not Authentication.CheckLogin():
        SiteManager.SetReferer('scoreboard')
        return SiteManager.JumpToPage('login')
    # ランキング取得
    ranking = Database.Query(
        "SELECT teamname,score FROM team ORDER BY score, lastlog DESC"
    )
    print ranking
    # サイトを表示する
    return flask.render_template(
        'scoreboard.html',
        ctf = ctf,
        ranking = ranking
    )
