from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///canopusflask.db"
# app.config['SQLALCHEMY_DATABASE_URI'] =
# "mysql+mysqlconnector://admin:admin123@database-canopus-003.cok0ixj3xw0j.us-east-1.rds.amazonaws.com:3306/" \
#

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

app.app_context().push()

from canopus_flask import routes
