# ref: https://stackoverflow.com/questions/43388476/how-could-spacy-tokenize-hashtag-as-a-whole
# ref: https://universaldependencies.org/docs/u/pos/
# ref: https://www.dataquest.io/blog/tutorial-text-classification-in-python-using-spacy/

# ref: https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
# ref: https://medium.com/@m.treerungroj/machine-learning-supervised-learning-with-basic-scikit-learn-part1-99b8b2327c9
# ref: https://spacy.io/api/pipeline-functions#merge_entities
# ref: https://spacy.io/api/token
import spacy
from nltk.corpus import stopwords
import csv
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.matcher import *
from pythainlp import *
from pythainlp.corpus import*
import pandas
import re
import time
from datetime import datetime
from tempfile import NamedTemporaryFile
import shutil
class NLP_crawler:
    def __init__(self,query):
        #Build file csv 
        self.csvfile_input = open(str(query)+'_crawler.csv', 'r',newline='', encoding='utf-8')
        self.csv_reader = csv.reader(self.csvfile_input, delimiter=',')
        
        fieldnames = ['10 ranking','number']
        self.csvfile_output = open(str(query)+'_NLP_crawler.csv', 'w', newline='', encoding="utf-8")
        self.writer_output = csv.DictWriter( self.csvfile_output, fieldnames=fieldnames )
        self.writer_output.writeheader()

    #select th or en word to analysis and count them
    def save_analysis(self, lang, data):
        dict_temp = {}
        first = 0
        self.nlp = spacy.load("en_core_web_md")
        for row in self.csv_reader:
            print(first)
            if(first > 0):
                if(lang == "th"):
                    temp = self.analyze_word_th(row[2],data)
                elif(lang == "en"):
                    temp = self.analyze_word_en(row[2],data)
                for i in temp:
                    message = i.lower()
                    if( message not in dict_temp ):
                        dict_temp[message] = 1
                    elif( message in dict_temp ):
                        dict_temp[message] += 1
                if(first == 5):
                    break
            first += 1
        self.dict_sort = self.bubbleSort(dict_temp,data)
        for temp in self.dict_sort:
            self.writer_output.writerow({'10 ranking':temp, 'number':dict_temp[temp]})
        self.csvfile_output.close()
        self.csvfile_input.close()
        self.re_search(data)

    #analysis th word
    def analyze_word_th(self, data, search):
        words = thai_stopwords()
        V = []
        data = re.sub("[0-9]",'',data)
        data = re.sub("[a-z A-Z]",'',data)
        nlp = word_tokenize(data , engine='newmm',keep_whitespace=False)
        nlp1 = [data for data in nlp if data not in words]
        for i in nlp1:
            r = re.sub('\w','',i)
            if i not in r and data and i != search:
                V.append(i)
        return V

    #analysis en word
    def analyze_word_en(self, data , search):
        data = re.sub("[0-9]",'',data)
        data = re.sub("#",'',data)
        self.output = []
        self.check = {}
        self.data = data
        self.docs = self.nlp(self.data)
        self.hashtag_filter()
        self.add_filter()
        for word in self.docs:
            self.twitter_check =( word.text[0]!="#"
                                and word.text[0]!="@"
                                and "#"+word.text not in self.check
                                and "@"+word.text not in self.check
                                and word.text not in self.nlp.Defaults.stop_words 
                                and word.text not in stopwords.words('english')
                                and not word.is_punct 
                                and "https:" not in word.text 
                                and self.filter_type(word)
                                and word.text != search)
            if( self.twitter_check ):
                self.output.append(word.text)
        return self.output

    #combine # and word
    def hashtag_filter(self):
        matcher = Matcher(self.nlp.vocab)
        pattern = [{'ORTH': '#'}, {'IS_ASCII': True}]
        matcher.add("HASHTAG", [pattern])
        matches = matcher(self.docs)
        spans = []
        for match_id, start, end in matches:
            spans.append(self.docs[start:end])
        for word in self.docs:
            if( word.text[0]=="#" ):
                self.output.append(word.text)
                self.check[word.text] = word.text
    
    #combine @ and word
    def add_filter(self):
        for word in self.docs:
            if( word.text[0]=="@" ):
                self.output.append(word.text)
                self.check[word.text] = word.text

    def merge_noun(self):
        merge_nps = self.nlp.create_pipe("merge_noun_chunks")
        self.nlp.add_pipe(merge_nps)
        self.docs = self.nlp(self.data)

    def filter_type(self, word):
        type_word = ["ADJ", "INTJ","NOUN", "PROPN", "VERB", "NUM"]
        if( word.pos_ in type_word ):
            return True
        else:
            return False

    def bubbleSort(self, dict_temp,data):
        first = 0
        key = [i for i in dict_temp.keys()]
        value = [i for i in dict_temp.values()]
        sort = {}
        for f in range(len(value)): 
            for s in range(len(value)-f-1): 
                if value[f] <= value[f+s] : 
                    value[f], value[f+s] = value[f+s], value[f]
                    key[f], key[f+s] = key[f+s], key[f]
        for fi in range(len(dict_temp)):
            if first < 10:
                sort[key[fi]] = value[fi]
                first += 1

        return sort

    def re_search(self,data):
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        headers = ["update_time",'file_name']
        file_name = 'file_list_Crawler.csv'
        try:
            csvfile = open(file_name, 'r',encoding='utf-8')
            reader = csv.reader(csvfile, delimiter=',') # Checkink NotFoundError 

            tempfile = NamedTemporaryFile(mode='w', delete=False, newline='',encoding='utf-8')
            writer_re = csv.DictWriter(tempfile, fieldnames=headers)
            writer_re.writeheader()

            first = 0
            n = []
            for row in reader:
                if(first > 0):
                    if(row[1] == str(data)+'.csv'):
                        writer_re.writerow( {'update_time':date_time, 'file_name':str(data)+'.csv'} )
                    else:
                        writer_re.writerow( {'update_time':row[0], 'file_name':row[1]} )
                n.append(row[1])
                first += 1

            if(str(data)+'.csv' not in n):
                writer_re.writerow( {'update_time':date_time, 'file_name':str(data)+'.csv'} )

            tempfile.close()
            csvfile.close()

            shutil.move(tempfile.name, file_name)

        except FileNotFoundError:
            csvfile = open(file_name, 'w', newline='')
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            
            csvfile = open(file_name, 'a', newline='')
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writerow( {'update_time':date_time, 'file_name':str(data)+'.csv'} )
            csvfile.close()

if __name__ == "__main__":
        start = time.time()
        obj = NLP_crawler()
        obj.save_analysis(str(input()),'covid')
        print( int(time.time() - start) )