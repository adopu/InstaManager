from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os


def scrap(keyword, loop, path):
	''' Scrap bing and download images in Path for the research keyword. Iterates loop times'''
	for i in range(loop):
		url =  "https://www.bing.com/images/search?&q=" + keyword + " + str(i*4) + \
		"&qft=+filterui:imagesize-large&FORM=R5IR3"
		html = requests.get(url).text
		dom = BeautifulSoup(html)
		urls = [a['src'] for a in dom.find_all("img", {"src": re.compile("mm.bing.net")})]
		for u in urls:
			raw_img = urllib2.urlopen(u).read()
			count = len([i for i in os.listdir(path)]) + 1
			f = open( path + "/selfie" + "_" + str(count), 'wb')
			f.write(raw_img)
			f.close()
