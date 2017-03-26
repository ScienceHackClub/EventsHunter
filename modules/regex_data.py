# -*- coding: utf-8 -*-
#!usr/bin/env python

##
## Prepara el texto sustituyendo valores por tags para facilitar
## el funcionamiento de NLTK, y posteriormente restaura los tags
## en los named entities devueltos de nltk_parse.py
##
## Author: Jean-Francois
##

import re

def PrepareText(data_in, replace=True):
	data = {
		'TIME_TAG' : [],
		'DATE_TAG'	:	[],
		'PRICE_TAG' : [],
		'NUMBER_TAG' : [],
		'HASH_TAG' : [],
		'LINK_TAG' : []
	}

	# Extract hashtags
	pattern = r'([\#\@][^\ ]{3,})'
	append = re.findall(pattern, data_in, re.M | re.I)
	if append:
		data['HASH_TAG'].extend(append)
	if replace:
		data_in = re.sub(pattern,'HASH_TAG',data_in, 100)

	# Extract links
	pattern = r'((?:http[s]?\:\/\/|www\.|http[s]\:\/\/www\.)[^\ ]+)'
	append = re.findall(pattern, data_in, re.M | re.I)
	if append:
		data['LINK_TAG'].extend(append)
	if replace:
		data_in = re.sub(pattern,'LINK_TAG',data_in, 100)

	# Extract times
	pattern = r'([0-9]{1,2}[:\.][0-9]{2}(?:am|pm)?)'
	append = re.findall(pattern, data_in, re.M | re.I)
	if append:
		data['TIME_TAG'].extend(append)
	if replace:
		data_in = re.sub(pattern,'TIME_TAG',data_in, 100)

	pattern = r'a las (.+?(?:pm|am)?(?: en punto| y [^ ]+| menos [^ ]+)?)[ \.,]'
	append = re.findall(pattern, data_in, re.M | re.I)
	if append:
		data['TIME_TAG'].extend(append)
	if replace:
		data_in = re.sub(pattern,'TIME_TAG',data_in, 100)

	# Extract dates
	pattern = r'((?:[^ ]+) de (?:[Ee]nero|[Ff]ebrero|[Mm]arzo|[Aa]bril|[Mm]ayo|[Jj]unio|[Aa]gosto|[Ss]eptiembre|[Oo]ctubre|[Nn]oviembre|[Dd]iciembre))'
	date = re.search(pattern, data_in, re.M | re.I)
	if date:
		data['DATE_TAG'].append(date.group(0))
	if replace:
		data_in = re.sub(pattern,'DATE_TAG',data_in, 100)

	# Extract prices
	pattern = r'([0-9]+[\.\'\,]?[0-0]+ (?:euro|euros|dólar|dólares|[\€\$]))'
	append = re.findall(pattern, data_in, re.M | re.I)
	if append:
		data['PRICE_TAG'].extend(append)
	if replace:
		data_in = re.sub(pattern,'PRICE_TAG',data_in, 100)

	# Extract numbers
	pattern = r'([0-9]+)'
	append = re.findall(pattern, data_in, re.M | re.I)
	if append:
		data['NUMBER_TAG'].extend(append)
	if replace:
		data_in = re.sub(pattern,'NUMBER_TAG',data_in, 100)

	return data_in, data #data_in = text, data = tags

##
NE_TAG = {
        "loc" : ['HASH_TAG','LINK_TAG','NUMBER_TAG'],
        "date" : ['DATE_TAG', 'TIME_TAG','NUMBER_TAG'],
        "time" : ['TIME_TAG','NUMBER_TAG'],
        "person" : ['HASH_TAG','LINK_TAG'],
        "price" : ['PRICE_TAG','NUMBER_TAG'],
        "title" : ['PRICE_TAG','NUMBER_TAG','HASH_TAG','LINK_TAG'],
        "org" : ['HASH_TAG','LINK_TAG']
}


## Restore tags on original text
def RestoreTags(nltk_data, text, backup_tags):
	global NE_TAG
	new_data = {
        "loc" : [],
        "date" : [],
        "time" : [],
        "person" : [],
        "price" : [],
        "title" : [],
        "org" : []
    }
	for ne_type in nltk_data:
		for ne in nltk_data[ne_type]:
			val = ne[0]

			tag_limit = ne[1]+3
			tag_index = text.count(ne_type, 0, tag_limit)
			'''
			if ne[0].count('El DATE_TAG') > 0:
				print "here--------------------------------------"
				print nltk_data
				print text
				print backup_tags
			'''
			for tag_type in NE_TAG[ne_type]:
				tag_number = ne[0].count(tag_type)
				for i in xrange(tag_number):
					#try:
					tag_restore = backup_tags[tag_type][tag_index+i]
					val = val.replace(tag_type, tag_restore, 1)
					#except:
					#	print "Bug restoring tag data"
					#	pass
			new_data[ne_type].append(val)
	return new_data
