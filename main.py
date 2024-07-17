###################################
# Required libraries
###################################
from email.message import EmailMessage
import ssl
import smtplib
from os import environ
from dotenv import load_dotenv
from time import sleep
load_dotenv()
from datetime import datetime
###################################

###################################
# Creation of SSL context
###################################
context = ssl.create_default_context()
###################################

###################################
# Sending email at the "annu sign" time
###################################
email_was_sent_for_current_hour = False

while True:
  current_date_time = datetime.now()
  current_hour = abs(current_date_time.hour - 12)
  current_minute = current_date_time.minute
  print(f'Current Hour: {current_hour} | Current minute: {current_minute}')

  if (email_was_sent_for_current_hour and (current_hour != current_minute)):
    email_was_sent_for_current_hour = False

  if (current_hour == current_minute) and not email_was_sent_for_current_hour:
    # Constants Creation & Email Msg Creation
    email_sender = environ.get('SENDER_EMAIL');
    email_password = environ.get('SENDER_PASSWORD')
    email_receiver = environ.get('RECEIVER_EMAIL');
    subject = f'NBC at {current_hour}:{current_minute}'
    body = 'lbumisu'
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
      smtp.login(email_sender, email_password)
      smtp.sendmail(email_sender, email_receiver, em.as_string())
      print('email sent')
      email_was_sent_for_current_hour = True

  sleep(5)
###################################