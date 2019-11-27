# takes a send time & day and sets a timer 
# to send email at that time

import csv
import smtplib, imaplib
global sender
# print "preparing to send message..."
from datetime import datetime
from threading import Timer
import threading



send_day = time_now.day # + number of days
send_hour = 19
send_minute = 27
recipient = 'chiabingtian@uchicago.edu'


time_now = datetime.today()
send_time = time_now.replace(day=send_day, hour=send_hour, minute=send_minute, second=50, microsecond=0)
time_diff = send_time - time_now
secs=time_diff.seconds+1


SMTP_SERVER = 'smtp-mail.outlook.com'
# SMTP_SERVER = 'smtp.aol.com'
# SMTP_SERVER = 'smtp.gmail.com'

# outlook
SMTP_PORT = 587

# aol
# SMTP_PORT = 465

# gmail
# SMTP_PORT = 25

send_from = 'ridevidetester@outlook.com'
# send_from = 'ridevideteste@aol.com'
# send_from = 'ridevidetester@gmail.com'
password = 'ilct2019'
# password = 'ilctech2019'
subject = 'RideVide: Your Upcoming Ride'


# print "Send to: "

       #"Content-Type: text/html"]
        #to send html

def sendemail(input):
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(send_from, password)
    headers = ["From: " + send_from,
           "Subject: " + subject,
           "To: " + input[1],
           "MIME-Version: 1.0",
           "Content-Type: text/plain"]
    headers = "\r\n".join(headers)
    body = "Hello {}, your ride is schedued at {} on {}. The pickup point is {}.".format(input[0], input[3], input[2], input[4])
    session.sendmail(send_from, input[1], headers + "\r\n\r\n" + body)
    session.quit()

def sendthemail():
    print("Sending Emails...")
    with open('database.csv', encoding = 'utf-8-sig') as db_file:
        csv_reader = csv.reader(db_file, delimiter=',')
        line_count = 1
        for row in csv_reader:
            sendemail(row)
            print("Sent!")

t = Timer(secs, sendthemail)
t.start()