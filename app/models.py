from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.whooshalchemy import whoosh_index

from app import db, app

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique = True)
    pwdhash = db.Column(db.String(54))
    
    def __init__(self, email, password):
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
        return '<User %r>' % (self.email)

# class with name URL does not work (URL - Uniform Resource Locator)
class Locator(db.Model):
    __tablename__ = 'locator'
    __searchable__ = ['url', 'title'] # for whooshalchemy
    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.String(500))
    title = db.Column(db.String(500))
    groupname = db.Column(db.String(25))
    date = db.Column(db.DateTime)
    email = db.Column(db.String(64), ForeignKey('user.email'))

    def __repr__(self):
        return '<URL %r>' % (self.url)

from flask.ext.whooshalchemy import whoosh_index
whoosh_index(app, Locator)

