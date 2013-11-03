#! /usr/bin/env python
#
# Backup all SVN repo inside the given folder
#

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
remotedir="//192.168.XXX.YYY/Somefolder/svn_backup"
localdir="/mnt/svn/"
today=datetime.datetime.now()
localdirname=localdir + str(today.year) + "-" + str(today.month) + "-" + str(today.day)

#Parametri per l'invio del messaggio
fromaddr = "notifiche@XXX.it"
toaddr = "matteo.ruina@XXX.it"
subject = "SVN Backup report of " + str(today.year) + "-" + str(today.month) + "-" + str(today.day)
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

def verify_repo(dir):
    ### Return TRUE if dir is a valid SVN repository
    print "Test %s to be a valid repository" % dir
    p = subprocess.Popen(['svnadmin','verify',dir],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out = p.communicate()
    if p.returncode == 1:
        print "ERROR: %s is not a valid SVN repository. Removing from list" % dir
        return False
    elif p.returncode == 0:
        print "OK: %s is a valid SVN repository" % dir
        return True    
    
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
    
    repolist=verify_repo(dirlist)
    
    print "\n"
    print "Starting backup procedure..."
    print "\n"

    #IS the destination directory mounted?
    if os.path.ismount(localdir) == False:
        print "Mounting backup destination directory..."
        # Mount the destination directory
        p = subprocess.Popen(['mount', '-t', 'cifs', remotedir, localdir, '-o', 'username=svn,password=svn'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out = p.communicate()
        if p.returncode == 0:
            print "Directory %s successfully mounted in %s" % remotedir, localdir
    else:
       print "Directory already mounted"

    print "\n"
    print "Creating backup directory"
    if os.path.exists(localdirname):
        print "Today backup already done"
        sys.exit(3)
    else:
        os.makedirs(localdirname)
        print "Creating directory %s ... OK\n" % localdirname

    print "Starting backup...OK"

    for x in list_repo:
        localdirrepo = localdirname + "/" + os.path.basename(x)
        if os.path.exists(localdirrepo):
             print "Today backup for repo %s already done" % localdirrepo
        else:
             if os.makedirs(localdirrepo):
                 print "Directory %s created" % localdirrepo
        p = subprocess.Popen(['svnadmin', 'hotcopy', x, localdirrepo],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out = p.communicate()
        #print p.returncode
        if p.returncode == 0:
            print "Backup of repo %s - DONE" % x
        else:
            print "ERROR while backup repo %s" % x
