# badhaikubot.py
# A twitter bot that turns a tweet into a really bad haiku
# Made by: https://github.com/Triple3Apple

import tweepy
import time
import json
import os

def makeHaiku(text):
	if not text:
		print('Error: text of tweet is empty :(')
		return;
	print('recieved text: ' + text)

	


# video on how to create environment variables on your PC: https://www.youtube.com/watch?v=IolxqkL7cD8&ab_channel=CoreySchafer
twitter_API_key = os.environ.get('TWITTER_API_KEY')
twitter_API_secret = os.environ.get('TWITTER_API_SECRET')
twitter_access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
twitter_access_secret = os.environ.get('TWITTER_TOKEN_SECRET')

sleep_time = 15 

auth = tweepy.OAuthHandler(twitter_API_key, twitter_API_secret)
auth.set_access_token(twitter_access_token, twitter_access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

user = api.me()

tweets = api.mentions_timeline()

while True:
	try:
		tweets = api.mentions_timeline(count = 1)	# get tweets that mention the bot

		# check if there are no mentions
		if not tweets:
			print('no mentions found')
			time.sleep(sleep_time)
			continue;

		print('mention/s found!')

		for tweet in tweets:
			tweet_text = tweet.text
			makeHaiku(tweet_text)
			time.sleep(1)

		time.sleep(sleep_time)

	except tweepy.TweepError as e:
		print("error recieved:" + e.reason)		# printing out the errors
	
		


#for tweet in tweets:
#	tweet_text = tweet.text


# Cursor gather all the things
#for follower in tweepy.cursor(api.followers).items():
#	print(follower.name)
#	if follower.name == "crazy how cool":
#		follower.follow()

#search = "Santa"

#numberOfTweets = 1

#for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
#	try:
#		print("Tweet Liked: " + tweet.text)
#		tweet.favorite()
#		# id = tweet.user.id_str
		
#		time.sleep(5)

#	except tweepy.TweepError as e:
#		print("error recieved:" + e.reason)		# printing out the errors

#	except StopIteration:	# reaches completion
#		break

#print(user.screen_name)
