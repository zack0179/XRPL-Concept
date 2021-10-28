# -*- coding: utf-8 -*-
from flaskr import create_app, db
from dotenv import load_dotenv
load_dotenv('.env') 
 
db.init_db_command()
application = create_app()
