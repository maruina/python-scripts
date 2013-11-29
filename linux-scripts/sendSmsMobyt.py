#! /usr/bin/env python
#
# Send a SMS via mobyt.it
#

#Import requested library library
import urllib
import urllib2
#Import sys for exit code
import sys

#Url for Mobyt service
url = 'http://smsweb.mobyt.it/sms-gw/sendsmart'
#Request dictionary
mydata = {}


def sendSmsMobyt(username, password, sender, recipient, text, quality):
    """Send a SMS via www.mobyt.it

    Arguments:
    username = your mobyt username
    password = your mobyt password
    sender = the SMS sender, can be both alphanumeric and
             international number +XXYYYYYYY
    recipient = the SMS recipient in international number +XXYYYYYYY
    text = your SMS text, can't be longer than 160 characters
    quality = quality of SMS, can be a (automatic), h (high),
              l (medium), ll (low)
    """
    mydata['id'] = username
    mydata['password'] = password
    mydata['from'] = sender
    mydata['rcpt'] = recipient
    mydata['operation'] = "TEXT"
    mydata['act'] = "1983"

    #Check the SMS maximum lenght
    if len(text) > 160:
        print "Error: mydata lenght exceeded (MAX 160)"
        sys.exit(1)
    else:
        mydata['data'] = text

    if (
        quality.lower() is 'n' or quality.lower() is 'h' or
        quality.lower() is 'l' or quality.lower() is 'll'
    ):
        mydata['qty'] = quality

    payload = urllib.urlencode(mydata)
    req = urllib2.Request(url, payload)
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    try:
        response = urllib2.urlopen(req)
    except urllib2.URLError, e:
        print "Can't connect to Mobyt: " + str(e.reason)
        sys.exit(2)
    mobyt_code = response.read()

    if str(mobyt_code).find('OK') >= 0:
        print "SMS sent successfully"
    else:
        print "ERROR. Mobyt says " + str(mobyt_code)


if __name__ == "__main__":

    sendSmsMobyt("Mobyt_user", "Mobyt_password", "Sender",
                 "Rcpt_number", "SMS text", "ll")
