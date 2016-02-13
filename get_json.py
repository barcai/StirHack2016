import requests, json, sys, random

username = 'thaddow'
password = 'thaddow'
authcode = 'thaddow'
errorVal = -1

def check_api_list():
    url = "http://dogfish.tech/api/apis"
    r = requests.get(url)

    if r.status_code == requests.codes.ok:
        parsed_json = r.json()
        if len(parsed_json['data']) > 0:
            return (r.status_code, parsed_json['data'])
    return (r.status_code, None)


def get_token(username, password):
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
	random_error = random.randint(0, 9)
	response = None
	if(access == "always"):
		if random_error == errorVal:
			response = requests.get(url_to_check + "?broken=1")
		else:
			response = requests.get(url_to_check)
		
	elif(access == "auth"):
		auth = "&auth=" + auth_key
		if random_error == errorVal:
			response = requests.get(url_to_check + auth + "&broken=1")
		else:
			response = requests.get(url_to_check + auth)
		

	elif(access == "token"):
		#token = "login?user=" + user_name + "&password=" + user_password
		token = get_token(user_name, user_password)
		if(token[1] != None):
			if random_error == errorVal:	
				response = requests.get(url_to_check + "&token=" + token[1] + "&broken=1")
			else:
				response = requests.get(url_to_check + "&token=" + token[1])
			

	
	message = "OK"
	returned_json = None
	try:
		returned_json = response.json()
	except:
		returned_json = None
		if response.status_code == 404:
			message = "Error: 404 Not Found"
		elif response.status_code == 500:
			message = "Error: 500 Internal Server Error"
		else:
			message = "Error: Unable to return data"

	return (response.status_code, message, returned_json)

def get_results():
	all_result = {}
	api_list = check_api_list()
	if api_list[0] == 200:
		results = {}
		for api in api_list[1]:
			api_result = check_api(api, username, password, authcode)
			api_results = {'status_code': api_result[0], 'message': api_result[1], 'returned_json': api_result[2]}
			results[api['endpoint']] = api_results
		all_result['test_result'] = results
		
	#with open('result.json', 'w') as f:
		#f.write(json.dumps(all_result))
	return json.dumps(all_result, sort_keys = True)
	
	
def main():
	#api_list = check_api_list()
	#if api_list[0] == 200:
	    #for api in api_list[1]:
			#print api['id']
			#api_status = check_api(api, username, password, authcode)
			#print(api_status)
	#else:
		#print ("Error fetching API list")
	get_results()

if __name__ == "__main__":
    main()

