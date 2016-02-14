from wtforms import TextField, PasswordField, validators
from flask_wtf import Form, RecaptchaField
from flask.ext.login import UserMixin


class Login(Form, UserMixin):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

class Register(Form, UserMixin):
    username = TextField('Username', [validators.Length(min=1, max = 12)])
    password = PasswordField('Password', [
        validators.Required(),
        validators.EqualTo('confirm_password', message='Passwords do not match')
    ])
    confirm_password = PasswordField('Confirm Password')
    email = TextField('Email', [validators.Length(min=6, max=35), validators.Email()])
    phone_num = TextField("Phone Number", [validators.Required()])