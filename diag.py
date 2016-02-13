import get_json, time, json
from datetime import datetime

from peewee import *

db = SqliteDatabase("test.db")

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
	db.create_tables([Diagnostic], safe = True)
	db.close()

def main():
	while True:
		Diagnostic.create_diag(get_json.get_results())
		print ("Diagnostics pushed to database")
		time.sleep(60)
		
create_tables()
main()