# coding: utf-8
import flask
from KoH import app
from KoH.core import CTF
from KoH.core import DatetimeManager

@app.route("/")
def index():
    ctf = CTF.GetInformation()
    duration = DatetimeManager.GetDurationSet()
    return flask.render_template(
        'index.html',
        ctf = ctf,
        duration = duration
    )
