import requests, json, sys

def checkAPIList():
	url = "http://dogfish.tech/api/apis"
	r = requests.get(url)
	
	if r.status_code == "500":
		print ("500 Internal Server Error")
	elif r.status_code == "404":
		print ("404 Not Found")
	else:
		parsed_json = r.json()
		return parsed_json['data']
	return
	
def getToken(username, password):
	url = "http://dogfish.tech/api/login"
	loginInfo = {'user': username, 'password': password}
	r = requests.get(url, params=loginInfo)
	if r.status_code == requests.codes.ok:
		parsed_json = r.json()
		if len(parsed_json['data']) > 0:
			return (r.status_code, parsed_json['data']['token'])
	return (r.status_code, None)
	

	

for api in checkAPIList():
	print api
print(getToken('thaddow', 'thaddow'))

