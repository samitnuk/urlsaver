import os
from local_config import MY_MAIL_USERNAME, MY_MAIL_PASSWORD

DEBUG = True
SERVER_NAME = 'urlsaver.ua:5000'


CSRF_ENABLED = True
SECRET_KEY = "ababagalamaga"
# SECRET_KEY = os.urandom(24)


basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'urlsaver.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


WHOOSH_BASE = os.path.join(basedir, 'search.db')
WHOOSH_DISABLED = True


MAIL_SERVER = "smtp.gmail.com"
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_PORT = 587
MAIL_USERNAME = MY_MAIL_USERNAME
MAIL_PASSWORD = MY_MAIL_PASSWORD
