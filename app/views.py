from datetime import datetime

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
from urlparse import urlparse
from helpers import url_exists, get_title

def get_urls():
    return db.session.query(Locator)\
                            .filter_by(username=current_user.username).all()

def save_url(path, groupname):
    locator = Locator(url=path, title=get_title(path),
                      groupname=groupname, date=datetime.today(),
                      username=current_user.username)
    db.session.add(locator)
    db.session.commit()
    if getattr(session, 'url', ''):
        session['url'] = ''
        session['groupname'] = ''
    
    return "URL saved to DB"

# def main_func(path, groupname):

#----------------------------------------------------------------------------
@app.route('/')
@app.route('/<path:path>')
def main(path='', groupname=''):
    # main_func(path, '')
    if path:
        if urlparse(path).scheme and url_exists(path):
            if current_user.is_authenticated:
                save_url(path, groupname)
                return render_template('urls.html', urls=get_urls())
            else:
                session['url'] = path
                session['groupname'] = groupname
                return redirect(url_for('login'))
        # return render_template('index.html',
        #                        arg="incorrect path: {}".format(path))

    if current_user.is_authenticated:
        print "current_user.is_authenticated = True"
        if getattr(session, 'url', ''):
            save_url(session['url'], getattr(session, 'groupname', ''))
        else:
            return render_template('urls.html', urls=get_urls())

    return render_template('index.html', arg=getattr(session, 'url', ''))

#----------------------------------------------------------------------------
# groupname - subdomain in blueprint
@bp.route("/<path:path>")
def main2(groupname, path):
    return 'Welcome to your subdomain, {}'.format(groupname)

# Register the blueprint into the application
app.register_blueprint(bp)

#----------------------------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
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
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user = form.get_user()
        login_user(user, remember=True)
        return redirect(url_for('main'))
    return render_template('login.html', form=form)

#----------------------------------------------------------------------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))

#----------------------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',
                           error_msg = app.config['ERROR_404']), 404
