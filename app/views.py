# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy import desc

from flask import render_template, redirect, request, session, url_for
from flask.ext.login import (LoginManager, login_user, logout_user,
                             current_user, login_required)

from app import app, bp, db
from models import User, Locator
from forms import LoginForm, RegistrationForm

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

def save_url(path, groupname):
    locator = Locator(url=add_scheme(path), title=get_title(path),
                      groupname=groupname, date=datetime.today(),
                      username=current_user.username)
    db.session.add(locator)
    db.session.commit()
    if getattr(session, 'url', ''):
        session['url'] = ''
        session['groupname'] = ''
    return render_template('urls.jade', urls=get_urls())

#----------------------------------------------------------------------------
@app.route('/')
@app.route('/<path:path>/')
def main(path='', groupname=''):
    # main_func(path, '')
    if path:
        if url_exists(path):
            if current_user.is_authenticated:
                save_url(path, groupname)
                # return render_template('urls.jade', urls=get_urls())
            else:
                session['url'] = path
                session['groupname'] = groupname
                return redirect(url_for('login'))

    if current_user.is_authenticated:
        if getattr(session, 'url', ''):
            save_url(session['url'], getattr(session, 'groupname', ''))
            # return render_template('urls.jade', urls=get_urls())
        else:
            return render_template('urls.jade', urls=get_urls())

    return render_template('index.jade')

#----------------------------------------------------------------------------
# groupname - subdomain in blueprint
@bp.route("/<path:path>/")
def main2(groupname, path):
    if url_exists(path):
        if current_user.is_authenticated:
            save_url(path, groupname)
            return render_template('urls.jade', urls=get_urls())
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
    return render_template('register.html', form=form)

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
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',
                           error_msg = app.config['ERROR_404']), 404
