#!usr/bin/env python

##
## Extraer tweets de forma autentificada
## usando la libreria Tweepy
## 


import tweepy, json
from tweepy import OAuthHandler

tw_api = None

def Auth():
	print 'Authenticating on Twitter...'
	global tw_api
	# Cuenta para App TheEventCalendar (JF)
	consumer_key = 'NDrER3txtbIHWCHlCLE9M7i7j'
	consumer_secret = 'fcfk4q9ppJ5Xh7hjOqnjVl1n8zES4DUWoi0xYXNp6KApJRBHa3'
	access_token = '230478664-nJVVHchEyomMbB4FVNDsD7gUwbLFokOFVGZZ3ZTc'
	access_secret = 'hdUwdY92LvrkVxkzmslXEOptY7x1vhJlDzUnNzbQfg4DC'
	 
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	 
	tw_api = tweepy.API(auth)


def GetTweets(_user, _count=3):
	print '...Retrieving ' + _user + ' tweets'
	global tw_api
	twits = []

	# user_timeline extrae twits de una cuenta
	content = tw_api.user_timeline(screen_name = _user, count=_count, include_rts = False)

	for twit in content:
		twit_json = json.dumps(twit._json)
		twits.append(ParseTweet(twit_json))

	print '..... (' + str(len(twits)) + ')'
	return twits


def ParseTweet(_tw_json):
	tw_json = json.loads(_tw_json)
	tw = {
		'username' : tw_json['user']['name'],
		'text' : tw_json['text']
	}
	return tw




