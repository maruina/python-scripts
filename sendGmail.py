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
# Import for parsing command line arguments
import argparse
# Import for check the smtp server
import socket


def checkEmailAddress(address):
    """Return True if it's a valid email address, otherwise return False."""
    domain = address.rsplit("@", 2)
    try:
        socket.gethostbyname(domain[1])
        return True
    except socket.gaierror as e:
        print "Error: %s is not a valid email" % address
        print e
        return False


def checkSmtpServer(smtp_server):
    """Return True if it's a valid SMTP server, otherwise return False."""
    server = smtp_server.rsplit(':')
    try:
        socket.gethostbyname(server[0])
        return True
    except socket.gaierror as e:
        print "Error: %s is not a smtp server" % smtp_server
        print e
        return False


def createMessagge(fromaddr, toaddr, subject, body):
    """Create a valid email messagge."""
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    return msg.as_string()


def parseArguments():
    parser = argparse.ArgumentParser(description='Send email via Gmail')

    # Read the arguments
    parser.add_argument(
        '-u', '--username', help='Your Gmail username', required=True
    )
    parser.add_argument(
        '-p', '--password', help='Your Mobyt password', required=True
    )
    parser.add_argument(
        '-f', '--fromaddr', help=('The sender email address'), required=True
    )
    parser.add_argument(
        '-t', '--toaddr', help=('The recipient email address'), required=True
    )
    parser.add_argument(
        '-s', '--subject', help=("The email subject"), required=True
    )
    parser.add_argument(
        '-b', '--body', help=("The email body"), required=True
    )
    parser.add_argument(
        '-m', '--smtp',
        help=("The smtp address in format ip:port"), required=True
    )

    args = parser.parse_args()

    if checkEmailAddress(args.fromaddr) is False:
        sys.exit(6)
    if checkEmailAddress(args.toaddr) is False:
        sys.exit(7)
    # Check the SMTP server
    if checkSmtpServer(args.smtp) is False:
        sys.exit(8)

    return args


def sendGmail(username, password, smtp_server, fromaddr, toaddr, subject, body):
    """Send email via Gmail."""

    try:
        server = smtplib.SMTP(smtp_server)
    except smtplib.SMTPConnectError as e:
        print "Error: cant connect with the server"
        print e
        sys.exit(1)

    try:
        server.ehlo()
    except smtplib.SMTPHeloError as e:
        print "Error: the server didnt reply properly to the HELO greeting"
        print e
        sys.exit(2)

    try:
        server.starttls()
    except smtplib.SMTPException as e:
        print "Error: the server does not support the STARTTLS extension."
        print e
        sys.exit(3)

    # Second ehlo() needed
    try:
        server.ehlo()
    except smtplib.SMTPHeloError as e:
        print "Error: the server didnt reply properly to the HELO greeting"
        print e
        sys.exit(4)

    try:
        server.login(username, password)
    except smtplib.SMTPAuthenticationError as e:
        print "Error: SMTP authentication went wrong."
        print e
        sys.exit(5)

    # Check the email addresses
    if checkEmailAddress(fromaddr) is False:
        sys.exit(6)
    if checkEmailAddress(toaddr) is False:
        sys.exit(7)
    # Check the SMTP server
    if checkSmtpServer(smtp_server) is False:
        sys.exit(8)
    # Create the messagge
    text = createMessagge(fromaddr, toaddr, subject, body)

    try:
        server.sendmail(fromaddr, toaddr, text)
    except (smtplib.SMTPRecipientsRefused, smtplib.SMTPHeloError,
            smtplib.SMTPSenderRefused, smtplib.SMTPDataError
            ) as e:
        print "Error: %s" % e
        sys.exit(9)

    server.quit()
    return True


if __name__ == '__main__':

    # Parse the script's arguments
    args = parseArguments()

    # Send the SMS
    if sendGmail(args.username, args.password, args.smtp, args.fromaddr,
                 args.toaddr, args.subject, args.body) is True:
        print "OK: email sent succesfully."
