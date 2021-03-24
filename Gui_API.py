# Refference https://www.youtube.com/watch?v=jJz3zADv0nU&t=2s
# Refference https://www.qtcentre.org/threads/68409-Save-QChartView-as-PNG
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtChart import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5 import *

import pandas as pd
import os
import os.path, time
from datetime import time
from textblob import TextBlob
import matplotlib.pyplot as plt
from tempfile import NamedTemporaryFile
import shutil
import codecs
from itertools import chain
from nltk import NaiveBayesClassifier as nbc

from miniproject_file1 import Twitter_API
from NLP import *
from Combine_GUI import*

class tweety_search(QWidget):

    switch_window = QtCore.pyqtSignal()

    def __init__(self): 
        #QApplication
        super().__init__()
        self.Creater()

    #copy text from line edit
    def getTextValue(self):
        data = self.inputbox.text()
        slide = self.slide.currentText()
        date1 = self.dateEdit.date().toPyDate()
        date2 = self.dateEdit1.date().toPyDate()
        self.check_search(data,slide,date1,date2)
        self.create_piechart(data)
        self.get_time(data)

    #check search word
    def check_search(self,data,slide,date1,date2):
        pan = pandas.read_csv('file_list_API.csv')
        check = str(data)+'.csv'
        store_file = []
        for i in pan['file_name']:
            store_file.append(i)
        if check not in store_file:
            obj = Twitter_API(data,slide,date1,date2)
            obj.search()
            print("This one :"+data)
            try:
                self.obj1 = NLP(data)
                self.obj1.save_analysis(slide,data)
                self.read_file(data)
                self.read_file_10rank(data)
                self.Sentiment(data,slide)
            except pandas.errors.EmptyDataError:
                pass
        else:
            self.read_file(data)
            self.read_file_10rank(data)
            self.show_sentiment(data)


    def Back(self):
        self.switch_window.emit()

    #creating title QMainWindow
    def Creater(self):
        self.setWindowTitle("Tweet search")
        self.resize(1780,920)

        #creating box QLineEdit
        self.inputbox = QLineEdit(self)
        self.inputbox.resize(300,30)
        self.inputbox.move(10,100)
        self.inputbox.setFont(QtGui.QFont("Helvetica",16))

        #creating button QPushButton
        self.button = QPushButton("Enter",self)
        self.button.resize(100,30)
        self.button.move(320,100)
        self.button.clicked.connect(self.getTextValue)
        self.button.setFont(QtGui.QFont("Helvetica",14))
        #creating button QPushButton
        self.button1 = QPushButton("Update Datetime",self)
        self.button1.resize(200,40)
        self.button1.move(10,250)
        self.button1.clicked.connect(self.update_time)
        self.button1.setFont(QtGui.QFont("Helvetica",14))
        #creating button QPushButton
        self.button3 = QPushButton("Back",self)
        self.button3.resize(150,80)
        self.button3.move(1600,800)
        self.button3.clicked.connect(self.Back)
        self.button3.setFont(QtGui.QFont("Helvetica",14))

        #set icon window
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap("../../Downloads/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(self.icon)

        #QLabel1
        self.label_1 = QLabel('Enter your word',self)
        self.label_1.move(20, 50)
        self.label_1.setFont(QtGui.QFont("Helvetica",20))
        #QLabel2
        self.label_2 = QLabel('Select your language',self)
        self.label_2.move(20,150)
        self.label_2.setFont(QtGui.QFont("Helvetica",16))
        #QLabel4
        self.label_5 = QLabel('Results of the tweet you searched',self)
        self.label_5.move(20,300)
        self.label_5.setFont(QtGui.QFont("Helvetica",16))
        #QLabel5
        self.label_5 = QLabel('Ranking Graph',self)
        self.label_5.move(800,15)
        self.label_5.setFont(QtGui.QFont("Helvetica",16))
        #QLabel6
        self.label_6 = QLabel('Sentiment',self)
        self.label_6.move(800,470)
        self.label_6.setFont(QtGui.QFont("Helvetica",16))
        #QLabel6
        self.label_7 = QLabel('First time to search',self)
        self.label_7.move(500,10)
        self.label_7.setFont(QtGui.QFont("Helvetica",16))
        #QLabel6
        self.label_8 = QLabel('End time to search',self)
        self.label_8.move(500,150)
        self.label_8.setFont(QtGui.QFont("Helvetica",16))

        #ComboBox th and en
        self.slide = QComboBox(self)
        self.slide.addItem('th')
        self.slide.addItem('en')
        self.slide.move(280,150)
        self.slide.setFont(QtGui.QFont("Helvetica",16))
        
        #TextBrowser
        #self.bro1 = QTextBrowser(self)
        #self.bro1.resize(250,30)
        #self.bro1.move(1320,800)
        #self.bro1.setFont(QtGui.QFont("Helvetica",12))
        #TextBrowser
        self.bro2 = QTextBrowser(self)
        self.bro2.resize(250,300)
        self.bro2.move(1300,50)
        self.bro2.setFont(QtGui.QFont("Helvetica",12))
        #TextBrowser
        self.bro3 = QTextBrowser(self)
        self.bro3.resize(500,400)
        self.bro3.move(800,50)
        self.bro3.setFont(QtGui.QFont("Helvetica",12))
        #TextBrower
        self.bro5 = QTextBrowser(self)
        self.bro5.resize(500,400)
        self.bro5.move(800,500)
        self.bro5.setFont(QtGui.QFont("Helvetica",12))
        #TextBrower
        self.bro6 = QTextBrowser(self)
        self.bro6.resize(250,300)
        self.bro6.move(1300,500)
        self.bro6.setFont(QtGui.QFont("Helvetica",12))

        #DateEdit
        self.Year = int(datetime.now().strftime('%Y'))
        self.Month = int(datetime.now().strftime('%m'))
        self.Day = int(datetime.now().strftime('%d'))
        self.dateEdit = QDateEdit(self)
        self.dateEdit.setMaximumDate(QtCore.QDate(self.Year,self.Month,self.Day))
        self.dateEdit.setMaximumTime(QtCore.QTime(23, 59, 59))
        self.dateEdit.setDate(QtCore.QDate(self.Year,self.Month,self.Day-1))
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.resize(150,50)
        self.dateEdit.move(500,50)
        self.dateEdit.setFont(QtGui.QFont("Helvetica",12))
        #DateEdit
        self.dateEdit1 = QDateEdit(self)
        self.dateEdit1.setMaximumDate(QtCore.QDate(self.Year,self.Month,self.Day))
        self.dateEdit1.setMaximumTime(QtCore.QTime(23, 59, 59))
        self.dateEdit1.setDate(QtCore.QDate(2021, 11, 2))
        self.dateEdit1.setCalendarPopup(True)
        self.dateEdit1.resize(150,50)
        self.dateEdit1.move(500,200)
        self.dateEdit1.setFont(QtGui.QFont("Helvetica",12))

        self.view = QTableView(self)
        self.view.resize(750,500)
        self.view.move(10,350)

    #readfile .csv
    def read_file(self,query):
        pan = pd.read_csv(str(query)+'_Data.csv')
        df = pd.DataFrame({'time': pan['time'],'tweet': pan['tweet']})
        model = pandasModel(df)
        self.view.setModel(model)


    #readfile .csv
    def read_file_10rank(self,query):
        self.dic10={}
        df = pandas.read_csv(str(query)+'_NLP.csv')
        for colume in df:
            self.dic10[colume]=[]
            for data in df[colume]:
                self.dic10[colume].append(data)
        self.bro2.clear()
        self.bro2.append('10 Ranking word')
        for word in self.dic10['10 ranking']:
            self.bro2.append(word)

    #show Graph ranking by pyqchart
    def create_piechart(self,data):
        pan = pandas.read_csv(str(data)+'_NLP.csv')
        se = QPieSeries()
        for i,j in zip(pan['10 ranking'],pan['number']):
            se.append(i,int(j))

        chart = QChart()
        chart.addSeries(se)
        chart.setTitle("Programming Pie Chart")
        chartview = QChartView(chart)
        chartview.setGeometry(0,0,650,500)
        chartview.setRenderHint(QPainter.Antialiasing)

        self.savepi = QPixmap(chartview.grab())
        self.savepi.save("C:/Users/Lenovo/Desktop/New folder/10_Rank_API.png", "PNG")
        self.bro3.setStyleSheet('border-image:url(C:/Users/Lenovo/Desktop/New folder/10_Rank_API.png);')


    #update datetime
    def update_time(self):
        data = self.inputbox.text()
        slide = self.slide.currentText()
        date1 = self.dateEdit.date().toPyDate()
        date2 = self.dateEdit1.date().toPyDate()
        obj = Twitter_API(data,slide,date1,date2)
        obj.search()
        obj1 = NLP(data)
        obj1.save_analysis(slide,data)
        self.read_file(data)
        self.read_file_10rank(data)
        self.create_piechart(data)
        self.Sentiment(data,slide)
        self.get_time(data)
    
    #check sentiment language
    def Sentiment(self,data,slide):
        if slide == 'th':
            self.sentiment_pickel(data)
        elif slide == 'en':
            self.Sentiment_en(data)
    
    def Sentiment_en(self,data):
        #Part-2: Sentiment Analysis Report
        df = pd.read_csv(str(data)+'_Data.csv')
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
        #print("Total Positive = ", self.pos)
        #print("Total Negative = ", self.neg)
        #print("Total Neutral = ", self.neu)

        se = QPieSeries()

        se.append('Positive',int(pos))
        se.append('Negative',int(neg))
        se.append('Neutral',int(neu))
        self.bro6.clear()
        self.bro6.append(f"Total Positive = {pos}")
        self.bro6.append(f"Total Negative = {neg}")
        self.bro6.append(f"Total Neutral = {neu}")
        self.bro6.append(f"Total All = {tol}")

        chart = QChart()
        chart.addSeries(se)
        chart.setTitle("Sentiment"+str(data))
        chartview = QChartView(chart)
        chartview.setGeometry(0,0,600,500)
        chartview.setRenderHint(QPainter.Antialiasing)

        self.savepi = QPixmap(chartview.grab())
        self.savepi.save("C:/Users/Lenovo/Desktop/New folder/Sentiment_api.png", "PNG")
        self.bro5.setStyleSheet('border-image:url(C:/Users/Lenovo/Desktop/New folder/Sentiment_api.png);')

        with open(str(data)+'_api_sentiment.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['pos','neg','neu'])
            writer.writerow([pos,neg,neu])
    
    def Sentiment_th(self,data):

        # pos.txt
        with codecs.open('pos.txt', 'r', "utf-8") as f:
            lines = f.readlines()
        listpos=[e.strip() for e in lines]
        f.close() # ปิดไฟล์

        # neu.txt
        with codecs.open('neu.txt', 'r', "utf-8") as f:
            lines = f.readlines()
        listneu=[e.strip() for e in lines]
        f.close() # ปิดไฟล์

        # neg.txt
        with codecs.open('neg.txt', 'r', "utf-8") as f:
            lines = f.readlines()
        listneg=[e.strip() for e in lines]
        f.close() # ปิดไฟล์

        pos1=['pos']*len(listpos)
        neg1=['neg']*len(listneg)
        neu1=['neu']*len(listneu)

        training_data = list(zip(listpos,pos1)) + list(zip(listneg,neg1)) + list(zip(listneu,neu1))
        vocabulary = set(chain(*[word_tokenize(i[0].lower()) for i in training_data]))
        feature_set = [({i:(i in word_tokenize(sentence.lower())) for i in vocabulary},tag) for sentence, tag in training_data]
        classifier = nbc.train(feature_set)

        totel = (classifier,vocabulary)
        return totel

    def storeData(self): 
        # database 
        db = self.main_mo()
        # Its important to use binary mode 
        dbfile = open('Model', 'wb') 
        # source, destination
        pickle.dump(db, dbfile)
        dbfile.close()

    def loadData(self):
        # for reading also binary mode is important
        dbfile = open('Model', 'rb')
        db = pickle.load(dbfile)
        dbfile.close()
        return db

    #analysis th word
    def analyze_word_th(self, data):
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

    def sentiment_pickel(self,data):
        df = pd.read_csv(str(data)+'_Data.csv')
        A = self.loadData()
        pos = 0
        neg = 0
        neu = 0

        for tweet in df['tweet']:
            test_sentence = tweet
            featurized_test_sentence =  {i:(i in self.analyze_word_th(test_sentence.lower())) for i in A[1]}
            if A[0].classify(featurized_test_sentence) == 'pos':
                pos = pos+1
            elif A[0].classify(featurized_test_sentence) == 'neg':
                neg = neg+1
            else:
                neu = neu+1
        tol = pos + neg + neu
        se = QPieSeries()

        se.append('Positive',int(pos))
        se.append('Negative',int(neg))
        se.append('Neutral',int(neu))

        print("Total Positive = ", pos)
        print("Total Negative = ", neg)
        print("Total Neutral = ", neu)

        self.bro6.clear()
        self.bro6.append(f"Total Positive = {pos}")
        self.bro6.append(f"Total Negative = {neg}")
        self.bro6.append(f"Total Neutral = {neu}")
        self.bro6.append(f"Total All = {tol}")

        chart = QChart()
        chart.addSeries(se)
        chart.setTitle("Sentiment"+str(data))
        chartview = QChartView(chart)
        chartview.setGeometry(0,0,600,500)
        chartview.setRenderHint(QPainter.Antialiasing)

        self.savepi = QPixmap(chartview.grab())
        self.savepi.save("C:/Users/Lenovo/Desktop/New folder/Sentiment_api.png", "PNG")
        self.bro5.setStyleSheet('border-image:url(C:/Users/Lenovo/Desktop/New folder/Sentiment_api.png);')

        with open(str(data)+'_api_sentiment.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['pos','neg','neu'])
            writer.writerow([pos,neg,neu])


    def show_sentiment(self,data):
        df = pd.read_csv(str(data)+'_api_sentiment.csv')
        pos = 0
        neg = 0
        neu = 0
        for i,j,k in zip(df['pos'],df['neg'],df['neu']):
            pos = i
            neg = j
            neu = k
        tol = pos + neg + neu
        se = QPieSeries()

        se.append('Positive',int(pos))
        se.append('Negative',int(neg))
        se.append('Neutral',int(neu))
        print("Total Positive = ", pos)
        print("Total Negative = ", neg)
        print("Total Neutral = ", neu)

        self.bro6.clear()
        self.bro6.append(f"Total Positive = {pos}")
        self.bro6.append(f"Total Negative = {neg}")
        self.bro6.append(f"Total Neutral = {neu}")
        self.bro6.append(f"Total All = {tol}")

        chart = QChart()
        chart.addSeries(se)
        chart.setTitle("Sentiment"+str(data))
        chartview = QChartView(chart)
        chartview.setGeometry(0,0,600,500)
        chartview.setRenderHint(QPainter.Antialiasing)

        self.savepi = QPixmap(chartview.grab())
        self.savepi.save("C:/Users/Lenovo/Desktop/New folder/Sentiment_api.png", "PNG")
        self.bro5.setStyleSheet('border-image:url(C:/Users/Lenovo/Desktop/New folder/Sentiment_api.png);')

    def get_time(self,data):
        self.date1 = self.dateEdit.date().toPyDate()
        self.date2 = self.dateEdit1.date().toPyDate()

        day_1,day_2 = str(self.date1.day), str(self.date2.day)
        month1,month2 = str(self.date1.month), str(self.date2.month)
        year1, year2 = str(self.date1.year), str(self.date2.year)
        #print(day_1,month1,year1)
    
        pan = pandas.read_csv(str(data)+'_Data.csv')
        if len(day_1) == 1:
            day_1 = '0' + day_1
        if len(day_2) == 1:
            day_2 = '0' + day_2
        if len(month1) == 1: 
            month1 = '0' + month1
        if len(month2) == 1:
            month2 = '0' + month2
        
        since = f'{year1}-{month1}-{day_1}'
        until = f'{year2}-{month2}-{day_2}'

        colume1 = pan['time'] >= f'{year1}-{month1}-{day_1} 00:00:00'
        colume2 = pan['time'] <= f'{year2}-{month2}-{day_2} 23:59:59'
        between = pan[colume1 & colume2]
        print(between)
        df = pd.DataFrame({'time': between['time'],'tweet': between['tweet']})
        model = pandasModel(df)
        self.view.setModel(model)

    #Show and Exit
    def show_exit(self):
        self.show()

class pandasModel(QAbstractTableModel):
    
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role= Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    A = tweety_search()
    A.show_exit()
    sys.exit(app.exec_())