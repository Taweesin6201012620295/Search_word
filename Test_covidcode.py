# Refference https://www.kaggle.com/drvaibhavkumar/twitter-data-analysis-using-tweepy?fbclid=IwAR3V7TyyRExe0CSIv_QVWBFB3i13YzQIOIaUs6tx_AXv4BfbrdBTF-VZZ5Y

import tweepy
from textblob import TextBlob

consumer_key = 'a9H686ql30kmQTdtk5rlMX9fM'
consumer_key_secret = 'R4czxY30ilsHjYB4wxTaJidesJKV2oacvFROPUrG8QXDlGjGON'
access_token = '1348153243323355137-XlYJi94nnDHAmEO8Nxgd0yKxgLKYHU'
access_token_secret = 'dIDtWvh6yxMrHOCpAFYqSHxZcC9uAw0znALAlbyX7rvMX'
auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

#Defining Search keyword and number of tweets and searching tweets
query = str(input())
max_tweets = 100
searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]

#Part-2: Sentiment Analysis Report

#Finding sentiment analysis (+ve, -ve and neutral)
pos = 0
neg = 0
neu = 0
for tweet in searched_tweets:
    analysis = TextBlob(tweet.text)
    if analysis.sentiment[0]>0:
       pos = pos +1
    elif analysis.sentiment[0]<0:
       neg = neg + 1
    else:
       neu = neu + 1
print("Total Positive = ", pos)
print("Total Negative = ", neg)
print("Total Neutral = ", neu)
