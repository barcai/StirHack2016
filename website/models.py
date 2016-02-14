from datetime import datetime
import json

from flask.ext.login import UserMixin
from peewee import *

from website import app, bcrypt

db = SqliteDatabase("iamverycreativeinnamingdatabases.db")


class User(Model, UserMixin):
	_id = PrimaryKeyField(primary_key=True)
	username = CharField(unique = True)
	email = CharField(unique = True)
	password = CharField()
	phone_number = CharField()
	joined_at = DateField(default = datetime.now)
	is_admin = BooleanField(default = False)

	@classmethod
	def create_user(cls, username, email, password, phone_number, admin = False):
		cls.create(
			username = username,
			email = email,
			password = bcrypt.generate_password_hash(password),
			phone_number = phone_number,
			is_admin = admin
			)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return int(self._id)

	class Meta:
		database = db


class Diagnostic(Model, UserMixin):
	date = DateField(default = datetime.now, unique = True)
	diag = TextField()

	@classmethod
	def create_diag(cls, diag):
		cls.create(diag = json.dumps(diag))

	class Meta:
		database = db


def create_tables():
	db.connect()
	db.create_tables([User, Diagnostic], safe = True)
	db.close()


def check_pass(username, password):
	return bcrypt.check_password_hash(User.get(User.username==username).password, password)


create_tables()
try:
	User.create_user("barcai", "udvardy.zsombor@gmail.com", "cat", "0769696969", True)
except:
	pass
print(check_pass("barcai", "cat"))