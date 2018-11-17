"""
 CTF Config File

 Edit this file to change the CTF confing.
"""
import os
from scripts import def_ziplist

# Secret key for sessionw
secret_key = os.urandom(24)

# Database
dbpath = 'database/database.db'

# Duration and date format
duration = {
    "start_year"  : 2018,
    "start_month" : 11,
    "start_date"  : 16,
    "start_hour"  : 18,
    "start_minute": 0,
    "start_second": 0,
    "end_year"  : 2018,
    "end_month" : 11,
    "end_date"  : 18,
    "end_hour"  : 19,
    "end_minute": 0,
    "end_second": 0,
}
date_format = '%b %dth %Y, %H:%M:%S'
timezone = 'JST'

# Token
tokenpath = 'database/token.json'
scripts = [
    def_ziplist.tokens
]
