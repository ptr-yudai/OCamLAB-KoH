# coding: utf-8
import flask


def JumpToPage(page):
    """ 特定のページにジャンプする """
    return flask.redirect(flask.url_for(page))


def JumpToReferer():
    """ 元いたページにジャンプする """
    return flask.redirect(flask.url_for(flask.session['referer']))


def SetReferer(page):
    """ リファラーを設定する """
    flask.session['referer'] = page
