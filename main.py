#!usr/bin/env python

##
## Extractor de eventos v0.00001
## Autores: 
##	Jean-Francois Kener
##	Carlos Vivar
##

import sys, os, time, json
from modules import twitter, regex_data
import feedparser

debug = 1


# Load config.json
try:
	with open("config.json") as json_data:
	    config = json.load(json_data)
except:
	pass

if not config:
	print "Problem loading config.json"
	sys.exit(0)
	

# Load args (not used yet)
if len(sys.argv) > 1:
	url = sys.argv[1]


######################################################## Twitter

## Connect and get
twitter.Auth()

twits = []
for tw in config['twitter_accounts']:
	add_twits = twitter.GetTweets(_user=tw, _count=10)
	if add_twits:
		twits.extend(add_twits)
print 'Total: ' + str(len(twits))


## Extract infos (regex)
for tw in twits:
	meta = regex_data.RegexExtractData(tw['text'])
	for attr in meta:
		tw[attr] = meta[attr]


## Dump
if debug:
	f = 'debug/debug_twits.txt'
	print "Dumping file " + f
	obj = open(f, 'wb')
	for item in twits:
		for descriptor in item:
			obj.write(descriptor + ": " + item[descriptor].encode('utf-8') + "\n")
		obj.write("\n\n")	
	obj.close
	print "Ready\n\n\n"


######################################################## Feeds

entries = []

## Connect and get
for feed in config['feeds']:
	url = feed['link']
	d = feedparser.parse( url )
	entries.extend(d.entries)
	print 'Extracted feed: ' + d.feed.title
	print 'Total: ' + str(len(d.entries))
	print "\n"

## Extract data (regex)
for item in entries:
		meta[item] = regex_data.RegexExtractData(item.description)


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

