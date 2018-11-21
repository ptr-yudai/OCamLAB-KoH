# coding: utf-8
import Configure

def GetInformation():
    """ CTFの詳細情報を取得する """
    config = Configure.LoadConfig()
    ctf = {
        'name': config['ctf']['name'],
        'brand': config['ctf']['brand'],
    }
    return ctf
