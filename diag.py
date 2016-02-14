import get_json, time, json, notifications, sqlite3
from datetime import datetime

from peewee import *

from website.models import User

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
		get = get_json.get_results()
		if get == {}:
			print("Unable to connect to API database.")
			time.sleep(60)
		else:
			Diagnostic.create_diag(get)
			print ("Diagnostics pushed to database")
			messaging(check_errors())
			time.sleep(20)

def check_errors(q_length=3):
	db.connect()
	past_entries = {}
	entry_times = {}
	
	for i in range(0, q_length):
		past_entries[i] = json.loads(Diagnostic.select().order_by(-Diagnostic.date)[i].diag)
		entry_times[i] = Diagnostic.select().order_by(-Diagnostic.date)[i].date
	api_list = past_entries[0]
	faults = {}
	for api in api_list:
		faults[api] = (api, True)
		for i in range(0, q_length):
			diag = past_entries[i][api]
			faults[api] = (api, faults[api][1] and (diag['message'] != "OK"))
		if faults[api][1] == True:
			if downtime.get(api, None) == None:
				downtime[api] = entry_times[q_length - 1].strftime("%Y-%m-%d %H:%M:%S")
			diag = past_entries[0][api]
			print("Error confirmed on: " + api + " | Downtime started: " + downtime[api] + " | Recent message: " + diag['message'])
		else:
			downtime[api] = None

	db.close()
	return faults
	
def messaging(faults):
	global up_down
	if up_down:
		for api_err in faults:
			if faults[api_err][1] == True:
				print("APIs are down.")
				send_messages(faults)
				up_down = False
				break;
	else:
		all_operational = True
		for api_err in faults:
			if faults[api_err][1] == True:
				all_operational = False
				break;
		if all_operational:
			print("Services confirmed to be back online.")
			up_down = True
		
		
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
	#print("SMS sent.")
	
	# Email
	#connection = sqlite3.connect("iamverycreativeinnamingdatabases.db")
	#cursor = connection.execute("SELECT email FROM User")
	#subject = "Dogfi.sh API Notification"
	#body = "The following APIs are down at the time this notification was sent:\n"
	#for api in mail_list:
		#body = body + api + "\n"
	#body = body + "\nThere may be more APIs which are down after the time this notification was sent. We will be working to bring these back up as soon as possible.\n\n-The Dogfi.sh Team"
	#notifications.email_notification(cursor, subject, body)
	#print("Email sent.")
		
		
create_tables()
main()
#fault = {('test1', True), ('test2', False), ('test3', True), ('test4', True)}
#send_messages(fault)