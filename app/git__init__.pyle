from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
from flask_mail import Mail
from flask_migrate import Migrate



app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://url"
db = SQLAlchemy(app)
Migrate = Migrate(app, db)
mail = Mail(app)

from app import views, models


