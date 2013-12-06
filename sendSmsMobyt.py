#!/usr/bin/env python
#
# Send a SMS via mobyt.it
#
# Created by Matteo Ruina
# mr@matteoruina.com
# License GPLv3
#
# For the latest script version go to:
# https://github.com/maruina/python-scripts

# To use it as a module in your script:
# import sendSmsMobyt
# and then use
# sendSmsMobyt.sendSms(username, password, sender, recipient,
#            text, quality, operation)


# Import requested library
import urllib
import urllib2
# Import sys for exit codes
import sys
# Import for Act calculation
import datetime
# Import for parsing command line arguments
import argparse

# Url for Mobyt service
url = 'http://smsweb.mobyt.it/sms-gw/sendsmart'
# Dictionary for storing request to Mobyt
mydata = {}
# HTTP POST header
header = {'Content-type': 'application/x-www-form-urlencoded'}

operation_dictionary = {
    'TEXT': "TEXT",
    'MULTI': "MULTI",
    'OLGO': "OLGO",
    'RING': "RING",
    '8BIT': "8BIT"
}

quality_dictionary = {
    'n': "n",
    'h': "h",
    'l': "l",
    'll': "ll"
}


def checkSender(sender):
    """"""
    if sender[:1] is '+' and len(sender) > 17:
        print "Error: sender number too long (max lenght 16)"
        return False
    elif len(sender) > 12:
        print "Error: sender name too long (max lenght 11)"
        return False
    else:
        return True


def checkSmsLenght(text):
    """Return False is the SMS text doesn't meet Mobyt's requirements."""
    if len(text) > 160:
        print 'Error: SMS text too long (max 160)'
        return False
    else:
        return True


def checkSmsQuality(quality):
    """Return False is the SMS quality doesn't meet Mobyt's requirements."""
    if quality in quality_dictionary:
        return True
    else:
        print 'Error: wrong SMS quality (choose from n, h, l, ll)'
        return False


def checkSmsOperation(operation):
    """Return False is the SMS operation doesn't meet Mobyt's requirements."""
    if operation in operation_dictionary:
        return True
    else:
        print 'Error: wrong SMS operation'
        return False


def getSmsAct():
    """Return a timestamp for the Act field."""
    now = datetime.datetime.now()
    act = (
        str(now.year) + str(now.month) + str(now.day) + str(now.hour) +
        str(now.minute) + str(now.second)
    )
    return act


def parseArguments():
    parser = argparse.ArgumentParser(description='Send SMS via Mobyt.it')

    # Read the arguments
    parser.add_argument(
        '-u', '--username', help='Your Mobyt username', required=True
    )
    parser.add_argument(
        '-p', '--password', help='Your Mobyt password', required=True
    )
    parser.add_argument(
        '-s', '--sender',
        help=(
            'The sender name, can be either alphanumeric (max lenght 11) or '
            'an international number +XXYYYYYYYYYY (max lenght 16)'
        ), required=True
    )
    parser.add_argument(
        '-r', '--recipient',
        help=(
            'The recipient number in international format +XXYYYYYYYYYY'
        ), required=True
    )
    parser.add_argument(
        '-t', '--text',
        help=(
            "The SMS text between " ", can't be longer than 160 characters"
        ), required=True
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
    if checkSender(args.sender) is False:
        sys.exit(2)
    if checkSmsLenght(args.text) is False:
        sys.exit(3)
    if checkSmsQuality(args.quality) is False:
        sys.exit(4)
    if checkSmsOperation(args.operation) is False:
        sys.exit(5)

    return args


def sendSms(username, password, sender, recipient,
            text, quality, operation):
    """Send a SMS via www.mobyt.it using POST method

    Arguments:
    username = your Mobyt username
    password = your Mobyt password
    sender = the sender name, can be either alphanumeric (max lenght 11) or an
             international number +XXYYYYYYYYYY (max lenght 16)
    recipient = the recipient number in international format +XXYYYYYYYYYY
    text = the SMS text, can't be longer than 160 characters
    quality = quality of SMS, can be a (automatic), h (high),
              l (medium), ll (low)
    operation = specify the SMS type, can be TEXT (standard sms text),
                MULTI (multiple SMS interpreted as one SMS), OLGO (SMS is a
                Nokia operator logo), GLGO (SMS is a Nokia group logo), RING
                (SMS is a ringtone), 8BIT (SMS is 8 bit)

    Return True is everything is fine.
    """
    mydata['id'] = username
    mydata['password'] = password
    mydata['from'] = sender
    mydata['rcpt'] = recipient
    if checkSmsOperation(operation) is True:
        mydata['operation'] = operation
    else:
        return False
    mydata['act'] = getSmsAct()
    if checkSmsLenght(text) is True:
        mydata['data'] = text
    else:
        return False
    if checkSmsQuality(quality) is True:
        mydata['qty'] = quality
    else:
        return False

    # Create the POST messagge and send it
    payload = urllib.urlencode(mydata)
    req = urllib2.Request(url, payload, header)
    try:
        response = urllib2.urlopen(req)
    except urllib2.URLError, e:
        print "Error: can't connect to Mobyt " + str(e.reason)
        return False

    # Read Mobyt response
    mobyt_response = response.read()
    mobyt_response_string = ''.join(mobyt_response)
    if mobyt_response_string.find('OK') >= 0:
        print (
            '* SMS sent successfully and costed %s credits'
            % mobyt_response_string.replace('OK ', '')
        )
        return True
    else:
        print 'Error: Mobyt says ' + mobyt_response_string
        return False

# Run as a standalone python script
if __name__ == '__main__':

    # Parse the script's arguments
    args = parseArguments()

    # Send the SMS
    if sendSms(args.username, args.password, args.sender,
               args.recipient, args.text, args.quality, args.operation
               ) is False:
            sys.exit(1)
