import tweepy
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
''' f = open('./tokens.txt', 'r')
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

api = connect_to_twitter_OAuth() '''

import matplotlib.pyplot as plt
def getData():
    tweetList = []
    f = open('./p-trade/trumpbot/rawTweets.csv', 'r')
    lines = f.read().split('\n')
    for line in lines:
        entries = line.split(',')
        if(len(entries)==5):
          tweetList.append({'text': entries[1],
              'time': entries[2],
              'isRetweet': entries[3],
              'id': entries[4]})
    return pd.DataFrame(tweetList, columns=['id', 'time', 'isRetweet', 'text'])

def get_tweet_sentiment(text):
  # create TextBlob object of passed tweet text
  analysis = TextBlob(text)
  return analysis.sentiment.polarity

'''
df1 = getData()
df2 = df1.iloc[1:]
df3 = df2[df2['isRetweet'] == 'false']
df3 = df3.assign(sentiment = df3['text'].apply(get_tweet_sentiment))
df4 = df3[abs(df3['sentiment'])>.1]'''
df5 = df4[df4['text'].str.contains("Market")]
df5 = df5.astype('object')