from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, SelectField, FileField, PasswordField, SubmitField, TextAreaField
# from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError, Email, NumberRange
from app.models import User_info
# from flask_login import LoginManager, login_required, login_user, logout_user, current_user
# from app import db

class Unique(object):
    """ validator that checks field uniqueness """
    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if not message:
            message = 'Email already exists'
        self.message = message

    def __call__(self, form, field):         
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)

class RegistrationForm(FlaskForm):
  fname = StringField('fname', validators=[InputRequired(message="Required"), Length(min=2, max=79)])
  lname = StringField('lname', validators=[InputRequired(message="Required"), Length(min=2, max=79)])
  email = StringField('Email Address', validators=[Length(min=6, max=49), InputRequired("Required"), Email(), Unique(User_info, User_info.email)])
  confirme = StringField('Confirm Email', validators=[InputRequired(message="Required"), EqualTo('email', message='email doesn\'t match original')])
  password = PasswordField('New Password', validators=[InputRequired("Required"), Length(min=8, max=100)])
  confirmp = PasswordField('Confirm Password', validators=[InputRequired(message="Required"),EqualTo('password', message='Password mismatch')])
  image = FileField('Image', validators=[InputRequired(message="Must upload an image")])
  age = IntegerField('Age', validators=[InputRequired(message="Required"), NumberRange(min=10,max=85, message="Only 10 - 85 year olds")])
  sex = SelectField('Sex', choices=[('Male','Boy'),('Female','Girl')], validators=[InputRequired(message="Required")])

class SigninForm(FlaskForm):
  email = StringField("Email",  validators=[InputRequired("Please enter your email address."), Email("Incorrect E-Mail format.")])
  password = PasswordField('Password', validators=[InputRequired("Please enter a password.")])
  submit = SubmitField("Sign In")
   
  def __init__(self, *args, **kwargs):
    FlaskForm.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not FlaskForm.validate(self):
      return False
     
    user = User_info.query.filter_by(email = self.email.data.lower()).first()
    if user and user.check_password(self.password.data):
      return True
    elif not user:
      self.email.errors.append("Invalid E-Mail")
      return False
    else:
      self.password.errors.append("Invalid Password")
      return False
      
class WishForm(FlaskForm):
  url = StringField('URL',  validators=[InputRequired("Please enter web address.")])
  
  def __init__(self, *args, **kwargs):
    FlaskForm.__init__(self, *args, **kwargs)
    
    
class ShareForm(FlaskForm):
  name = StringField('Name', validators=[InputRequired()])
  email = StringField('Email', validators=[InputRequired(), Email()])
  subject = StringField('Subject', validators=[InputRequired()])
  message = TextAreaField('Message', validators=[InputRequired()])
  send = SubmitField('Send')
