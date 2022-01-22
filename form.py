from email import contentmanager
from xmlrpc.server import SimpleXMLRPCRequestHandler
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length,Email
from flask_wtf import FlaskForm

class RegisterForm(FlaskForm):
    username = StringField("Username",validators=[InputRequired(), Length(min=1,max=20)])
    password = PasswordField("Password", validators=[InputRequired(),Length(min=6,max=55)])
    email = StringField("Email", validators=[InputRequired(), Email(), Length(max=50)])
    first_name = StringField("First name", validators=[InputRequired(), Length(max=55)])
    last_name = StringField("Last name", validators=[InputRequired(), Length(max=55)])

class LoginForm(FlaskForm):
    username = StringField("Username",validators=[InputRequired(), Length(min=1,max=20)])
    password = PasswordField("Password", validators=[InputRequired(),Length(min=6,max=55)])

class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = StringField("Content", validators=[InputRequired()])  

class DeleteForm(FlaskForm):    
    """Delete form -- this form is intentionally blank."""
