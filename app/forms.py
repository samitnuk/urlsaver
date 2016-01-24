from flask.ext.wtf import Form
# from flask.ext.wtf.file import FileField, FileRequired, FileAllowed
from wtforms import TextField, PasswordField, validators

from app import db
from models import User, URLs

#----------------------------------------------------------------------------
class LoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

    def validate_username(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        if not user.check_password(password=self.password.data):
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(User)\
            .filter_by(username=self.username.data).first()

#----------------------------------------------------------------------------
class RegistrationForm(Form):
    username = TextField('Username', [validators.Required()])
    email = TextField('Email Address')
    password = PasswordField('Password', [validators.Required(),
                                          validators.EqualTo('confirm',
                                          message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

    def validate_username(self, field):
        if db.session.query(User)\
            .filter_by(username=self.username.data).count() > 0:
            raise validators.ValidationError('Duplicate username')
