from flask.ext.wtf import Form
# from flask.ext.wtf.file import FileField, FileRequired, FileAllowed
from wtforms import TextField, PasswordField, validators

from app import db
from models import User, Locator

#----------------------------------------------------------------------------
class LoginForm(Form):
    email = TextField('Email', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

    def validate_email(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user.')

        if not user.check_password(password=self.password.data):
            raise validators.ValidationError('Invalid password.')

    def get_user(self):
        return db.session.query(User)\
            .filter_by(email=self.email.data).first()

#----------------------------------------------------------------------------
class RegistrationForm(Form):
    email = TextField('Email Address', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    confirm = PasswordField('Repeat Password',
                            [validators.Required(), 
                             validators.EqualTo('password',
                             message='Passwords must match.')])

    def validate_email(self, field):
        if db.session.query(User)\
            .filter_by(email=self.email.data).count() > 0:
            raise validators.ValidationError('Duplicate email.')

#----------------------------------------------------------------------------
class EditForm(Form):
    title = TextField('title', [validators.Required()])
    url = TextField('url', [validators.Required()])
    groupname = TextField('groupname')

#----------------------------------------------------------------------------
class SearchForm(Form):
    search = TextField('search', [validators.Required()])