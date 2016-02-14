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
		check_errors()
		time.sleep(1)

def check_errors(q_length=3):
	db.connect()
	past_entries = {}
	entry_times = {}
	
	for i in range(0, q_length):
		past_entries[i] = json.loads(Diagnostic.select().order_by(-Diagnostic.date)[i].diag)
		entry_times[i] = Diagnostic.select().order_by(-Diagnostic.date)[i].date
		
	api_list = json.loads(past_entries[0])
	faults = {}
	for api in api_list:
		faults[api] = True
		for i in range(0, q_length):
			diag = json.loads(past_entries[i])[api]
			faults[api] = faults[api] and (diag['message'] != "OK")
		if faults[api] == True:
			print("Error confirmed on: " + api)	
	db.close()
	return faults
		
create_tables()
main()