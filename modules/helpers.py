#!usr/bin/env python

try:
	from BeautifulSoup import BeautifulSoup
	use_bs = True
except:
	import re
	use_bs = False

def cleanhtml(raw_html):
	global use_bs
	if use_bs:
		return BeautifulSoup(raw_html).text
	else:
		cleanr = re.compile('<.*?>')
		return re.sub(cleanr, '', raw_html)
