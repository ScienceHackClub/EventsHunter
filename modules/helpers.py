#!usr/bin/env python

import re
from xml.sax.saxutils import unescape # remove &...;

def cleanhtml(raw_html):
	cleanr = re.compile('<.*?>')
	text = re.sub(cleanr, '', raw_html)

	text = unescape(text) # remove &...;

	cleanr = re.compile('[\s]{2,}')
	text = re.sub(cleanr, ' ', text)
	return text
