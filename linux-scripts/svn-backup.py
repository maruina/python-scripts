#! /usr/bin/env python

# Import usefull stuff
import smtplib
import os
import sys
import subprocess
import datetime

# Import the email modules we'll need
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

#Parametri per il backup
remotedir="//192.168.1.101/SharedFolder/svn_backup"
localdir="/mnt/svn/"
today=datetime.datetime.now()
localdirname=localdir + str(today.year) + "-" + str(today.month) + "-" + str(today.day)

#Parametri per l'invio del messaggio
fromaddr = "notifiche@XXX.it"
toaddr = "matteo.ruina@XXX.it"
subject = "Finex SVN Backup"
content = "Messaggio di prova\n"

#Formatto il messaggio
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = subject
msg.attach(MIMEText(content, 'plain'))

#Credenziali per GMAIL
username = "ZZZ"
password = "YYY"

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
    """Main script"""
    dirlist = []
    #Check of number of arguments
    if len(sys.argv) != 2:
        print "Argument error!!!"
        print "Usage: " + sys.argv[0] + " /FULL/PATH/WITH/SVN/REPO\n"
        sys.exit(1)
    # Read the path
    path = sys.argv[1]
    # Test if it's a valid path
    if os.path.exists(path) == False:
        print "Path doesn't exist"
        sys.exit(2)
    print "Looking for SVN repo in %s\n" % path
        # Read all subdirs
    for dirname in os.listdir(path):
        tmpdir=os.path.join(path,dirname)
        if os.path.isdir(tmpdir) == True:
            dirlist.append(tmpdir)
            print "Found a directory called " + dirname + " in" + path
            
    print "\n"
    print "Testing directory..."