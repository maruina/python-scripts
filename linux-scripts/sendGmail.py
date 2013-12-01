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

# Parameters
smtp_server = 'smtp.gmail.com:587'


def checkEmailAddress(address):
    """Check the email address and return False if it is invalid."""
    if '@' not in address:
        print "Error: @ missing in the email address"
        return False
    else:
        return True


def createMessaggeHeaders(fromaddr, toaddr, subject, body):
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
        '-q', '--quality',
        help=(
            " The SMS quality, can be a (automatic), h (high), "
            "l (medium), ll (low)"
        ), required=True
    )
    parser.add_argument(
        '-o', '--operation',
        help=(
            "The SMS type, can be TEXT (standard sms text), "
            "MULTI (multiple SMS interpreted as one SMS), OLGO (SMS is a "
            "Nokia operator logo), GLGO (SMS is a Nokia group logo), RING "
            "(SMS is a ringtone), 8BIT (SMS is 8 bit)"
        ), required=True
    )
    args = parser.parse_args()

    # Arguments checks
    return args


def sendGmail(fromaddr, toaddr, subject, body, username, password, smtp_server):
    """Send email via Gmail."""

    try:
        server = smtplib.SMTP(smtp_server)
    except smtplib.SMTPConnectError as e:
        print "Error: can't connect with the server"
        sys.exit(2)

    try:
        server.ehlo()
    except smtplib.SMTPHeloError as e:
        print "Error: the server didn’t reply properly to the HELO greeting"
        sys.exit(3)

    try:
        server.starttls()
    except smtplib.SMTPException as e:
        print "Error: the server does not support the STARTTLS extension."
        sys.exit(4)
    # Second ehlo() needed
    try:
        server.ehlo()
    except smtplib.SMTPHeloError as e:
        print "Error: the server didn’t reply properly to the HELO greeting"
        sys.exit(5)

    try:
        server.login(username, password)
    except smtplib.SMTPAuthenticationError as e:
        print "Error: SMTP authentication went wrong."
        sys.exit(6)

    # Check on the email addresses
    if checkEmailAddress(fromaddr) or checkEmailAddress(toaddr) is not True:
        sys.exit(8)

    # Create the messagge
    text = createMessaggeHeaders(fromaddr, toaddr, subject, body)

    try:
        server.sendmail(fromaddr, toaddr, text)
    except (smtplib.SMTPRecipientsRefused, smtplib.SMTPHeloError,
            smtplib.SMTPSenderRefused, smtplib.SMTPDataError
            ) as e:
        print "Error: %s" % e
        sys.exit(7)
    server.quit()


if __name__ == '__main__':
    print "Command line version in development"
