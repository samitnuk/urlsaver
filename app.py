# this file do not used and will be delayed after some tests

from flask import Flask
from flask import Blueprint

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SERVER_NAME'] = 'urlsaver.ua:5000'

@app.route("/")
@app.route("/<path:path>")
def hello_world(path=None):
	if path:
		return "<i>Path for saving: </i>" + path
	return "This is main page!"

# Blueprint declaration
bp = Blueprint('subdomain', __name__, subdomain="<group>")

# Add a route to the blueprint
@bp.route("/")
def home(group):
    return 'Welcome to your subdomain, {}'.format(group)

# Register the blueprint into the application
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run()