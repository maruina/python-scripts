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