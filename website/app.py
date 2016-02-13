import os

from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager


# Creation of the app itself
app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'iamverycreativeinnamingdatabases.db'),
    DEBUG=True,
    SECRET_KEY="Please don't tell anyone <3",
    USERNAME='admin',
    PASSWORD='admin'
))


bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)


if __name__  == "__main__":
	app.run(host = "0.0.0.0", port= 8888, debug = True)