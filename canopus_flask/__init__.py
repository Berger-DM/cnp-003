from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin


application = Flask(__name__)

application.config['SECRET_KEY'] = 'secretkey'
application.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///canopusflask.db"
application.config['UPLOAD_FOLDER'] = '.\\static\\images'
application.config['FLASK_ADMIN_SWATCH'] = 'darkly'

db = SQLAlchemy(application)
bcrypt = Bcrypt(application)
login_manager = LoginManager()
admin_manager = Admin(application, template_mode='bootstrap3')

application.app_context().push()
login_manager.init_app(application)

from canopus_flask import routes
