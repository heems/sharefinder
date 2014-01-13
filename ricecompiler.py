import json
import urllib2
from bs4 import BeautifulSoup
import re

data = json.load(urllib2.urlopen("http://api.4chan.org/g/catalog.json"))
w = open('tripfilter.txt', 'r')
s = open('rice.txt', 'w')

def soupify(raw):
	raw = raw.replace("</br>", "\n")
	raw = raw.replace("</wbr>", "\n")
	raw = raw.replace("<br>", "\n")
	soup = BeautifulSoup(raw)
	line = re.sub(r">>\d+", '', soup.text)
	return line

def fTrip(trip):
	for line in w:
		if trip == line:
			return True
	return False

#def extractTag(threadno):

def printRice(threadno):
	url = "http://api.4chan.org/g/res/" + str(threadno) + ".json"
	threaddata = json.load(urllib2.urlopen(url))
	posts = threaddata['posts']
	for i in range(0, len(posts)):
		if 'trip' not in posts[i] or fTrip(posts[i]['trip']) == False:
			if 'com' in posts[i]: 
				if "pastebin" in posts[i]['com'] or "github" in posts[i]['com']:
					try:
						#if "resto" in posts[i]['com']:
							#extractTag(posts[i]['com']['resto'])
						s.write(soupify(posts[i]['com']))
					except UnicodeEncodeError:
						s.write(soupify(posts[i]['com']).encode('utf8'))
					else:
						s.write("\n")
						s.write("-------------------------------------------------")
						s.write("\n")

for i in range(0,11):
	for thread in data[i]["threads"]:
		if "sub" in thread:
			if "desktop thread" in thread["sub"]:
				print "desktop thread on page " + str(i)
				print "THREAD NO " + str(thread["no"])
				printRice(thread["no"])
		elif "com" in thread:
			if "love" in thread["com"].lower() or "desktop thread" in thread["com"].lower():
				print "desktop thread on page " + str(i)
				print "THREAD NO " + str(thread["no"])
				printRice(thread["no"])