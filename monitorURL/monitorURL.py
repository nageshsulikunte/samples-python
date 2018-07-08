#!/usr/bin/python

import urllib2
import time
import datetime
import smtplib
from smtplib import SMTPException
DELAY=60

#Conf File
URL_CONF_FILE="url_conf"
#URL Dictionary
URLS={}
#Can run monitor.?
CAN_RUN=0
#Mail recievers
MAIL_IDS=[]
#TO LIST
tolist=""

#Build URL dictionary using the URL conf file
try:
        fp=open(URL_CONF_FILE,"r")
        fp_data=fp.readlines()
        if fp_data: #If the conf file is not empty
                #Build mail list
                MAIL_IDS=fp_data[0].replace('\n','').split(';')
                for m in MAIL_IDS:
                        tolist=tolist+m+";"
                #URLs
                for u in fp_data[1:]:
                        u=u.replace('\n','').split('=')
                        URLS[u[0]]=u[1]
                CAN_RUN=1
                print "Below URLs will be monitored.\n\t"
                for URL in URLS:
                        print "%s\t: %s" %(URL,URLS[URL])
                print "*"*30
                print "\nBelow e-mails will recieve alerts.\n"
                for email in tolist.split(';'):
                        print email
                print "*"*30
        else:
                print "\nURL conf file seems to be empty. Please add URLs to be monitored & re-run the script."
except:
        print "Unable to read URL conf file. Script will not run if this is not fixed.\nContact snagesh@temenos.com"


message = """From: URL monitor <urlmonitor@kayaka.com>
To: %s
Subject: ALERT: %s

%s

**This is a automated alert e-mail message. Do not reply.
"""

#Mailing part
def alertAdmins(tolist,what,msg,message):
        sender = 'monitor@company.com'
        receivers = MAIL_IDS
        message=message % (tolist,what,msg)
        print message

        try:
                smtpObj = smtplib.SMTP('mailhost', 25)
                smtpObj.sendmail(sender, receivers, message)
                print "Successfully sent email"
                return 1
        except SMTPException:
                print "Error: unable to send email"
                return 0

#Monitoring start
if CAN_RUN==1:
        print "\nSTARTING MONITOR...\n"
        while 1:
                for SITE in URLS.keys():
                        print datetime.datetime.now()
                        print "\tTrying to access: %s (%s)" % (SITE,URLS[SITE])
                        alert=-1
                        try:
                                response=urllib2.urlopen(URLS[SITE])
                                code=response.code
                                if code==200:
                                        print "\tACCESSING %s : OK (%s)" % (SITE,code)
                                else:
                                        print "\tACCESSING %s : NOT OK (%s)" % (SITE,code)
                                        msg="%s (%s) has returned %s code." % (SITE,URLS[SITE],code)
                                        print msg
                                        try:
                                                alert=alertAdmins(tolist,SITE,msg,message)
                                        except:
                                                print "Unable to send E-mail, check mail host setting and permission"
                        except:
                                msg= "%s (%s) is not accessible. It may be down or too slowly respondig." % (SITE,URLS[SITE])
                                print msg
                                try:
                                        alert=alertAdmins(tolist,SITE,msg,message)
                                except:
                                        print "Unable to send E-mail, check mail host setting and permission"
                        print "\tAlert mail status: %s" % (alert)
                        print "."*30
        
                print "#"*30
                time.sleep(DELAY)
