import http.client, urllib
from twilio.rest import TwilioRestClient
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


PUSHOVER_APP_TOKEN = 'aAckoTwkr26Ukc855pRR76T9z5jUJB'
TEST_USER_KEY = 'uMSMGNJ5MtH5265UTftx9MfkuUjqYf'
TWILIO_ACCOUNT_SID = 'AC8f016e4a9e84c6f80a4a5a41d4c6d312'
TWILIO_AUTH_TOKEN = '401f295e0d82514a42ec08a9563baa15'
EMAIL_ADDRESS = 'stirhackdogfish@gmail.com'
EMAIL_PASSWORD = 'SeuXtHMdBM'


#### PUSHOVER ####

def pushover_notification(user_key, message):
    """Send the message as a Pushover notification to the given user."""
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({
            "token": PUSHOVER_APP_TOKEN,
            "user": user_key,
            "message": message,
        }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()



#### SMS ####

def sms_notification(number, message):
    """Send sms message via Twilio to number (include country code in number, 
    for example '+447000000000')"""
    client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(body=message, to=number, from_="+441158242719")



#### EMAIL ####

def email_notification(recipients):
    server = connect_to_email_server()
    for recipient in recipients:
        message = make_email(recipient)
        server.sendmail(EMAIL_ADDRESS, recipients, message)
    server.quit()


def connect_to_email_server():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    return server


def make_email(recipient):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient
    subject, body = generate_email_content()
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    return msg.as_string()
            
    
def generate_email_content():
    # TODO
    return 'subject', 'body'



