# -*- coding: utf-8 -*-
'''
blog blueprint
    The blog should list all posts, allow logged in users to create posts, and
        allow the author of a post to edit, see their account holding value the 
        post represents, and delete it.
''' 

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

# the main index view (blog)
@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, issue_quantity, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall() # fetchall returns all query resuts in db
    return render_template('blog/index.html', posts=posts)

# create view
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        issue_quantity = request.form['issue_quantity']
        error = None

        if not title:
            title = 'New token.'


        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, issue_quantity, wallet_accout, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, issue_quantity, g.user['account'], g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

# function to get the post and call it from each view
#   update and delete views will need to fetch a post by id and check if the
#   author matches the logged in user
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, issue_quantity, wallet_accout, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        # check_author to get a post without checking the author
        abort(403) # HTTP status code
        #  404 means “Not Found”, and 403 means “Forbidden”
        #  401 means “Unauthorized”, redirect to the login page instead

    return post

# update view
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        issue_quantity = request.form['issue_quantity']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, issue_quantity = ?'
                ' WHERE id = ?',
                (title, issue_quantity, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

# delete view
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
