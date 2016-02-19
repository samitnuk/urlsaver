# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy import desc

from flask import render_template, redirect, request, session, url_for
from flask.ext.login import (LoginManager, login_user, logout_user,
                             current_user, login_required)

from app import app, bp, db
from models import User, Locator
from forms import LoginForm, RegistrationForm, EditForm

lm = LoginManager()
lm.init_app(app)

@lm.user_loader
def get_user(user_id):
    return db.session.query(User).get(user_id)

#/ INNER HELPERS /-----------------------------------------------------------
# from urlparse import urlparse
from helpers import add_scheme, url_exists, get_title

def get_urls():
    return db.session.query(Locator)\
                            .filter_by(username=current_user.username)\
                            .order_by(desc(Locator.id))

def get_groupnames():
    return [x[0] for x in list(set(db.session.query(Locator.groupname)))]


def save_url(path, groupname):
    locator = Locator(url=add_scheme(path), title=get_title(path),
                      groupname=groupname, date=datetime.today(),
                      username=current_user.username)
    db.session.add(locator)
    db.session.commit()
    if getattr(session, 'url', ''):
        session['url'] = ''
        session['groupname'] = ''
    return redirect(url_for('main'))

#----------------------------------------------------------------------------
@app.route('/')
def main():
    if current_user.is_authenticated:
        if getattr(session, 'url', ''):
            save_url(session['url'], getattr(session, 'groupname', ''))
        return render_template('urls.jade', urls=get_urls(),
                                            groupnames=get_groupnames())
    return render_template('index.jade')

@app.route('/<path:path>/')
def main1(path):
    # main_func(path, '')
    if path:
        if url_exists(path):
            if request.query_string:
                path = path + '/?' + request.query_string
            if current_user.is_authenticated:
                save_url(path, groupname='')
            else:
                session['url'] = path
                session['groupname'] = ''
                return redirect(url_for('login'))

    return redirect(url_for('main'))

#----------------------------------------------------------------------------
# groupname - subdomain in blueprint
@bp.route("/<path:path>/")
def main2(groupname, path):
    if url_exists(path):
        if request.query_string:
            path = path + '/?' + request.query_string
        if current_user.is_authenticated:
            save_url(path, groupname)
        else:
            session['url'] = path
            session['groupname'] = groupname
            return redirect(url_for('login'))

    return redirect(url_for('main'))

# Register the blueprint into the application
app.register_blueprint(bp)

#----------------------------------------------------------------------------
@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('main'))
    return render_template('register.jade', form=form)

#----------------------------------------------------------------------------
@app.route('/restore_password/', methods=['GET', 'POST'])
def restore_password():
    # form = RegistrationForm(request.form)
    # if request.method == 'POST' and form.validate_on_submit():
    #     user = User(username=form.username.data,
    #                 email=form.email.data,
    #                 password=form.password.data)
    #     db.session.add(user)
    #     db.session.commit()
    #     login_user(user, remember=True)
    #     return redirect(url_for('main'))
    return redirect(url_for('main'))

#----------------------------------------------------------------------------
@app.route('/login/', methods = ['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user = form.get_user()
        login_user(user, remember=True)
        return redirect(url_for('main'))
    return render_template('login.jade', form=form)

#----------------------------------------------------------------------------
@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))

#----------------------------------------------------------------------------
@app.route('/groupname/<groupname>')
@login_required
def urls_by_group(groupname):
    if groupname == 'ungrouped':
        groupname = ''
    urls = db.session.query(Locator).filter_by(groupname=groupname)\
                                    .order_by(desc(Locator.id))
    return render_template('urls.jade', urls=urls, 
                                        groupnames=get_groupnames())

#----------------------------------------------------------------------------
@app.route('/edit/<int:id>/')
@login_required
def edit_url(id):
    form = EditForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        url_row = db.session.query(Locator).filter_by(id=id).first()
        url_row.title = form.title
        url_row.url = form.url
        url_row.groupname = form.groupname
        db.session.commit()
    return redirect(url_for('main'))

#----------------------------------------------------------------------------
@app.route('/delete/<int:id>/')
@login_required
def delete_url(id):
    db.session.query(Locator).filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('main'))

#----------------------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',
                           error_msg = app.config['ERROR_404']), 404