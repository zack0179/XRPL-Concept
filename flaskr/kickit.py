<<<<<<< HEAD
from flaskr import create_app
from dotenv import load_dotenv

load_dotenv('.env')
=======
# -*- coding: utf-8 -*-

from flaskr import create_app, db

db.init_db()
>>>>>>> beta
application = create_app()
