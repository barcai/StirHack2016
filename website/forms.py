from wtforms import TextField, PasswordField, validators
from flask_wtf import Form, RecaptchaField


class Login(Form):
    login_user = TextField('Username', [validators.Required()])
    login_pass = PasswordField('Password', [validators.Required()])

class Register(Form):
    username = TextField('Username', [validators.Length(min=1, max = 12)])
    password = PasswordField('Password', [
        validators.Required(),
        validators.EqualTo('confirm_password', message='Passwords do not match')
    ])
    confirm_password = PasswordField('Confirm Password')
    email = TextField('Email', [validators.Length(min=6, max=35), validators.Email()])
    phone_num = TextField("Phone Number", [validators.Required()]) 
    recaptcha = RecaptchaField()