# -*- coding: utf-8 -*-
'''
Authentication Blueprint
    registering an accout and generate a wallet connected to the test net. 
'''

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from flaskr import xrp_poc

bp = Blueprint('auth', __name__, url_prefix='/auth')

# register view function
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        account = xrp_poc.usr_wallet()
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password, account) VALUES (?, ?, ?)",
                    (username, generate_password_hash(password), account),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

# login view function
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone() # fetchone returns one row from the query

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()                 # session is a dict that stores data across requests
            session['user_id'] = user['id'] # user id is stored in session when loged in
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

# load user information from session and make it available to other views
@bp.before_app_request # registers function that runs before the view function
def load_logged_in_user():
    '''checks if a user id is stored in the session and
        gets that user’s data from the database,
        storing it on g.user, which lasts for the length of the request.
        If there is no user id, or if the id doesn’t exist, g.user will be None'''
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone() # returns one row from the query

# logout
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Require Authentication in Other Views
def login_required(view):
    '''decorator returns a new view function that wraps the original.
        checks if a user is loaded and redirects to the login page otherwise.
        If a user is loaded the original view is called and continues normally.'''
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
