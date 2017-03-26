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

# Keep track
total_twits = 0
okay_twits = 0
total_rss = 0
okay_rss = 0

######################################################## Twitter

##----- Connect and get
if not debug:
    twitter.Auth()

    twits = [] # twit holds 'username' and 'text'
    for tw in config['twitter_accounts']:
    	add_twits = twitter.GetTweets(_user=tw, _count=10)
    	if add_twits:
    		twits.extend(add_twits)
    total_twits = len(twits)
    print 'Total: ' + str(total_twits)

    # SAVE DEBUG FILES
    if save_files:
    	with open(debug_path+'twits.pickle', 'wb') as handle:
    		pickle.dump(twits, handle)
else:
# LOAD DEBUG FILES
    try:
        with open(debug_path+'twits.pickle', 'rb') as handle:
            twits = pickle.load(handle)
            total_twits = len(twits)
    except:
    	print "Please, consider saving files before debug mode"

##----- Extract infos
for tw in twits:
    new_item = dict(item_template)
    new_item['publisher'] = tw['username']
    new_item['corpus'] = tw['text']

    # Process text with custom regex for tags + NLTK
    text, backup_tags = regex_data.PrepareText(tw['text'], replace=True)
    nltk_data = nltk_parse.nltk_extract(text, text_type="twitter")
    nltk_data = regex_data.RestoreTags(nltk_data, text, backup_tags)

    # Temporal first-ocurrence data
    for it in nltk_data:
        if len(nltk_data[it]) > 0:
            new_item[it] = nltk_data[it][0]

    if (new_item['date']!=None
    and new_item['title']!=None):
        okay_twits += 1
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
        channel_number_items = len(d.entries)
        total_rss += channel_number_items
        print 'Extracted feed: ' + d.feed.title
        print 'Total: ' + str(channel_number_items) + '\n'

        # SAVE DEBUG FILES
        if save_files:
        	with open(debug_path+'feeds.pickle', 'wb') as handle:
        		pickle.dump(entries, handle)
else:
    # LOAD DEBUG FILES
    try:
        with open(debug_path+'feeds.pickle', 'rb') as handle:
            entries = pickle.load(handle)
            total_rss = len(entries)
    except:
    	print "Please, consider saving files before debug mode"

##----- Extract data
for item in entries:
    clean_desc = helpers.cleanhtml(item.description)

    new_item = dict(item_template)
    new_item['corpus'] = clean_desc
    new_item['title'] = helpers.cleanhtml(item.title)
    new_item['link'] = item.link
    new_item['date_pub'] = item.published

    # Process text with custom regex for tags + NLTK
    text, backup_tags = regex_data.PrepareText(clean_desc, replace=True)
    nltk_data = nltk_parse.nltk_extract(text, text_type="rss")
    #print "BACKUP TAGS---------------------------"
    #print backup_tags
    #print "BEFORE--------------------------------"
    #print nltk_data
    nltk_data = regex_data.RestoreTags(nltk_data, text, backup_tags)
    #print "AFTER---------------------------------"
    #print nltk_data

    # Temporal first-ocurrence data
    for it in nltk_data:
        if len(nltk_data[it]) > 0:
            new_item[it] = nltk_data[it][0]


    if (new_item['date']!=None
    and new_item['title']!=None):
        okay_rss += 1
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
    '''
    for x in items:
    	for desc in x:
    		if x[desc]!=None:
    			print desc + ": " + x[desc]
    	print "-----------------------------------"
    '''

##------ Save infos
    f = debug_path + 'items.txt'
    print "Dumping file " + f
    obj = open(f, 'wb')
    for x in items:
    	for descriptor in x:
    		if x[descriptor]!=None:
    			obj.write(descriptor + ": " + x[descriptor].encode('utf-8') + "\n")
    	obj.write("\n\n")
    obj.close

print "\n----------------------"
print "Okay feeds: " + str(okay_rss)
print "Total feeds: " + str(total_rss)
print "----------------------"
print "Okay twits: " + str(okay_twits)
print "Total twits: " + str(total_twits)
print "----------------------"
print "Total okay: " + str(okay_twits + okay_rss)
print "Total: " + str(total_rss + total_twits)
print "----------------------"
print "Ready\n"
