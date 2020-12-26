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


def record_tweet_info(tweet, mentions_list):
	if not tweet:
		print('Error: tweet is empty')
		return mentions_list;

	tweet_info = f"Tweet sent by @{tweet.author.name} on {tweet.created_at}: {tweet.text}"

	mentions_list.append(tweet_info)

	print("------------------------------------------------")
	print("AFTER APPENDING: ")
	print('\n'.join(map(str, mentions_list))) 
	print("------------------------------------------------")

	print("size is: " + str(len(mentions_list)))

	# load/write recent mentions into 'recent_mentions.pkl'
	with open('recent_mentions.pkl', 'wb') as mentions_pickle_file:
		pickle.dump(mentions_list, mentions_pickle_file)

	print('recorded tweet info')
	return mentions_list


def is_new_tweet(tweet, mentions_list):
	if not tweet:
		print('Error: tweet is empty')
		return False;

	tweet_info = f"Tweet sent by @{tweet.author.name} on {tweet.created_at}: {tweet.text}"
	if tweet_info in mentions_list:
		print('Not a new mention')
		return False
	else:
		print('New mention found!!!!!!!!')
		return True
	
# resize list to desired size
def resize_list(size, mentions_list):
	if len(mentions_list) <= size:
		print('no need to resize..')
		return mentions_list

	print("Before resize SIZE: " + str(len(mentions_list)))
	while len(mentions_list) > size:
		mentions_list.pop(0)
		print('reduced size of list, new size is: ' + str(len(mentions_list)))
		#print(str(mentions_list))
	
	print('done resizing')
	return mentions_list
	


# video on how to create environment variables on your PC: https://www.youtube.com/watch?v=IolxqkL7cD8&ab_channel=CoreySchafer
twitter_API_key = os.environ.get('TWITTER_API_KEY')
twitter_API_secret = os.environ.get('TWITTER_API_SECRET')
twitter_access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
twitter_access_secret = os.environ.get('TWITTER_TOKEN_SECRET')

sleep_time = 45
num_mention = 6 # number of mentions this bot will worry about

auth = tweepy.OAuthHandler(twitter_API_key, twitter_API_secret)
auth.set_access_token(twitter_access_token, twitter_access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

user = api.me()

recent_mentions = []
# load/write recent mentions into 'recent_mentions.pkl'
with open('recent_mentions.pkl', 'wb') as mentions_pickle_file:
	pickle.dump(recent_mentions, mentions_pickle_file)

print('Starting bot...')

# rb = "reading binary"
# reads 'recent_mentions.pkl' and stores it into recent_mentions list
with open('recent_mentions.pkl', 'rb') as mentions_pickle_file:
	recent_mentions = pickle.load(mentions_pickle_file)
	print(f"recent_mentions.plk contains: {recent_mentions}")

while True:
	try:
		tweets = api.mentions_timeline(count = 10)	# get tweets that mention the bot

		# check if there are no mentions
		if not tweets:
			print('no mentions found')
			time.sleep(sleep_time)
			continue;

		print('mention/s found!')
		# range(start, stop, step)
		# the following line will make start for loop at last index, and decrement i
		# why? in order to make it so the oldest entries are in the front of the "queue" --> 'recent_mentions' list
		for i in range(len(tweets) - 1, -1, -1):
			if is_new_tweet(tweets[i], recent_mentions):
				# get tweet text
				tweet_text = tweets[i].text

				# make haiku
				make_haiku(tweet_text)

				# record the person who mentioned to prevent making haiku of the same tweet
				record_tweet_info(tweets[i], recent_mentions)

				print("------------------------------------------------")
				print("Recent mentions updated: ")
				print('\n'.join(map(str, recent_mentions))) 
				print("------------------------------------------------")

				time.sleep(2)

		recent_mentions = resize_list(15, recent_mentions)

		print("------------------------------------------------")
		print("Recent mentions RESIZED: ")
		print('\n'.join(map(str, recent_mentions))) 
		print("------------------------------------------------")

		print(" ++++++++++++++++++++++++++++++++++++++++++++++++++++++")
		print("+++++++++++++++++++  SLEEPING  +++++++++++++++++++++++++")
		print(" ++++++++++++++++++++++++++++++++++++++++++++++++++++++")
		time.sleep(sleep_time)

	except tweepy.TweepError as e:
		print("error recieved:" + e.reason)		# printing out the errors
