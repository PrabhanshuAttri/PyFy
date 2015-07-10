#!/usr/bin/python

import urllib, urllib2, cookielib, os
import time
from bs4 import BeautifulSoup
import codecs
import string
import re
import subprocess

fbURL = "https://m.facebook.com/messages/?ref_component=mbasic_home_header&ref_page=%2Fwap%2Fhome.php&refid=7"
file1 = 'a.html'
delay = 5

def sendmessage(message):
    subprocess.Popen(['notify-send', message])
    return

class PyFB:
    jar = cookielib.CookieJar()
    cookie = urllib2.HTTPCookieProcessor(jar)       
    opener = urllib2.build_opener(cookie)
    myMsgs = []
    headers = {
        "User-Agent" : "Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.8.1.14) Gecko/20080609 Firefox/2.0.0.14",
        "PyFBept" : "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,text/png,*/*;q=0.5",
        "PyFBept-Language" : "en-us,en;q=0.5",
        "PyFBept-Charset" : "ISO-8859-1",
        "Content-type": "application/x-www-form-urlencoded",
        "Host": "m.facebook.com"
    }

    def login(self):
      # edit this first
    	email = 'your_email'
    	mypassword = 'your_fb_password'
        try:
        	print 'Logging into facebook...'
        	print 'Email: ' + email
        	print 'Password:',
        	print '*' * len(mypassword)

        	params = urllib.urlencode({'email':email,'pass':mypassword,'login':'Log+In'})
        	req = urllib2.Request('http://m.facebook.com/login.php?m=m&refsrc=m.facebook.com%2F', params, self.headers)
        	res = self.opener.open(req)
        	html = res.read()
        	self.fetch(fbURL)
        	time.sleep(5)
        	self.unreadmsg(file1)

        except urllib2.HTTPError, e:
			print e.msg
        except urllib2.URLError, e:
        	print e.reason[1]

        return False        

    def fetch(self,url):
    	#self.headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' }
        req = urllib2.Request(url,None,self.headers)
        res = self.opener.open(req)
        data = res.read()
        text = data.decode('utf-8')
        resfile = codecs.open(file1,'w', encoding='utf-8')
        resfile.write(text)
        resfile.close()
        return res.read()

    def unreadmsg(self, pagename):
    	theMsg = 'You have unread messages from: '
    	friends = []
    	page = urllib.urlopen(pagename).read()
    	strr = "{background-color:#eceff5"
    	pos = page.find(strr)
    	att = page[pos-2:pos]
    	print att
    	soup = BeautifulSoup(page, 'html.parser')
    	print soup.title.string
    	rows = soup.find_all('table')
    	for row in rows:
    		if (att in row['class']):
    			friends.append(row.find('a'))
    	
    	for friend in friends:
    		[s.extract() for s in friend('img')]
    		name = friend.string
    		name = re.sub(r"\([^)]*\)", '', name)
    		#print name
    		self.myMsgs.append(name)
    		theMsg += name + ", "

    	sendmessage(theMsg[:-2])
    	print self.myMsgs
    	del friends[:]

    def unRead(self, pagename):
    	print self.myMsgs
    	theMsg = 'You have recieved message from: '
    	new = []
    	friends = []
    	tmp = []
    	msg = []
    	notify = []
    	page = urllib.urlopen(pagename).read()
    	strr = "{background-color:#eceff5"
    	pos = page.find(strr)
    	att = page[pos-2:pos]
    	print att
    	soup = BeautifulSoup(page, 'html.parser')
    	print soup.title.string
    	rows = soup.find_all('table')
    	i = 0
    	for row in rows:
    		if (att in row['class']):
    			friends.append((row.find('a'),row.find('strong').find('span')))
    			msg.append(row.find('strong').find('span').string)

    	for x,y in friends:
    		[s.extract() for s in x('img')]
    		name = x.string
    		name = re.sub(r"\([^)]*\)", '', name)
    		#print name
    		if name not in self.myMsgs:
    			new.append(name)
    			theMsg += name + ", "
    			notify.append(name + " says " + y.string)
    		tmp.append(name)
    	
    	if new:
    		sendmessage(theMsg[:-2])
    		for n in notify:
    			sendmessage(n)
    	myMsgs = tmp[:]
    	del tmp[:]
    	del new[:]
    	del friends[:]
    	del msg[:]
    	del notify[:]
    	print myMsgs

pyfy = PyFB()
pyfy.login()
time.sleep(5)
while True:
	print 'Removing old files...'
	try:
		os.remove(file1)
	except OSError as e:
		print 'a.html is not present'

	print 'Fetching...'
	pyfy.fetch(fbURL)
	time.sleep(5)
	pyfy.unRead(file1)
	
	print 'Waiting (' + str(delay+5) + ' seconds)...'
	time.sleep(delay)
