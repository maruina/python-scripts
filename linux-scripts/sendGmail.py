#! /usr/bin/env python
#
# Send a mail via Gmail
#

# Import usefull stuff
import smtplib
# Import the email modules we need
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
# Import sys for exit codes
import sys

# Parameters
fromaddr = "notifiche@XXX.it"
toaddr = "matteo.ruina@XXX.it"
subject = "My subject"
content = "My beautiful email body"


# GMAIL credential
username = "AAA_change_me"
password = "BBB_change_me"
smtp_server = 'smtp.gmail.com:587'


def checkEmailAddress(address):
    if '@' not in address:
        print "Error: @ missing in FROM email address"
        sys.exit(1)


def createMessagge(fromaddr, toaddr, subject):
    # Format messagge
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
    msg.attach(MIMEText(content, 'plain'))

    return msg.as_string()


def sendGmail(fromaddr, toaddr, msg, username, password, smtp_server):
    """Invia il messaggio"""
    server = smtplib.SMTP(smtp_server)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    text = createMessagge(fromaddr, toaddr, subject)
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


if __name__ == '__main__':
    print 'ciao'
