import os

#/ GENERAL SETTINGS /--------------------------------------------------------
DEBUG = True
SERVER_NAME = 'urlsaver.ua:5000'


#/ FOR FORMS /---------------------------------------------------------------
CSRF_ENABLED = True
SECRET_KEY = 'ababagalamagaababagalamaga'


#/ FOR DATABASE /------------------------------------------------------------
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'urlsaver.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

SQLALCHEMY_TRACK_MODIFICATIONS = False
# http://flask-sqlalchemy.pocoo.org/2.1/config/#configuration-keys

#/ FOR ERRORS /--------------------------------------------------------------
# ERROR_PAGE_NUM = 'Unfortunately page with number %s does not exist.'
ERROR_404 = 'What you were looking for is just not there.'