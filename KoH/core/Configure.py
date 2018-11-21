# coding: utf-8
import json
import os.path

def LoadConfig():
    """ 設定ファイルを読み込む """
    cd = os.path.dirname(__file__)
    config_path = os.path.join(cd, "../../config.json")
    try:
        f = open(config_path, "r")
        config = json.load(f)
        return config
    except IOError:
        print("[-] config.json: File not found")
        exit(1)
    except ValueError:
        print("[-] config.json: Invalid JSON syntax")
        exit(1)

