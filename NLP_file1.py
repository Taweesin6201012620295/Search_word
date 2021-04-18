from pythainlp import *
from pythainlp.corpus import*
import pandas
import re
import emoji

df = pandas.read_csv('tweet_table.csv')
words = thai_stopwords()
V = []
for text in df['tweet']:

    text = text.replace("https","")
    text = text.replace("://","")
    nlp = word_tokenize(text , engine='newmm',keep_whitespace=False)
    nlp1 = [text for text in nlp if text not in words]
    for i in nlp1:
        r = re.findall('\W',i)
        if i not in r and text:
            V.append(i)
print(V)