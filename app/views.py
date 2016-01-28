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

# ----------------------------------------------------------------------------
@app.route('/')
@app.route('/<path:path>')
def main(path=None):
    if path:
        return "<i>Path for saving: </i>" + path
    if current_user.is_authenticated:
        return "Hi, %s!" % current_user.username
    else:
        return "Welcome to this page"

# ----------------------------------------------------------------------------
# Add a route to the blueprint
@bp.route("/<path:path>")
def main2(groupname, path):
    return 'Welcome to your subdomain, {}'.format(groupname)

# Register the blueprint into the application
app.register_blueprint(bp)

# ----------------------------------------------------------------------------
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
    return render_template('login.html', form=form)

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