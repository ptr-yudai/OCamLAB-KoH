#!/usr/bin/env python
# coding: utf-8
from KoH import app
from KoH.core import Configure

from KoH.interface import index
from KoH.interface import login
#from KoH.interface import logout

if __name__ == '__main__':
    config = Configure.LoadConfig()
    app.config['SECRET_KEY'] = config['server']['secret']
    Configure.InitializeDatabase()
    app.run(
        debug = config['debug'],
        host = config['server']['host'],
        port = config['server']['port']
    )
