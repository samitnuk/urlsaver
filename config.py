import os

#/ GENERAL SETTINGS /--------------------------------------------------------
DEBUG = True
SERVER_NAME = 'urlsaver.ua:5000'


#/ FOR FORMS /---------------------------------------------------------------
CSRF_ENABLED = True
SECRET_KEY = "ababagalamaga"
# SECRET_KEY = os.urandom(24)


#/ FOR DATABASE /------------------------------------------------------------
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'urlsaver.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

SQLALCHEMY_TRACK_MODIFICATIONS = False
# http://flask-sqlalchemy.pocoo.org/2.1/config/#configuration-keys

#/ FOR WhooshAlchemy /-------------------------------------------------------
WHOOSH_BASE = os.path.join(basedir, 'search.db')
WHOOSH_DISABLED = True
