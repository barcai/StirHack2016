import get_json, time, json, notifications
from datetime import datetime

from peewee import *

db = SqliteDatabase("test.db")
up_down = True
downtime = {}

class Diagnostic(Model):
	date = DateTimeField(default = datetime.now, unique = True)
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
		faults[api] = (api, True)
		for i in range(0, q_length):
			diag = json.loads(past_entries[i])[api]
			faults[api] = (api, faults[api][1] and (diag['message'] != "OK"))
		if faults[api][1] == True:
			if downtime.get(api, None) == None:
				downtime[api] = entry_times[0].strftime("%Y-%m-%d %H:%M:%S")
			print("Error confirmed on: " + api + " | Downtime started: " + downtime[api])
		else:
			downtime[api] = None

	db.close()
	return faults
		
		
def send_messages(faults):
	mail_list = []
	for api_err in faults:
		if api_err[1] == True:
			mail_list.append(api_err[0])
	
	mail_list.sort()
	message = "Dogfi.sh API Notification - the following APIs are down:\n"
	for api in mail_list:
		message = message + api + "\n"

	# SMS
	#notifications.sms_notification("+447490152593", message)
	#notifications.pushover_notification("uMSMGNJ5MtH5265UTftx9MfkuUjqYf", message)
		
		
create_tables()
main()
#fault = {('test1', True), ('test2', False), ('test3', True), ('test4', True)}
#send_messages(fault)