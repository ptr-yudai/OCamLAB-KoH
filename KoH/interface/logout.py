# coding: utf-8
import flask
from KoH import app
from KoH.core import SiteManager

@app.route("/logout")
def logout():
    flask.session['login'] = False
    return SiteManager.JumpToPage('index')
