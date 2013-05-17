#TODO
#add trip filter maybe in a list in an external txt file

import json
import urllib2
from bs4 import BeautifulSoup
import re

data = json.load(urllib2.urlopen("http://api.4chan.org/mu/catalog.json"))
w = open('whitelist.txt', 'r')

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


def printShares(threadno):
	url = "http://api.4chan.org/mu/res/" + str(threadno) + ".json"
	threaddata = json.load(urllib2.urlopen(url))
	posts = threaddata['posts']
	for i in range(0, len(posts)):
		if 'trip' not in posts[i] or fTrip(posts[i]['trip']) == False:
			if 'com' in posts[i] and "youtube" in posts[i]['com']:
				print soupify(posts[i]['com'])
				print "-------------------------------------------------"

for i in range(0,11):
	for thread in data[i]["threads"]:
		if "sub" in thread:
			if "sharethread" in thread["sub"]:
				print "sharethread on page " + str(i)
				print "THREAD NO " + str(thread["no"])
				printShares(thread["no"])
		elif "com" in thread:
			if "sharethread" in thread["com"].lower():
				print "sharethread on page " + str(i)
				print "THREAD NO " + str(thread["no"])
				printShares(thread["no"])