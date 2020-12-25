# badhaikubot.py
# A twitter bot that turns a tweet into a really bad haiku
# Made by: https://github.com/Triple3Apple

import tweepy
import time
import json
import os
import pickle

def make_haiku(text):
	if not text:
		print('Error: text of tweet is empty :(')
		return;
	print('recieved text: ' + text)


def record_tweet_info(tweet):
	if not tweet:
		print('Error: tweet is empty')
		return;

	tweet_info = f"Tweet sent by @{tweet.author.name} on {tweet.created_at}: {tweet.text}"
	recent_mentions.append(tweet_info)

	# resize list if necessary
	resize_list(num_mention)

	# load/write recent mentions into 'recent_mentions.pkl'
	with open('recent_mentions.pkl', 'wb') as mentions_pickle_file:
		pickle.dump(recent_mentions, mentions_pickle_file)

	print('recorded tweet info')



def is_new_tweet(tweet):
	if not tweet:
		print('Error: tweet is empty')
		return;

	tweet_info = f"Tweet sent by @{tweet.author.name} on {tweet.created_at}: {tweet.text}"
	if tweet_info in recent_mentions:
		print('Not a new mention')
		return False
	else:
		print('New mention found!!!!!!!!')
		return True
	
# resize list to desired size
def resize_list(size):
	if len(recent_mentions) < size:
		print('no need to resize')
		return recent_mentions

	while len(recent_mentions) >= size:
		recent_mentions.pop()
	
	print('done resizing')
	#return mentions_list
	


# video on how to create environment variables on your PC: https://www.youtube.com/watch?v=IolxqkL7cD8&ab_channel=CoreySchafer
twitter_API_key = os.environ.get('TWITTER_API_KEY')
twitter_API_secret = os.environ.get('TWITTER_API_SECRET')
twitter_access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
twitter_access_secret = os.environ.get('TWITTER_TOKEN_SECRET')

sleep_time = 15 
num_mention = 5 # number of mentions this bot will worry about

auth = tweepy.OAuthHandler(twitter_API_key, twitter_API_secret)
auth.set_access_token(twitter_access_token, twitter_access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

user = api.me()

recent_mentions = []
# load/write recent mentions into 'recent_mentions.pkl'
#with open('recent_mentions.pkl', 'wb') as mentions_pickle_file:
#	pickle.dump(recent_mentions, mentions_pickle_file)

print('Starting bot...')

# rb = "reading binary"
# reads 'recent_mentions.pkl' and stores it into recent_mentions list
with open('recent_mentions.pkl', 'rb') as mentions_pickle_file:
	recent_mentions = pickle.load(mentions_pickle_file)
	print(f"recent_mentions.plk contains: {recent_mentions}")

#tweets = api.mentions_timeline()



while True:
	try:
		tweets = api.mentions_timeline(count = num_mention)	# get tweets that mention the bot

		# check if there are no mentions
		if not tweets:
			print('no mentions found')
			time.sleep(sleep_time)
			continue;

		print('mention/s found!')

		for tweet in tweets:
			if is_new_tweet(tweet):
				# get tweet text
				tweet_text = tweet.text

				# make haiku
				make_haiku(tweet_text)

				# record the person who mentioned to prevent making haiku of the same tweet
				record_tweet_info(tweet)

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
