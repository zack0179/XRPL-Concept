from flaskr import create_app
from flasker.db import init_db_command 

init_db_command()
application = create_app()
