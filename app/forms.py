from flask.ext.wtf import Form
from wtforms.fields import TextField, IntegerField, SelectField, FileField, PasswordField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Required, Length, EqualTo, ValidationError, Email, NumberRange
from app.models import User_info
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
from app import db

class Unique(object):
    """ validator that checks field uniqueness """
    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if not message:
            message = u'Email already exists'
        self.message = message

    def __call__(self, form, field):         
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)

class RegistrationForm(Form):
  fname = TextField('fname', validators=[Required(message="Required"), Length(min=2, max=79)])
  lname = TextField('lname', validators=[Required(message="Required"), Length(min=2, max=79)])
  email = TextField('Email Address', validators=[Length(min=6, max=49), Required("Required"), Email(), Unique(User_info, User_info.email)])
  confirme = TextField('Confirm Email', validators=[Required(message="Required"), EqualTo('email', message='email doesn\'t match original')])
  password = PasswordField('New Password', validators=[Required("Required"), Length(min=8, max=100)])
  confirmp = PasswordField('Confirm Password', validators=[Required(message="Required"),EqualTo('password', message='Password mismatch')])
  image = FileField('Image', validators=[Required(message="Must upload an image")])
  age = IntegerField('Age', validators=[Required(message="Required"), NumberRange(min=10,max=85, message="Only 10 - 85 year olds")])
  sex = SelectField('Sex', choices=[('Male','Boy'),('Female','Girl')], validators=[Required(message="Required")])

class SigninForm(Form):
  email = TextField("Email",  validators=[Required("Please enter your email address."), Email("Incorrect E-Mail format.")])
  password = PasswordField('Password', validators=[Required("Please enter a password.")])
  submit = SubmitField("Sign In")
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
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
      
class WishForm(Form):
  url = TextField('URL',  validators=[Required("Please enter web address.")])
  
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
    
    
class ShareForm(Form):
  name = TextField('Name', validators=[Required()])
  email = TextField('Email', validators=[Required(), Email()])
  subject = TextField('Subject', validators=[Required()])
  message = TextAreaField('Message', validators=[Required()])
  send = SubmitField('Send')
     
      
  