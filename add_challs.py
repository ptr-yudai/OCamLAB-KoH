# coding: utf-8
import sqlite3
import glob
import json
from contextlib import closing
from KoH.core import Configure

def Query(query, param=None):
    """ SQLクエリを発行する """
    with closing(sqlite3.connect(Configure.GetDatabasePath())) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        if param:
            cur.execute(query, param)
        else:
            cur.execute(query)
        result = cur.fetchall()
        conn.commit()
    return result

if __name__ == '__main__':
    for filename in glob.glob("./challs/*.json"):
        print("[+] Processing {0} ...".format(filename))
        # ロード
        try:
            with open(filename) as f:
                chall = json.load(f)
        except:
            print("[-] Invalid JSON!")
            continue
        # 検証
        result = Query("SELECT id FROM challenge WHERE title=?", (chall['title'], ))
        if result:
            print("[?] The problem `{0}` exists. Do you want to overwrite it?".format(chall['title']))
            ans = raw_input("[Y/N] ")
            if ans != 'Y':
                print("[+] Skipping...")
                continue
            # 上書き
            Query(
                "UPDATE challenge SET problem=?, score=?, category=?, flag=? WHERE title=?",
                (chall['problem'], chall['score'], chall['category'], chall['flag'], chall['title'])
            )
            print("[+] The challenge is successfully updated")
        else:
            # 追加
            Query(
                "INSERT INTO challenge(title, problem, score, category, flag) VALUES(?, ?, ?, ?, ?)",
                (chall['title'], chall['problem'], chall['score'], chall['category'], chall['flag'])
            )
            print("[+] The challenge is successfully added")
