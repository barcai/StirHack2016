import requests, json, sys

def checkAPIList():
    url = "http://dogfish.tech/api/apis"
    r = requests.get(url)

    if r.status_code == 500:
        print ("500 Internal Server Error")
    elif r.status_code == 404:
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
        auth = "&" + auth_key
        response = requests.get(url_to_check)

    elif(access == "token"):
        #token = "login?user=" + user_name + "&password=" + user_password
        token = getToken(user_name, user_password)
        if(token[1] != None):
            response = requests.get(url_to_check + "&token=" + token[1])


    api_status = None

    if(response.status_code == 500):
        api_status = "Error 500"

    elif(response.status_code == 404):
        api_status = "Error 404"

    elif(response.status_code == 200):
        api_status = "OK"

    return api_status

def main():
    for api in checkAPIList():
        print api
        api_status = check_api(api, "thaddow", "thaddow", "thaddow")
        print(api_status)
    #print(getToken('thaddow', 'thaddow'))

if __name__ == "__main__":
    main()

