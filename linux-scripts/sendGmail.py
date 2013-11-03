#! /usr/bin/env python
#
# Send a mail via Gmail
#

# Import usefull stuff
import smtplib
# Import the email modules we'll need
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import datetime

#Parametri per l'invio del messaggio
fromaddr = "notifiche@XXX.it"
toaddr = "matteo.ruina@XXX.it"
today=datetime.datetime.now()
subject = "SVN Backup report of " + str(today.year) + "-" + str(today.month) + "-" + str(today.day)
content = "Backup avvenuto con successo\n"

#Formatto il messaggio
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = subject
msg.attach(MIMEText(content, 'plain'))

#Credenziali per GMAIL
username = "AAA"
password = "BBB"

def send_mail(fromaddr,toaddr,msg):
    """Invia il messaggio"""
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username,password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    
def main():
    send_mail(fromaddr,toaddr,msg)    

if __name__ == '__main__':
    main()