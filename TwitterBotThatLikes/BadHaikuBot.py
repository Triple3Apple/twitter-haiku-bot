# badhaikubot.py
# A twitter bot that turns a tweet into a really bad haiku
# Made by: https://github.com/Triple3Apple

import tweepy
import time
import json
import os

twitter_API_key = os.environ.get('TWITTER_API_KEY')
twitter_API_secret = os.environ.get('TWITTER_API_SECRET')
twitter_access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
twitter_access_secret = os.environ.get('TWITTER_TOKEN_SECRET')

auth = tweepy.OAuthHandler(twitter_API_key, twitter_API_secret)
auth.set_access_token(twitter_access_token, twitter_access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

user = api.me()

# Cursor gather all the things
#for follower in tweepy.cursor(api.followers).items():
#	print(follower.name)
#	if follower.name == "crazy how cool":
#		follower.follow()

search = "Santa"

numberOfTweets = 1

for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
	try:
		print("Tweet Liked: " + tweet.text)
		tweet.favorite()
		# id = tweet.user.id_str
		
		time.sleep(5)

	except tweepy.TweepError as e:
		print("error recieved:" + e.reason)		# printing out the errors

	except StopIteration:	# reaches completion
		break

print('using new file!!!!!!')
print(user.screen_name)
