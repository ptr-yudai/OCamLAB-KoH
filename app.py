#!/usr/bin/env python
# coding: utf-8
import config
import datetime
import sqlite3
import hashlib
from contextlib import closing
import json
from flask import Flask, session, redirect, request, url_for, render_template
app = Flask(__name__)

@app.route("/")
def home():
    """ Home

    Rules, duration and so on.
    """
    # Check for login status
    login = checkLogin()
    session['referer'] = ''
    # Get the duration
    is_running, duration = checkDuration()
    return render_template(
        'index.html',
        duration = duration,
        login = login
    )

@app.route("/token")
def token():
    """ Team Token

    Show all team tokens.
    """
    # Check for the login status
    if not checkLogin():
        session['referer'] = 'token'
        return redirect(url_for('login'))
    else:
        session['referer'] = ''
    # Get the team token
    with open(config.tokenpath) as f:
        token_list = json.load(f)
    return render_template(
        'token.html',
        token_list = token_list.items()
    )

@app.route("/score")
def scoreboard():
    """ Challenges

    Show all available challenges.
    """
    # Check for the login status
    if not checkLogin():
        session['referer'] = 'scoreboard'
        return redirect(url_for('login'))
    else:
        session['referer'] = ''
    # Get ranking table
    ranking = getRanking()
    return render_template(
        'score.html',
        ranking = ranking
    )

@app.route("/challenges")
def challenges():
    """ Challenges

    Show all available challenges.
    """
    # Check for the login status
    if not checkLogin():
        session['referer'] = 'challenges'
        return redirect(url_for('login'))
    else:
        session['referer'] = ''
    # Check for the duration
    is_running, duration = checkDuration()
    # Get challenge list
    challs = getChallengeList()
    return render_template(
        'challenges.html',
        running = is_running,
        challs = challs
    )

@app.route("/challenge", methods=['GET', 'POST'])
def challenge():
    """ Challenges

    Show a challenge
    """
    status = 0
    message = ''
    # Check for the login status
    if not checkLogin():
        session['referer'] = 'challenges'
        return redirect(url_for('login'))
    else:
        session['referer'] = ''
    # Check for the duration
    is_running, duration = checkDuration()
    if not is_running:
        return redirect(url_for('challenges'))
    # Verify the challenge id
    cid = request.args.get("id", default=0, type=int)
    if cid <= 0:
        return redirect(url_for('challenges'))
    # Check flag is submitted
    if isSolved(cid):
        message = 'You have already solved this challenge.'
        status = 2
    elif request.method == 'POST':
        if 'flag' in request.form:
            if submitFlag(cid, request.form['flag']):
                message = 'The flag is correct!'
                status = 1
            else:
                message = 'The flag is wrong...'
                status = -1
    # Get challenge info
    chall = getChallenge(cid)
    if not chall:
        return redirect(url_for('challenges'))
    return render_template(
        'challenge.tmpl',
        chall = chall,
        status = status,
        message = message
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Login
    """
    # Check for the login status
    if checkLogin():
        return redirect(url_for('home'))
    # Login attempt
    message = ''
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            info = tryLogin(request.form['username'], request.form['password'])
            if info:
                session['login'] = True
                session['username'] = info['username']
                return jump2referer()
            else:
                message = 'Invalid username or password.'
    return render_template(
        'login.html',
        message = message
    )

@app.route('/logout')
def logout():
    """ Logout
    """
    # Check for the login status
    if not checkLogin():
        return redirect(url_for('home'))
    # Logout attempt
    session['login'] = False
    session['user'] = None
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Register
    """
    # Check for the login status
    if checkLogin():
        return redirect(url_for('home'))
    # Register attempt
    message = ''
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form and 'password-confirm' in request.form:
            if len(request.form['username']) > 63:
                message = 'Username is too long.'
            elif request.form['password'] == request.form['password-confirm']:
                info = tryRegister(request.form['username'], request.form['password'])
                if info:
                    session['login'] = True
                    session['username'] = request.form['username']
                    return jump2referer()
                else:
                    message = 'The username is already used.'
            else:
                message = 'Confirm your password.'
    return render_template(
        'register.html',
        message = message
    )

def getRanking():
    """ Get the ranking """
    with closing(sqlite3.connect(config.dbpath)) as conn:
        c = conn.cursor()
        c.execute(u"SELECT username,score FROM account ORDER BY score DESC")
        result = c.fetchall()
    return result

def getChallenge(cid):
    """ Get a challenge info """
    with closing(sqlite3.connect(config.dbpath)) as conn:
        c = conn.cursor()
        c.execute(u"SELECT * FROM challenge WHERE id=?", (str(cid),))
        result = c.fetchone()
    return result

def getChallengeList():
    """ Get challenge list """
    with closing(sqlite3.connect(config.dbpath)) as conn:
        c = conn.cursor()
        c.execute(u"SELECT id,title,score,category,solved FROM challenge")
        result = c.fetchall()
    return result

def tryLogin(username, password):
    """ Login attempt """
    with closing(sqlite3.connect(config.dbpath)) as conn:
        c = conn.cursor()
        sha256 = hashlib.sha256()
        sha256.update(password)
        password_hash = sha256.hexdigest()
        c.execute(u"SELECT username FROM account WHERE username=? and password=?", (username, password_hash))
        result = c.fetchone()
    if result:
        return {'username': result[0]}
    else:
        return None

def tryRegister(username, password):
    """ Register attempt """
    with closing(sqlite3.connect(config.dbpath)) as conn:
        c = conn.cursor()
        sha256 = hashlib.sha256()
        sha256.update(password)
        password_hash = sha256.hexdigest()
        try:
            c.execute(u"INSERT INTO account(username, password) VALUES(?, ?)", (username, password_hash))
            conn.commit()
        except sqlite3.IntegrityError:
            return False
    return True

def isSolved(cid):
    """ Check if the challenge is already solved """
    with closing(sqlite3.connect(config.dbpath)) as conn:
        c = conn.cursor()
        c.execute(u"SELECT solved FROM account WHERE username=?", (session['username'],))
        result = c.fetchone()
    print result
    for x in result[0].split(','):
        try:
            if cid == int(x):
                return True
        except:
            pass
    return False

def submitFlag(cid, flag):
    """ Submit flag """
    with closing(sqlite3.connect(config.dbpath)) as conn:
        c = conn.cursor()
        c.execute(u"SELECT flag,score FROM challenge WHERE id=?", (cid,))
        result = c.fetchone()
    valid_flag, score = result
    if flag.replace(" ", "") != valid_flag:
        return False
    # Flag is correct
    with closing(sqlite3.connect(config.dbpath)) as conn:
        c = conn.cursor()
        c.execute(u"UPDATE account SET score=score+?, solved=?||','||solved WHERE username=?", (score, str(cid), session['username']))
        c.execute(u"UPDATE challenge SET solved=solved+1 WHERE id=?", (cid,))
        conn.commit()
    return True

def checkLogin():
    """ Check if the user is already logged in. """
    if 'login' in session and session['login']:
        return True
    return False

def jump2referer(default='home'):
    """ Redirect to the page the user wanted to go. """
    if 'referer' in session and session['referer'] != '':
        page, session['referer'] = session['referer'], ''
        return redirect(url_for(page))
    return redirect(url_for(default))

def checkDuration():
    """ Check for the CTF duration """
    start = datetime.datetime(
        config.duration['start_year'], config.duration['start_month'],
        config.duration['start_date'], config.duration['start_hour'],
        config.duration['start_minute'], config.duration['start_second']
    )
    end = datetime.datetime(
        config.duration['end_year'], config.duration['end_month'],
        config.duration['end_date'], config.duration['end_hour'],
        config.duration['end_minute'], config.duration['end_second']
    )
    now = datetime.datetime.now()
    if start > now or end < now:
        is_running = False
    else:
        is_running = True
    duration = {
        'start': formatDate(start), 'end': formatDate(end),
        'timezone': config.timezone
    }
    return is_running, duration

def formatDate(date):
    return date.strftime(config.date_format)

def initDB():
    with closing(sqlite3.connect(config.dbpath)) as conn:
        c = conn.cursor()
        # Create account table if not exist
        c.execute("select name from sqlite_master where type='table' and name='account'")
        if not c.fetchone():
            create_table = """
            CREATE TABLE account(
            id       INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            username CHAR(64) NOT NULL UNIQUE,
            password CHAR(128) NOT NULL,
            score    INTEGER NOT NULL DEFAULT 0,
            solved   TEXT DEFAULT ''
            )
            """
            c.execute(create_table)
        # Create challenge table if not exist
        c.execute("select name from sqlite_master where type='table' and name='challenge'")
        if not c.fetchone():
            create_table = """
            CREATE TABLE challenge(
            id       INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            title    CHAR(128) NOT NULL,
            problem  TEXT NOT NULL,
            score    INT NOT NULL,
            category CHAR(32) NOT NULL,
            flag     CHAR(64) NOT NULL,
            solved   INT NOT NULL DEFAULT 0
            )
            """
            c.execute(create_table)
        conn.commit()
    return

if __name__ == '__main__':
    app.secret_key = config.secret_key
    initDB()
    app.run(debug=True, port=8080)
