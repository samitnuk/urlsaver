# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy import desc

from flask import render_template, redirect, request, session, url_for, flash
from flask.ext.login import (LoginManager, login_user, logout_user,
                             current_user, login_required)
from flask.ext.mail import Mail, Message

from app import app, bp, db
from models import User, Locator
from forms import (LoginForm, RegistrationForm, EditForm, SearchForm,
                   RestorePasswordForm)

from helpers import add_scheme, url_exists, get_title, get_new_password

lm = LoginManager()
lm.init_app(app)

mail=Mail(app)

@lm.user_loader
def get_user(user_id):
    return db.session.query(User).get(user_id)

#/ INNER HELPERS /-----------------------------------------------------------

def get_urls():
    return db.session.query(Locator)\
                            .filter_by(email=current_user.email)\
                            .order_by(desc(Locator.date))

def get_groupnames():
    return [x[0] for x in list(set(db.session.query(Locator.groupname) \
                                   .filter_by(email=current_user.email)))]


def save_url(path, groupname):
    locator = Locator(url=add_scheme(path), title=get_title(path),
                      groupname=groupname, date=datetime.now(),
                      email=current_user.email)
    db.session.add(locator)
    db.session.commit()
    if session['url']:
        session['url'] = ''
        session['groupname'] = ''
    return redirect(url_for('main'))

#/ ROUTES /------------------------------------------------------------------

@app.route('/', methods=['GET', 'POST'])
def main():
    if current_user.is_authenticated:
        if session['url']:
            save_url(session['url'], session['groupname'])
        form = SearchForm(request.form)
        if request.method == 'POST' and form.validate_on_submit():
            return redirect(url_for('search_results',
                                    query = form.search.data))
        return render_template('urls.jade', form=form,
                                            urls=get_urls(),
                                            groupnames=get_groupnames())
    return render_template('home.jade')


@app.route('/<path:path>/')
def main1(path):
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


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('main'))
    return render_template('register.jade', form=form)


@app.route('/restore_password/', methods=['GET', 'POST'])
def restore_password():
    form = RestorePasswordForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        new_password = get_new_password()
        # msg = Message('Restore password | urlsaver.ua',
	    #               sender = MAIL_USERNAME,
	    #               recipients = [email])
        # msg.body = render_template('restore_pass_email.jade',
        #                            password=new_password)
	    # mail.send(msg)
        # user = db.session.query(Locator).filter_by(email=email).first()
        # user.password = new_password
        # db.session.commit()
        flash('Please check you email for new password')
        return redirect(url_for('login'))

    return render_template('restore_password.jade', form=form)


@app.route('/login/', methods = ['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user = form.get_user()
        login_user(user, remember=True)
        return redirect(url_for('main'))
    return render_template('login.jade', form=form)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))


@app.route('/groupname/<groupname>/')
@login_required
def urls_by_group(groupname):
    form = SearchForm(request.form)
    if request.method == 'POST':
        return redirect(url_for('search_results', query = form.search.data))
    if groupname == 'ungrouped':
        groupname = ''
    urls = db.session.query(Locator).filter_by(groupname=groupname) \
                                    .filter_by(email=current_user.email) \
                                    .order_by(desc(Locator.date)).all()
    return render_template('urls.jade', form=form,
                                        urls=urls,
                                        groupnames=get_groupnames())


@app.route('/edit/<int:id>/', methods = ['GET', 'POST'])
@login_required
def edit_url(id):
    form = EditForm(request.form)
    url_row = db.session.query(Locator).filter_by(id=id).first()
    if request.method == 'POST' and form.validate_on_submit():
        url_row.title = form.title.data
        url_row.url = form.url.data
        url_row.groupname = form.groupname.data
        db.session.commit()
        return redirect(url_for('main'))
    return render_template('edit.jade', form=form, url=url_row)


@app.route('/delete/<int:id>/')
@login_required
def delete_url(id):
    db.session.query(Locator).filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('main'))


@app.route('/search_results/<query>')
@login_required
def search_results(query):
    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        return redirect(url_for('search_results', query = form.search.data))
    results = Locator.query.whoosh_search(query).\
                            filter_by(email=current_user.email)
    for r in results.order_by(desc(Locator.id)):
        print r.id, r.date
    return render_template('urls.jade', form=form,
                                        urls=results,
                                        groupnames=get_groupnames())


@app.route('/contact/')
def contact():
    return render_template('contact.jade')


@app.route('/about/')
def about():
    return render_template('about.jade')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.jade')
