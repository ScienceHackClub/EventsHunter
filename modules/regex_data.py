# -*- coding: utf-8 -*-
#!usr/bin/env python

## UNFINISHED
## Text preprocessing
## - Separa comas, interrogantes, dospuntos, exc,etc (y puntos?) de palabras
## - Extracts dates,times,prices,numbers by regex, hashtags, links, etc
## and prepares TAGs for NLTK parse
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

## Restore tags on original text
def RestoreTags(text, backup):
	for it in backup: # it = TAGS
		for el in it: # el = backup data
			text = text.replace(it, el)


## bruteforce restoration (temporal)
## THIS IS BUGGY. A SENTENCE COULD BE IN TWO PLACES
## TO DO: SAVE TAG POSITION IN NLTK PROCESSING
def RestoreEntity(sent, text, backup, tag_type):
	i=0
	for el in backup[tag_type]: # el = backup data
		test_sent = sent.replace(tag_type, el)
		found = text.find(sent)
		if found!=-1:
			regex = '^((.*?'+tag_type+'.*?){' + i + '})'+tag_type
			text = re.sub(regex, el, text)
		i+=1
