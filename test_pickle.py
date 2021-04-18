from pythainlp.tokenize import word_tokenize
from pythainlp import *
from pythainlp.corpus import*
import codecs
from itertools import chain
from nltk import NaiveBayesClassifier as nbc
import pandas as pd
from datetime import*
import pickle
import re
from datetime import datetime, date

data = str(input())
pos = 0
neg = 0
neu = 0
start = datetime.now()
        # pos.txt
with codecs.open('pos.txt', 'r', "utf-8") as f:
    lines1 = f.readlines()
    listpos=[e1.strip() for e1 in lines1]
    f.close() # ปิดไฟล์

# neu.txt
with codecs.open('neu.txt', 'r', "utf-8") as f:
    lines2 = f.readlines()
    listneu=[e2.strip() for e2 in lines2]
    f.close() # ปิดไฟล์

        # neg.txt
with codecs.open('neg.txt', 'r', "utf-8") as f:
    lines3 = f.readlines()
    listneg=[e3.strip() for e3 in lines3]
    f.close() # ปิดไฟล์

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
        if i not in r and data:
            V.append(i)
    return V


pos1=['pos']*len(listpos)
neu1=['neu']*len(listneu)
neg1=['neg']*len(listneg)

training_data = list(zip(listpos,pos1)) + list(zip(listneu,neu1)) + list(zip(listneg,neg1))
#print(training_data)
vocabulary = set(chain(*[word_tokenize(i[0].lower()) for i in training_data]))
#print(vocabulary)
feature_set = [({i:(i in word_tokenize(sentence.lower())) for i in vocabulary},tag) for sentence, tag in training_data]
#print(feature_set)
classifier = nbc.train(feature_set)
#print(classifier)

df = pd.read_csv(str(data)+'_crawler.csv',error_bad_lines=False)

for tweet in df['Description']:
    test_sentence = tweet
    featurized_test_sentence =  {i:(i in analyze_word_th(test_sentence.lower())) for i in vocabulary}
    if classifier.classify(featurized_test_sentence) == 'pos':
        pos = pos+1
    elif classifier.classify(featurized_test_sentence) == 'neg':
        neg = neg+1
    else:
        neu = neu+1

end = datetime.now()
diff = end - start

print(diff)
print("Total Positive = ", pos)
print("Total Negative = ", neg)
print("Total Neutral = ", neu)