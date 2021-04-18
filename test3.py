import pandas as pd
import pickle
import re
from nltk import NaiveBayesClassifier as nbc
from pythainlp import *
from pythainlp.corpus import*
from pythainlp.tokenize import *
from textblob import TextBlob

day_1,day_2 = '20', '28'
month1,month2 = '03','03'
year1, year2 = '2021', '2021'
#print(day_1,month1,year1)

data = 'โควิด'
pan = pd.read_csv(str(data)+'_Data.csv')

def loadData():
    # for reading also binary mode is important
    dbfile = open('Model', 'rb')
    db = pickle.load(dbfile)
    dbfile.close()
    return db

#analysis th word
def analyze_word_th(data):
    words = thai_stopwords()
    V = []
    data = re.sub("[0-9]",'',data)
    data = re.sub("[a-z A-Z]",'',data)
    nlp = word_tokenize(data , engine='newmm',keep_whitespace=False)
    nlp1 = [data for data in nlp if data not in words]
    for i in nlp1:
        r = re.sub('\w','',i)
        if i != data:
            if i not in r :
                V.append(i)
    return V

def Sentiment_pickel(df):
    A = loadData()
    pos = 0
    neg = 0
    neu = 0

    for tweet in df['tweet']:
        test_sentence = tweet
        featurized_test_sentence =  {i:(i in analyze_word_th(test_sentence.lower())) for i in A[1]}
        if A[0].classify(featurized_test_sentence) == 'pos':
            pos = pos+1
        elif A[0].classify(featurized_test_sentence) == 'neg':
            neg = neg+1
        else:
            neu = neu+1
    tol = pos + neg + neu

    print("Total Positive = ", pos)
    print("Total Negative = ", neg)
    print("Total Neutral = ", neu)
    print('Toatl = ',tol)


def Sentiment_en(df):
    #Part-2: Sentiment Analysis Report
    #Finding sentiment analysis (+ve, -ve and neutral)
    pos = 0
    neg = 0
    neu = 0
    for tweet in df['tweet']:
        analysis = TextBlob(tweet)
        if analysis.sentiment[0]>0:
            pos = pos +1
        elif analysis.sentiment[0]<0:
            neg = neg + 1
        else:
            neu = neu + 1
    tol = pos + neg + neu
    print("Total Positive = ", pos)
    print("Total Negative = ", neg)
    print("Total Neutral = ", neu)
    print('Total = ' ,tol)


if len(day_1) == 1:
    day_1 = '0' + day_1
if len(day_2) == 1:
    day_2 = '0' + day_2
if len(month1) == 1: 
    month1 = '0' + month1
if len(month2) == 1:
    month2 = '0' + month2

colume1 = pan['time'] >= f'{year1}-{month1}-{day_1} 00:00:00'
colume2 = pan['time'] <= f'{year2}-{month2}-{day_2} 23:59:59'
between = pan[colume1 & colume2]
df = pd.DataFrame({'time': between['time'],'tweet': between['tweet']})
print(df)

if re.match('[ก-๙]',data) != None:
    Sentiment_pickel(df)
else:
    Sentiment_en(df)