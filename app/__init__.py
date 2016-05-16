from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
#from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
from flask_mail import Mail



app = Flask(__name__)
app.config.from_object('config')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ztlngjrnvziegs:Ev9h62QPQYd0zyiTZipZsGbmDD@ec2-54-204-35-248.compute-1.amazonaws.com:5432/dfqlm57b31f0ab'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost/proj3"
db = SQLAlchemy(app)
mail = Mail(app)

from app import views, models


