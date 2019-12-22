import tweepy
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

f = open('./tokens.txt', 'r')
keys = f.read().split('\n')
CONSUMER_KEY    = keys[0]
CONSUMER_SECRET = keys[1]
ACCESS_TOKEN  = keys[2]
ACCESS_SECRET = keys[3]

def connect_to_twitter_OAuth():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api

api = connect_to_twitter_OAuth()

trumpTweets = api.user_timeline('realdonaldtrump')
tweet_list = []
for tweet in trumpTweets:
    tweet_list.append({'tweet_id':tweet.id,
                          'text':tweet.text})
    print(tweet.text.encode("utf-8"))

df = pd.DataFrame(tweet_list, columns=['tweet_id', 'text'])
df