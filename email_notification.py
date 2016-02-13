import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


sender = 'stirhackdogfish@gmail.com'
password = 'SeuXtHMdBM'


def connect_to_server():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    return server


def notify(recipients):
    server = connect_to_server()
    for recipient in recipients:
        message = make_message(recipient)
        server.sendmail(sender, recipients, message)
    server.quit()


def make_message(recipient):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = '...'
    body = '...'
    msg.attach(MIMEText(body, 'plain'))
    return msg.as_string()
            
    

# if __name__ == '__main__':
#     import sys
#     notify([sys.argv[1]])

