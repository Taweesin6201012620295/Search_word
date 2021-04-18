  # Refference https://www.youtube.com/watch?v=ae62pHnBdAg&ab_channel=BorntoDev

import tweepy
import unittest
import csv
import pandas
from datetime import *
from geopy.geocoders import Nominatim

class Twitter_API:

    def __init__(self,query,lang,since,until):

        consumer_key = 'a9H686ql30kmQTdtk5rlMX9fM'
        consumer_key_secret = 'R4czxY30ilsHjYB4wxTaJidesJKV2oacvFROPUrG8QXDlGjGON'
        access_token = '1348153243323355137-XlYJi94nnDHAmEO8Nxgd0yKxgLKYHU'
        access_token_secret = 'dIDtWvh6yxMrHOCpAFYqSHxZcC9uAw0znALAlbyX7rvMX'

        self.query = query
        self.lang = lang
        self.count = 100
        self.since = datetime.strptime(str(since) + " 00:00:00","%Y-%m-%d %H:%M:%S")
        until = datetime.strptime(str(until),"%Y-%m-%d") + timedelta(days = 1)
        self.until = str(until).split(" ")[0]
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

    def search(self): #Function search word
        start = 0
        maxId = -1
        Inmediat = 0
        Stop = True
        while(Stop):
            try:
                if (maxId <= 0 and Inmediat<1):
                    data = self.api.search(q=self.query,
                                        lang=self.lang,
                                        count=self.count,
                                        tweet_mode=self.tweet_mode,
                                        result_type=self.result_type,
                                        until = self.until)
                else:
                    if Inmediat >= 1:
                        data = self.api.search(q=self.query,
                                        lang=self.lang,
                                        count=self.count,
                                        tweet_mode=self.tweet_mode,
                                        result_type=self.result_type,
                                        max_id = str( maxId - 38555555555555 -555555555 - (100000000*Inmediat)),
                                        until = self.until)

                        print(start)
                        start += 1
                        Inmediat +=1
        
                    else:
                        data = self.api.search(q=self.query,
                                        lang=self.lang,
                                        count=self.count,
                                        tweet_mode=self.tweet_mode,
                                        result_type=self.result_type,
                                        max_id = str( maxId - 38555555555555),
                                        until = self.until)
                self.write_csv(data,self.query)

                if(len(data)==0):
                    continue
                maxId = data[-1].id
                start += 1
                Stop = self.write_csv(data,self.query)

            except:
                Inmediat +=1
                start += 1
                
                if start >= 10:
                    Stop = False
        print(start)
        print(len(data))
        self.csvfile.close()
        print("Finish all of tweet are ",start)
        return data

    #Write file csv
    def write_csv(self, data,query):
        for infor in data:
            data_created_at = datetime.strptime(str(infor.created_at),"%Y-%m-%d %H:%M:%S")
            if( data_created_at < self.since):
                return False

            if(  (not infor.retweeted) and ("RT @" not in infor.full_text)  ):
                self.writer.writerow( {'time': str(infor.created_at), 'places': infor.user.location, 'tweet':infor.full_text} )
        return True

if __name__ == "__main__":

    #class Unit_test(unittest.TestCase):
    #    def test_API(self):
            obj = Twitter_API("โควิด","th","2021-04-14","2021-04-18");
            obj.search()
    #        self.assertIsNotNone(obj.search())
    #        self.assertTrue(obj.write_csv())

    #unittest.main()