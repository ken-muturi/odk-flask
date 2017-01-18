import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask.ext.bcrypt import Bcrypt
from config import basedir, ADMINS

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
bcrypt = Bcrypt(app)

# modules
from app import views
from app.main.view import main_blueprint
from app.user.view import user_blueprint
from app.logger.view import logger_blueprint
app.register_blueprint(main_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(logger_blueprint)

# login
from app.user.model import User
lm.login_view = "user.login"

try:
	# log errors
	if not app.debug:
		import logging
		from logging.handlers import RotatingFileHandler
		
		# log to files
		file_handler = RotatingFileHandler('tmp/logs.log', 'a', 1 * 1024 * 1024, 10)
		file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
		app.logger.setLevel(logging.INFO)
		file_handler.setLevel(logging.INFO)
		app.logger.addHandler(file_handler)
		app.logger.info(app.config['SITE_TITLE'] + ' startup')

except ImportError:
    import sys
    print >> sys.stderr, "Please create a config.py with the necessary settings."