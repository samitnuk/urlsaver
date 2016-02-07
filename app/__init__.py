from flask import Flask, Blueprint
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

# for work with Jade Template Engine
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

# Blueprint declaration
bp = Blueprint('subdomain', __name__, subdomain="<groupname>")

db = SQLAlchemy(app)
# db.create_all()

from app import views, models
