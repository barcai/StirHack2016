from datetime import datetime
import json

from peewee import *

from app import *

db = SqliteDatabase("iamverycreativeinnamingdatabases.db")


class User(Model):
	username = CharField(unique = True)
	email = CharField()
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


def check_pass(username, password):
	return bcrypt.check_password_hash(User.get(User.username==username).password, password)



if __name__ == "__main__":
	create_tables()
	try:
		User.create_user("barcai", "udvardy.zsombor@gmail.com", "cat", "0769696969", True)
	except:
		pass
	print(check_pass("barcai", "cat"))