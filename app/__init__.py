from flask import Flask, Blueprint
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

# Blueprint declaration
bp = Blueprint('subdomain', __name__, subdomain="<groupname>")

db = SQLAlchemy(app)
# db.create_all()

from app import views, models
