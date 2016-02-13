from datetime import datetime
import json

from flask.ext.bcrypt import Bcrypt
from peewee import *

from app import *


bcrypt = Bcrypt(app)
db = SqliteDatabase("iamverycreativeinnamingdatabases.db")


class User(Model):
	username = CharField(unique = True)
	email = CharField()
	password = CharField()
	phone_number = CharField()
	joined_at = DateField(default = datetime.now)

	@classmethod
	def create_user(cls, username, email, password, phone_number):
		cls.create(
			username = username,
			email = email,
			password = bcrypt.generate_password_hash(password),
			phone_number = phone_number)

	class Meta:
		database = db


class Diagnostic(Model):
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


if __name__ == "__main__":
	create_tables()
	try:
		User.create_user("a", "a@a.com", "cat", "0769696969")
	except:
		pass
	print(User.select().where())