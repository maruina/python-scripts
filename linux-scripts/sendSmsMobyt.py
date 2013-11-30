#!/usr/bin/env python
#
# Send a SMS via mobyt.it
#

#Import requested library
import urllib
import urllib2
#Import sys for exit codes
import sys
#Import for Act calculation
import datetime

#Url for Mobyt service
url = 'http://smsweb.mobyt.it/sms-gw/sendsmart'
#Dictionary for storing request to Mobyt
mydata = {}
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


def checkSmsLenght(text):
    #Check the SMS maximum lenght
    if len(text) > 160:
        print 'Error: SMS text too long (max 160)'
        sys.exit(1)
    else:
        return text


def checkSmsQuality(quality):
    # Check the quality option
    if quality.lower() in quality_dictionary:
        return quality.lower()
    else:
        print 'Error: wrong SMS quality (choose from n, h, l, ll)'
        sys.exit(3)


def checkSmsOperation(operation):
    if str(operation).upper() in operation_dictionary:
        return str(operation).upper()
    else:
        print 'Error: wrong SMS operation'
        sys.exit(5)


def getSmsAct():
    now = datetime.datetime.now()
    act = (
        str(now.year) + str(now.month) + str(now.day) + str(now.hour) +
        str(now.minute) + str(now.second)
    )
    return act


def sendSmsMobyt(username, password, sender, recipient,
                 text, quality, operation):
    """Send a SMS via www.mobyt.it using POST method

    Arguments:
    username = your mobyt username
    password = your mobyt password
    sender = the SMS sender, can be both alphanumeric and
             international number +XXYYYYYYY
    recipient = the SMS recipient in international number +XXYYYYYYY
    text = your SMS text, can't be longer than 160 characters
    quality = quality of SMS, can be a (automatic), h (high),
              l (medium), ll (low)
    operation = specify the SMS type, can be TEXT (standard sms text),
                MULTI (multiple SMS interpreted as one SMS), OLGO (SMS is a
                Nokia operator logo), GLGO (SMS is a Nokia group logo), RING
                (SMS is a ringtone), 8BIT (SMS is 8 bit)
    """
    mydata['id'] = username
    mydata['password'] = password
    mydata['from'] = sender
    mydata['rcpt'] = recipient
    mydata['operation'] = checkSmsOperation(operation)
    mydata['act'] = getSmsAct()
    mydata['data'] = checkSmsLenght(text)
    mydata['qty'] = checkSmsQuality(quality)

    # Create the POST messagge and send it
    payload = urllib.urlencode(mydata)
    req = urllib2.Request(url, payload, header)
    try:
        response = urllib2.urlopen(req)
    except urllib2.URLError, e:
        print "Error: can't connect to Mobyt " + str(e.reason)
        sys.exit(2)
    mobyt_code = response.read()

    # Read Mobyt response
    if str(mobyt_code).find('OK') >= 0:
        print 'SMS sent successfully'
    else:
        print 'Error: Mobyt says ' + str(mobyt_code)
        sys.exit(4)

# Run as a standalone python script
if __name__ == '__main__':

    sendSmsMobyt('Mobyt_user', 'Mobyt_password', 'Sender',
                 'Rcpt_number', 'SMS text', 'll')
