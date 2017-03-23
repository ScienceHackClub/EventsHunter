#!usr/bin/env python
##
## Extractor de eventos v0.00002
## Autores:
##	Jean-Francois Kener
##	Carlos Vivar alias Kato
##

import sys, os, time, json, pickle
from modules import twitter, regex_data, helpers, nltk_parse
import feedparser

# Debug settings
debug = 1
save_files = 0
debug_path = './debug/'


# Load config.json
with open("config.json") as json_data:
    config = json.load(json_data)


# Load args (not used yet)
if len(sys.argv) > 1:
	url = sys.argv[1]

# Template
item_template = {
	'title' : None,
	'desc' : None,
	'date' : None,
	'time' : None,
	'loc' : None,
	'link' : None,
	'publisher' : None,
	'date_pub' : None,
	'price' : None,
	'corpus' : None
}
items = []


######################################################## Twitter

##----- Connect and get
if not debug:
	twitter.Auth()

	twits = [] # twit holds 'username' and 'text'
	for tw in config['twitter_accounts']:
		add_twits = twitter.GetTweets(_user=tw, _count=10)
		if add_twits:
			twits.extend(add_twits)
	print 'Total: ' + str(len(twits))

	# SAVE DEBUG FILES
	if save_files:
		with open(debug_path+'twits.pickle', 'wb') as handle:
			pickle.dump(twits, handle)
else:
	# LOAD DEBUG FILES
	try:
		with open(debug_path+'twits.pickle', 'rb') as handle:
			twits = pickle.load(handle)
	except:
		print "Please, consider saving files before debug mode"

##----- Extract infos (regex)
for tw in twits:
	new_item = dict(item_template)
	new_item['publisher'] = tw['username']
	new_item['corpus'] = tw['text']

	# Process text with custom regex for tags + NLTK
	text, backup_tags = regex_data.ProcessTags(tw['text'], replace=True)
	nltk_data = nltk_parse.nltk_extract(text, text_type="twitter")

	# Temporal unrestored first-ocurrence data
	if len(nltk_data['date']) > 0:
		new_item['date'] = nltk_data['date'][0]

	if len(nltk_data['time']) > 0:
		new_item['time'] = nltk_data['time'][0]

	if len(nltk_data['loc']) > 0:
		new_item['loc'] = nltk_data['loc'][0]

	items.append(new_item)


######################################################## Feeds

##----- Get information
if not debug:
	# Connect each site
	entries = []
	for feed in config['feeds']:
		url = feed['link']
		d = feedparser.parse( url )
		entries.extend(d.entries)
		print 'Extracted feed: ' + d.feed.title
		print 'Total: ' + str(len(d.entries)) + '\n'

		# SAVE DEBUG FILES
		if save_files:
			with open(debug_path+'feeds.pickle', 'wb') as handle:
				pickle.dump(entries, handle)
else:
	# LOAD DEBUG FILES
	try:
		with open(debug_path+'feeds.pickle', 'rb') as handle:
			entries = pickle.load(handle)
	except:
		print "Please, consider saving files before debug mode"

##----- Extract data (regex)
for item in entries:
	clean_desc = helpers.cleanhtml(item.description)

	new_item = dict(item_template)
	new_item['corpus'] = clean_desc
	new_item['title'] = helpers.cleanhtml(item.title)
	new_item['link'] = item.link
	new_item['date_pub'] = item.published

	# Process text with custom regex for tags + NLTK
	text, backup_tags = regex_data.ProcessTags(clean_desc, replace=True)
	nltk_data = nltk_parse.nltk_extract(text, text_type="rss")

	# Temporal unrestored first-ocurrence data
	if len(nltk_data['date']) > 0:
		new_item['date'] = nltk_data['date'][0]

	if len(nltk_data['time']) > 0:
		new_item['time'] = nltk_data['time'][0]

	if len(nltk_data['loc']) > 0:
		new_item['loc'] = nltk_data['loc'][0]

	items.append(new_item)

'''
## Dump
if debug:
	f = 'debug/debug_feeds.txt'
	print "Dumping file " + f
	obj = open(f, 'wb')

	for item in entries:
		obj.write(item.title.encode('utf-8') + "\n")
		obj.write(item.published.encode('utf-8') + "\n")
		obj.write(item.description.encode('utf-8') + "\n")
		obj.write(item.link.encode('utf-8') + "\n")
		for descriptor in meta[item]:
			obj.write(descriptor + ": " + meta[item][descriptor].encode('utf-8') + "\n")
		obj.write("\n\n")
	obj.close
	print "Ready\n\n\n"
'''


######################################################## Debug


##----- Print infos
if debug:
	for x in items:
		for desc in x:
			if x[desc] is not None:
				print desc + ": " + x[desc]
		print "-----------------------------------"

##------ Save infos
	f = debug_path + 'items.txt'
	print "Dumping file " + f
	obj = open(f, 'wb')
	for x in items:
		for descriptor in x:
			if x[descriptor] is not None:
				obj.write(descriptor + ": " + x[descriptor].encode('utf-8') + "\n")
		obj.write("\n\n")
	obj.close

print "Ready\n\n"
