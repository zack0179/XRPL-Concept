# -*- coding: utf-8 -*-

from flaskr import create_app, db

db.init_db()
application = create_app()
