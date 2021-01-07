# coding: utf-8

# badhaikubot.py
# A twitter bot that turns a tweet into a really bad haiku
# Made by: https://github.com/Triple3Apple

import tweepy
import time
import os
import pickle
import sys
import random
from datetime import date
from datetime import datetime
from haikumaker import make_haiku
# import syllapy

haiku_text_decor = ['    *☆･ﾟ*.｡', '    *★ ﾟ｡ * ｡',
                    '    ☆∴｡　*', '    ･ﾟ*｡★･',
                    '   * ☆ ｡･ﾟ*.｡', '   * ﾟ*.｡☆ ｡･',
                    '    ･ﾟ*☆｡✰', '    ﾟ✧ *★ ﾟ･']

haiku_text_intros = ['Here\'s your haiku!',
                     'Haiku incoming!',
                     'Bad Haiku Incoming!',
                     'Enjoy! 🌸',
                     'Enjoy!',
                     'Haiku just for you!',
                     'Tweet haiku:',
                     'I\'m Sorry',
                     'Beep Boop']

special_line = '🌟✨🌟✨🌟'


class HaikuBot:
    sleep_time = 120

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

    # sends a tweet
    def send_tweet(self, api, tweet_text: str, tweet_id, tweet):
        try:
            # send tweet
            api.update_status(
                status=str(tweet_text),
                in_reply_to_status_id=tweet_id)

            print('tweet sent')
        except tweepy.TweepError as e:
            print("++++++++++++++error recieved for " + str(date.today()) + ":" + e.reason + "++++++++++")		# printing out the errors
            print('ERROR WHEN TWEETING: ' + tweet_text + " : from: " + str(tweet_id))

    def load_recent_mentions_file(self):
        with open('recent_mentions.pkl', 'rb') as mentions_pickle_file:
            self.recent_mentions = pickle.load(mentions_pickle_file)
            print(f"recent_mentions.plk contains: {self.recent_mentions}")


def main():

    # create HaikuBot object
    hb = HaikuBot('TWITTER_API_KEY', 'TWITTER_API_SECRET',
                  'TWITTER_ACCESS_TOKEN', 'TWITTER_TOKEN_SECRET', 6, 15)
    api = hb.authenticate_bot()

    # load/write recent mentions into 'recent_mentions.pkl' (creates the file)
    # with open('recent_mentions.pkl', 'wb') as mentions_pickle_file:
    #     pickle.dump(hb.recent_mentions, mentions_pickle_file)

    print('Starting bot...')

    # rb = "reading binary"
    # reads 'recent_mentions.pkl' and stores it into recent_mentions list
    try:
        hb.load_recent_mentions_file()
    except:
        # recent_mentions.pkl does not exist
        # so we have to create it
        # load/write recent mentions into 'recent_mentions.pkl' (creates the file)
        with open('recent_mentions.pkl', 'wb') as mentions_pickle_file:
            pickle.dump(hb.recent_mentions, mentions_pickle_file)
      
    # original below  
    # with open('recent_mentions.pkl', 'rb') as mentions_pickle_file:
    #     hb.recent_mentions = pickle.load(mentions_pickle_file)
    #     print(f"recent_mentions.plk contains: {hb.recent_mentions}")

    # this bool will make it so the the tweets gathered in the first wave of
    # gathering tweets are recorded but not responded to by the bot
    # (this is used to ignore tweets mentioning the bot when it was not actively running)
    is_ignoring = True

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
                    
                    if is_ignoring is False:
                        # continue to next tweet if not quoted tweet
                        if curr_tweet.is_quote_status is False:
                            print('tweet is NOT a QUOTE RETWEET!   :C')
    
                            # TODO: reply to tweet stating that the format is incorrect or something..
    
                            if 'source' in curr_tweet.text.lower():
                            
                                source_text = '@' + curr_tweet.user.screen_name + ' Link to source code (Github): https://github.com/Triple3Apple/twitter-haiku-bot'
    
                                hb.send_tweet(api=api, tweet_text=source_text, tweet_id=curr_tweet.id, tweet=curr_tweet)
    
                                print('source code wanted')
    
                            else:
                                if 'help' in curr_tweet.text.lower():
                                
                                    help_info = '@' + curr_tweet.user.screen_name + ' To use me and create a wonderfully bad haiku out of someone\'s tweet, create a quote tweet (click retweet and then "Quote Retweet") and @ me as a comment'
                                    
                                    hb.send_tweet(api=api, tweet_text=help_info, tweet_id=curr_tweet.id, tweet=curr_tweet)
    
                                    print('help requested')
                                else:
                                    info = '@' + curr_tweet.user.screen_name + ' Hello, I am a Haiku bot created by @Triple3Apple, ' \
                                         'I turn people\'s tweets into a wonderfully bad haiku! To use me and create a wonderfully ' \
                                         'bad haiku out of someone\'s tweet, create a quote tweet (click retweet and then "Quote Retweet") and @ me as a comment.'
                                         
                                    hb.send_tweet(api=api, tweet_text=info, tweet_id=curr_tweet.id, tweet=curr_tweet)
    
                        else:
                            print('tweet is QUOTE RETWEET!')
                            print('contents: ' + str(curr_tweet.quoted_status.text) + '-----------------------')
                            # get quoted tweet text
                            quoted_tweet_text = str(curr_tweet.quoted_status.text)
                            # make haiku
                            haiku = make_haiku(quoted_tweet_text)
    
                            if haiku == 'NEWR':
                                print('ERROR RECEVED: Not enough words recieved, tweet must have 5 non duplicate words')
                                # reply to tweet informing user that more words are needed
                                err_text = '@' + curr_tweet.user.screen_name + ' \n🤖 Says: Sorry, the quoted tweet must have more than 5 words'
                                
                                hb.send_tweet(api=api, tweet_text=err_text, tweet_id=curr_tweet.id, tweet=curr_tweet)
    
                                # api.update_status(
                                #     status=str(err_text),
                                #     in_reply_to_status_id=curr_tweet.id)
    
                            elif haiku == 'ECH':
                                print('ERROR RECIEVED: Something has gone wrong and my creator is bad at coding')
                                # reply to tweet informing user that bot has failed and creator is bad
                                err_text = '@' + curr_tweet.user.screen_name + ' \n🤖 Says: Sorry, something has gone wrong while making your Haiku. \nGo complain to my creator, @Triple3Apple'
                                
                                hb.send_tweet(api=api, tweet_text=err_text, tweet_id=curr_tweet.id, tweet=curr_tweet)
    
                                # api.update_status(
                                #     status=str(err_text),
                                #     in_reply_to_status_id=curr_tweet.id)
    
                            else:
                                greeting = ''
                                ending = ''
    
                                if random.randint(0, 20) == 10:
                                    # 5% chance to get "special" text
                                    greeting = f'@{curr_tweet.user.screen_name} {random.choice(haiku_text_intros)} \n\n{special_line}\n'
                                    ending = f'\n{special_line}'
                                else:
                                    greeting = f'@{curr_tweet.user.screen_name} {random.choice(haiku_text_intros)} \n\n{random.choice(haiku_text_decor)}\n'
                                    ending = f'\n{random.choice(haiku_text_decor)}'
                                    
                                haiku_tweet = greeting + haiku + ending
    
                                # post tweet
                                hb.send_tweet(api, tweet_text=haiku_tweet, tweet_id=curr_tweet.id, tweet=curr_tweet)

                    

                    # record the person who mentioned to prevent
                    # making haiku of the same tweet
                    hb.record_tweet_info(curr_tweet)

                    hb.print_recent_mentions('Recent mentions updated: ')

                    time.sleep(2)

            hb.recent_mentions = hb.resize_list(hb.num_entries)

            hb.print_recent_mentions('Recent mentions RESIZED')

            print(" ++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("+++++++++++++++++++  SLEEPING  +++++++++++++++++++++++++")
            print(" ++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            
            # After ignoring & recording the first wave of tweets,
            # resume tweeting and normal bot actions
            if is_ignoring is True:
                is_ignoring = False
                
            time.sleep(hb.sleep_time)

        except tweepy.TweepError as e:
            print("++++++++++++++error recieved for " + str(date.today()) + ":" + e.reason + "++++++++++")		# printing out the errors
            time.sleep(30)

        except StopIteration:
            break

    # ------------------------


if __name__ == "__main__":
    main()
