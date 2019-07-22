from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
from flask_mail import Mail
from flask_migrate import Migrate



app = Flask(__name__)
app.config.from_object('config')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ztlngjrnvziegs:Ev9h62QPQYd0zyiTZipZsGbmDD@ec2-54-204-35-248.compute-1.amazonaws.com:5432/dfqlm57b31f0ab'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://iaioceqw:TrcP47je0Jh47zthPf_pvkgwfLY924ge@raja.db.elephantsql.com:5432/iaioceqw"
db = SQLAlchemy(app)
Migrate = Migrate(app, db)
mail = Mail(app)

from app import views, models


