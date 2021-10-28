# -*- coding: utf-8 -*-

import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
        #DATABASE=os.environ.get("DATABASE_URL"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # import and call database connection
    from flaskr import db
    db.init_app(app)

    # import and register authentication blueprint
    from flaskr import auth
    app.register_blueprint(auth.bp)

    # import and register blog blueprint
    #   does not have a url_prefix. So the index view will be at /
    #   blog is the main feature of Flaskr, blog index will be the main index
    from flaskr import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
