from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    pwdhash = db.Column(db.String(54))
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email.lower()
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

class URLs(db.Model):
    __tablename__ = 'URLs'
    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.String(500))
    groupname = db.Column(db.String(25))
    date = db.Column(db.Date)
    username = db.Column(db.String(64), ForeignKey('users.username'))

    def __repr__(self):
        return '<URLs %r>' % (self.url)