# coding: utf-8
import commands

def tokens(new):
    token_list = set()
    # コンテナIDを取得
    cid = commands.getoutput("docker ps | grep sample | awk '{print $1}'")
    # コンテナでコマンドを実行
    result = commands.getoutput("docker exec -it {0} cat tokens".format(cid))
    # 有効なトークンを調べる
    for line in result.split('\n'):
        if line[:6] == 'tokens-':
            token_list.add(line)
    # トークンの集合を返す
    return token_list

def title():
    return 'Sample Problem'
