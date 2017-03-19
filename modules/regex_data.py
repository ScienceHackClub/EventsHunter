#!usr/bin/env python

##
## Extraer datos por regex
## (Temporal hasta AI)
## 

import re

def RegexExtractData(data):
	# Extract time
	times = []
	
	append = re.findall(r'([0-9]{1,2}[:\.][0-9]{1,2}(?:am|pm)?)', data, re.M | re.I)
	if append:
		times.extend(append)

	append = re.findall(r'a las (.+?(?:pm|am)?(?: en punto| y [^ ]+| menos [^ ]+)?)[ \.,]', data, re.M | re.I)
	if append:
		times.extend(append)

	if len(times)>3: times = times[:3]  
	times.sort(key=len)
	
	if times:
		time=times[0]
	else:
		time="Unknown"
		
	#Extract location
	locations = []
	
	append = re.findall(r'((?:En|en) (?:la|el)? ?(?:.+?))(?:\.|,|a las)', data, re.M | re.I)
	if append:
		locations.extend(append)

	if len(locations)>3: locations = locations[:3]  
	locations.sort(key=len)
	
	if locations:
		location=locations[0]
	else:
		location="Unknown"

	#Extract date
	date = re.search(r'((?:[^ ]+) de (?:[Ee]nero|[Ff]ebrero|[Mm]arzo|[Aa]bril|[Mm]ayo|[Jj]unio|[Aa]gosto|[Ss]eptiembre|[Oo]ctubre|[Nn]oviembre|[Dd]iciembre))', data, re.M | re.I)

	if date:
		date = date.group(0)
	else:
		date = "Unknown"

	#return stuff
	ret = {
		'date' : date,
		'time' : time,
		'loc'  : location
	}
	return ret




