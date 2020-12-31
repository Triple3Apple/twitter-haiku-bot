# badhaikubot.py
# A twitter bot that turns a tweet into a really bad haiku
# Made by: https://github.com/Triple3Apple

import tweepy
import time
import os
import pickle
import sys
from haikumaker import make_haiku
# import syllapy


class HaikuBot:
    sleep_time = 45

    def __init__(self, twit_api_key, twit_api_secret, twit_access_token,
                 twit_secret_token, num_mentions: int, num_entries: int):
        # video on how to create environment variables on your PC:
        # https://www.youtube.com/watch?v=IolxqkL7cD8&ab_channel=CoreySchafer
        self.twitter_API_key = os.environ.get(twit_api_key)
        self.twitter_API_secret = os.environ.get(twit_api_secret)
        self.twitter_access_token = os.environ.get(twit_access_token)
        self.twitter_access_secret = os.environ.get(twit_secret_token)
        # number of mentions this bot will worry about
        self.num_mentions = num_mentions
        # number of mentions to be recorded in 'recent_mentions.pkl'
        self.num_entries = num_entries
        self.recent_mentions = []

    # authenticates and returns api object
    def authenticate_bot(self):
        # auth = tweepy.OAuthHandler(self.twitter_API_key, self.twitter_API_secret)
        # auth.set_access_token(self.twitter_access_token, self.twitter_access_secret)
        print(self.twitter_API_key)
        auth = tweepy.OAuthHandler(
            consumer_key=self.twitter_API_key,
            consumer_secret=self.twitter_API_secret)
        auth.set_access_token(
            key=self.twitter_access_token,
            secret=self.twitter_access_secret)

        api = tweepy.API(
            auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        try:
            api.verify_credentials()
            print("Authentication OK")
        except:
            print("Error during authentication!")
            sys.exit("Error during authentication!")

        return api

    # def make_haiku(self, text: str):
    #     if not text:
    #         print('Error: text of tweet is empty :(')
    #         return
    #     print('RECIEVED TEXT: ' + text)

    # prints out the recent_mentions list (for debugging purposes)
    def print_recent_mentions(self, text: str = ''):
        print("------------------------------------------------")
        if text != '':
            print(text)
        print('\n'.join(map(str, self.recent_mentions)))
        print("------------------------------------------------")

    # save tweet info in file to keep track of tweets the
    # bot has already replied to
    def record_tweet_info(self, tweet):
        if not tweet:
            print('Error: tweet is empty')
            return self.recent_mentions

        # string that will be written in file for recording tweets
        # that were turned to haikus
        tweet_info = (
            f"Tweet sent by @{tweet.author.name} "
            f"on {tweet.created_at}: {tweet.text}")

        self.recent_mentions.append(tweet_info)

        self.print_recent_mentions('AFTER APPENDING')

        print("size is: " + str(len(self.recent_mentions)))

        # load/write recent mentions into 'recent_mentions.pkl'
        with open('recent_mentions.pkl', 'wb') as mentions_pickle_file:
            pickle.dump(self.recent_mentions, mentions_pickle_file)

        print('recorded tweet info')
        return self.recent_mentions

    # check if tweet is "new" (not already processed yet by the bot)
    def is_new_tweet(self, tweet):
        if not tweet:
            print('Error: tweet is empty')
            return False

        tweet_info = (
            f"Tweet sent by @{tweet.author.name} "
            f"on {tweet.created_at}: {tweet.text}")
        if tweet_info in self.recent_mentions:
            print('Not a new mention')
            return False
        else:
            print('New mention found!!!!')
            return True

    # resize list to desired size

    def resize_list(self, size):
        if len(self.recent_mentions) <= size:
            print('no need to resize..')
            return self.recent_mentions

        print("Before resize SIZE: " + str(len(self.recent_mentions)))
        while len(self.recent_mentions) > size:
            self.recent_mentions.pop(0)
            print('reduced size of list, new size is: ' +
                  str(len(self.recent_mentions)))

        print('done resizing')
        return self.recent_mentions


def main():
    # create HaikuBot object
    hb = HaikuBot('TWITTER_API_KEY', 'TWITTER_API_SECRET',
                  'TWITTER_ACCESS_TOKEN', 'TWITTER_TOKEN_SECRET', 6, 15)
    api = hb.authenticate_bot()

    # load/write recent mentions into 'recent_mentions.pkl'
    with open('recent_mentions.pkl', 'wb') as mentions_pickle_file:
        pickle.dump(hb.recent_mentions, mentions_pickle_file)

    print('Starting bot...')

    # rb = "reading binary"
    # reads 'recent_mentions.pkl' and stores it into recent_mentions list
    with open('recent_mentions.pkl', 'rb') as mentions_pickle_file:
        hb.recent_mentions = pickle.load(mentions_pickle_file)
        print(f"recent_mentions.plk contains: {hb.recent_mentions}")

    while True:
        try:
            # get tweets that mention the bot
            tweets = api.mentions_timeline(count=hb.num_mentions)

            # check if there are no mentions
            if not tweets:
                print('no mentions found')
                time.sleep(hb.sleep_time)
                continue

            print('mention/s found!')
            # range(start, stop, step)
            # the following line will make start for loop at
            # last index, and decrement i
            # why? in order to make it so the oldest entries are in
            # the front of the "queue" --> 'recent_mentions' list
            for i in range(len(tweets) - 1, -1, -1):
                if hb.is_new_tweet(tweets[i]):

                    curr_tweet = tweets[i]
                    
                    # get tweet text
                    #tweet_text = curr_tweet.text
                    
                    # continue to next tweet if not quoted tweet
                    if curr_tweet.is_quote_status is False:
                        # TODO: reply to tweet sstating that the format is incorrect or something..
                        print('tweet is NOT a QUOTE RETWEET!   :C')
                    
                    else:
                        print('tweet is QUOTE RETWEET!')
                        print('contents: ' + str(curr_tweet.quoted_status.text) + '-----------------------')
                        # get quoted tweet text
                        quoted_tweet_text = str(curr_tweet.quoted_status.text)
                        # make haiku
                        make_haiku(quoted_tweet_text)


                    #test_tweet_text = curr_tweet.retweeted_status.text if curr_tweet.text.startswith("RT @") else curr_tweet.text

                    # record the person who mentioned to prevent
                    # making haiku of the same tweet
                    hb.record_tweet_info(curr_tweet)

                    hb.print_recent_mentions('Recent mentions updated: ')

                    time.sleep(1)

            hb.recent_mentions = hb.resize_list(hb.num_entries)

            hb.print_recent_mentions('Recent mentions RESIZED')

            print(" ++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("+++++++++++++++++++  SLEEPING  +++++++++++++++++++++++++")
            print(" ++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            time.sleep(hb.sleep_time)

        except tweepy.TweepError as e:
            print("error recieved:" + e.reason)		# printing out the errors
            time.sleep(10)

        except StopIteration:
            break

    # ------------------------


if __name__ == "__main__":
    main()
