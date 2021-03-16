# Refference https://www.youtube.com/watch?v=ae62pHnBdAg&ab_channel=BorntoDev

import tweepy
import csv
import pandas
from textblob import TextBlob

class Twitter_API:
    def __init__(self,query,lang):

        consumer_key = 'a9H686ql30kmQTdtk5rlMX9fM'
        consumer_key_secret = 'R4czxY30ilsHjYB4wxTaJidesJKV2oacvFROPUrG8QXDlGjGON'
        access_token = '1348153243323355137-XlYJi94nnDHAmEO8Nxgd0yKxgLKYHU'
        access_token_secret = 'dIDtWvh6yxMrHOCpAFYqSHxZcC9uAw0znALAlbyX7rvMX'

        self.query = query
        self.lang = lang
        self.count = 10
        self.tweet_mode = "extended"
        self.result_type = "mixed"
        self.auth = tweepy.OAuthHandler(consumer_key,consumer_key_secret)
        self.auth.set_access_token(access_token,access_token_secret)
        self.api = tweepy.API(self.auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
        
        # Write file .csv for checking and record infor
        fieldnames = ['time', 'places', 'tweet']
        self.csvfile = open(str(query)+'_Data.csv', 'a', newline='', encoding="utf-8")
        self.writer = csv.DictWriter( self.csvfile, fieldnames=fieldnames )
        self.writer.writeheader()

    def search(self):
        count = 0
        maxId = 0
        while(count < 10):
            data = self.api.search(q=self.query,lang=self.lang,count=self.count,tweet_mode=self.tweet_mode,result_type=self.result_type,max_id=str(maxId - 1))
            self.write_csv(data,self.query)
            if(len(data)==0):
                continue
            maxId = data[-1].id
            count += 1
        self.csvfile.close()
        print("Finish all of tweet are ",count)

    def write_csv(self, data,query):
        for infor in data:
            if(  (not infor.retweeted) and ("RT @" not in infor.full_text)  ):
                self.writer.writerow( {'time': str(infor.created_at), 'places': infor.user.location, 'tweet':infor.full_text} )

if __name__ == "__main__":
    obj = Twitter_API("covid","en")
    obj.search()