import requests, json, sys

def checkAPIList():
    url = "http://dogfish.tech/api/apis?broken=1"
    r = requests.get(url)

    if r.status_code == requests.codes.ok:
        parsed_json = r.json()
        if len(parsed_json['data']) > 0:
            return (r.status_code, parsed_json['data'])
    return (r.status_code, None)


def getToken(username, password):
    url = "http://dogfish.tech/api/login"
    loginInfo = {'user': username, 'password': password}
    r = requests.get(url, params=loginInfo)
    if r.status_code == requests.codes.ok:
        parsed_json = r.json()
        if len(parsed_json['data']) > 0:
            return (r.status_code, parsed_json['data']['token'])
    return (r.status_code, None)


def check_api(api_data, auth_key, user_name, user_password):
	endpoint = api_data["endpoint"]
	access = api_data["access"]
	params = api_data["params"]
	url_to_check = "http://dogfish.tech/api/" + endpoint + "/" + params
	
	# Make a test call to the given API
	response = None
	if(access == "always"):
		response = requests.get(url_to_check)

	elif(access == "auth"):
		auth = "&auth=" + auth_key
		response = requests.get(url_to_check + auth + "&broken=1")

	elif(access == "token"):
		#token = "login?user=" + user_name + "&password=" + user_password
		token = getToken(user_name, user_password)
		if(token[1] != None):
			response = requests.get(url_to_check + "&token=" + token[1] + "&broken=1")

	returned_json = None
	try:
		returned_json = response.json()
	except:
		returned_json = None
	
	return (response.status_code, returned_json)

def main():
	api_list = checkAPIList()
	if api_list[0] == 200:
	    for api in checkAPIList()[1]:
			print api['id']
			api_status = check_api(api, "thaddow", "thaddow", "thaddow")
			print(api_status)
	else:
		print ("Error fetching API list")

if __name__ == "__main__":
    main()

