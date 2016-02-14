import os

from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import *



# Creation of the app itself
app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'iamverycreativeinnamingdatabases.db'),
    DEBUG=True,
    SECRET_KEY="Please don't tell anyone <3",
    USERNAME='admin',
    PASSWORD='admin'
))
app.jinja_env.autoescape = False

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

from website.models import User, DoesNotExist
from website.views import app

@login_manager.user_loader
def load_user(userid):
    try:
        return User.select().where(
            User._id == int(userid)
        ).get()
    except DoesNotExist:
        return None