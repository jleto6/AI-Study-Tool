from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('project', __name__)

@bp.route('/')
def index():
    db = get_db()
    projects = db.execute(
        'SELECT p.id, title, subheading, body, created, author_id, username'
        ' FROM project p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('project/index.html', projects=projects)



@bp.route('/create', methods=('GET', 'project'))
@login_required
def create():
    if request.method == 'project':
        title = request.form['title'] 
        subheading = request.form['subheading'] 
        body = request.form['body'] 
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO project (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('project.index'))

    return render_template('project/create.html')

def get_project(id, check_author=True):
    project = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM project p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if project is None:
        abort(404, f"project id {id} doesn't exist.")

    if check_author and project['author_id'] != g.user['id']:
        abort(403)

    return project

@bp.route('/<int:id>/update', methods=('GET', 'POST'), endpoint='project_update')
@login_required
def update(id):
    # Function code

    project = get_project(id)

    if request.method == 'POST':
        title = request.form['title']
        subheading = request.form['subheading']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE project SET title = ?, subheading = ?, body = ?'
                ' WHERE id = ?',
                (title, subheading, body, id)
            )
            db.commit()
            return redirect(url_for('project.index'))

    return render_template('project/update.html', project=project)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_project(id)
    db = get_db()
    db.execute('DELETE FROM project WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('project.index'))
