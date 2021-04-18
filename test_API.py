import os
import tweepy as tw
import pandas as pd

consumer_key = 'a9H686ql30kmQTdtk5rlMX9fM'
consumer_key_secret = 'R4czxY30ilsHjYB4wxTaJidesJKV2oacvFROPUrG8QXDlGjGON'
access_token = '1348153243323355137-XlYJi94nnDHAmEO8Nxgd0yKxgLKYHU'
access_token_secret = 'dIDtWvh6yxMrHOCpAFYqSHxZcC9uAw0znALAlbyX7rvMX'

auth = tw.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

search_words = "#covid"
new_search = search_words + " -filter:retweets"

until = "2021-2-17"
since = "2021-2-10"

# Collect tweets
tweets = tw.Cursor(api.search,
              q=new_search,
              count=100,
              lang="en",
              until = until,
              since = since).items()

for tweet in tweets:
    print(str(tweet.created_at) + str(tweet.text) + str(tweet.user.location))