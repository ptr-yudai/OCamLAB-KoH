# coding: utf-8
import datetime
import pytz
import Configure

def CheckDuration():
    """ CTFが開催中か確認する """
    config = Configure.LoadConfig()
    start = config['ctf']['duration']['start']
    end   = config['ctf']['duration']['end']
    # 各種時刻を取得
    tz = pytz.timezone(config['ctf']['duration']['timezone'])
    dt_now = datetime.datetime.now(tz = tz)
    dt_start = datetime.datetime(
        start['year'], start['month'], start['date'],
        start['hour'], start['minute'], start['second'],
        tzinfo = tz
    )
    dt_end = datetime.datetime(
        end['year'], end['month'], end['date'],
        end['hour'], end['minute'], end['second'],
        tzinfo = tz
    )
    # 開始前かの確認
    if dt_now < dt_start:
        return 1
    # 終了後かの確認
    if dt_now > dt_end:
        return 2
    return 0


def GetDurationSet():
    """ CTFの開催期間をローカルタイムとUTCで文字列として返す """
    duration = {
        'local': {
            'start': GetStartTime(False),
            'end'  : GetEndTime(False)
        },
        'global': {
            'start': GetStartTime(True),
            'end'  : GetEndTime(True)
        }
    }
    return duration


def GetStartTime(utc=False):
    """ CTFの開始時刻を文字列で返す """
    config = Configure.LoadConfig()
    start = config['ctf']['duration']['start']
    time_format = config['ctf']['duration']['format']
    tz = pytz.timezone(config['ctf']['duration']['timezone'])
    dt_start = datetime.datetime(
        start['year'], start['month'], start['date'],
        start['hour'], start['minute'], start['second'],
        tzinfo = tz
    )
    if utc:
        return dt_start.astimezone(pytz.timezone('UTC'))
    else:
        return dt_start.strftime(time_format)


def GetEndTime(utc=False):
    """ CTFの修了時刻を文字列で返す """
    config = Configure.LoadConfig()
    end = config['ctf']['duration']['end']
    time_format = config['ctf']['duration']['format']
    tz = pytz.timezone(config['ctf']['duration']['timezone'])
    dt_end = datetime.datetime(
        end['year'], end['month'], end['date'],
        end['hour'], end['minute'], end['second'],
        tzinfo = tz
    )
    if utc:
        return dt_end.astimezone(pytz.timezone('UTC'))
    else:
        return dt_end.strftime(time_format)
