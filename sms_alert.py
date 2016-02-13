from twilio.rest import TwilioRestClient

account_sid = 'AC8f016e4a9e84c6f80a4a5a41d4c6d312'
auth_token = '401f295e0d82514a42ec08a9563baa15'

def send_alert(number, message):
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(body="Hi!", to=number, from_="+441158242719")


