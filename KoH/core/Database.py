# coding: utf-8
import sqlite3
from contextlib import closing
import Configure

def Query(query, param=None):
    """ SQLクエリを発行する """
    sqlite3.dbapi2.converters['DATETIME'] = sqlite3.dbapi2.converters['TIMESTAMP']
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
