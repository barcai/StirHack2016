import http.client, urllib

app_token = 'aAckoTwkr26Ukc855pRR76T9z5jUJB'

user_key = 'uMSMGNJ5MtH5265UTftx9MfkuUjqYf'

def pebble_alert(user_key, message):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({
            "token": app_token,
            "user": user_key,
            "message": message,
        }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()


