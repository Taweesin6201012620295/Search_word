from PyQt5.QtWidgets import *
from PyQt5.QtChart import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5 import *

from datetime import datetime, date

import re
from pandas_datareader import data as pdr
import pandas as pd
import sys
import csv
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mpl_dates

from miniproject_file1 import Twitter_API
from NLP import *

from Crawler_file1 import *
from NLP_crawler import *
from Crawler_file2 import * 

from Combine_GUI import*

class search_finance(QWidget):

    switch_window2 = QtCore.pyqtSignal()

    def __init__(self): 
        #QApplication
        super().__init__()
        self.Creater()

    def getTextValue(self):
        data = self.inputbox.text()
        date1 = self.dateEdit.date().toPyDate()
        date2 = self.dateEdit1.date().toPyDate()
        self.stock(data,date1,date2)

    def Back(self):
        self.switch_window2.emit()

    def Creater(self):
        self.setWindowTitle("Finance")
        self.resize(1400,1000)

        #creating box QLineEdit
        self.inputbox = QLineEdit(self)
        self.inputbox.resize(300,30)
        self.inputbox.move(10,100)
        self.inputbox.setFont(QtGui.QFont("Helvetica",16))

        #set icon window
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap("../../Downloads/Finance_icon_0919_250x252.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(self.icon)

        #QLabel1
        self.label_1 = QLabel('Enter your Stock',self)
        self.label_1.move(20, 50)
        self.label_1.setFont(QtGui.QFont("Helvetica",18))
        #QLabel2
        self.label_2 = QLabel('Since',self)
        self.label_2.move(20, 160)
        self.label_2.setFont(QtGui.QFont("Helvetica",16))
        #QLabel3
        self.label_3 = QLabel('Until',self)
        self.label_3.move(20, 240)
        self.label_3.setFont(QtGui.QFont("Helvetica",16))
        #QLabel4
        self.label_4 = QLabel('API',self)
        self.label_4.move(80, 500)
        self.label_4.setFont(QtGui.QFont("Helvetica",16))
        #QLabel5
        self.label_5 = QLabel('Crawler',self)
        self.label_5.move(780, 500)
        self.label_5.setFont(QtGui.QFont("Helvetica",16))

        #creating button QPushButton
        self.button = QPushButton("Enter",self)
        self.button.resize(100,30)
        self.button.move(320,100)
        self.button.clicked.connect(self.getTextValue)
        self.button.setFont(QtGui.QFont("Helvetica",14))

        #creating button QPushButton
        self.button1 = QPushButton("Back",self)
        self.button1.resize(200,60)
        self.button1.move(10,400)
        self.button1.clicked.connect(self.Back)
        self.button1.setFont(QtGui.QFont("Helvetica",14))
        #creating button QPushButton
        self.button2 = QPushButton("Compare",self)
        self.button2.resize(200,60)
        self.button2.move(240,400)
        self.button2.clicked.connect(self.compare)
        self.button2.setFont(QtGui.QFont("Helvetica",14))

        #TextBrower
        self.bro1 = QTextBrowser(self)
        self.bro1.resize(500,500)
        self.bro1.move(500,0)
        self.bro1.setFont(QtGui.QFont("Helvetica",12))
        #TextBrower
        self.bro2 = QTextBrowser(self)
        self.bro2.resize(500,500)
        self.bro2.move(200,500)
        self.bro2.setFont(QtGui.QFont("Helvetica",12))
        #TextBrower
        self.bro3 = QTextBrowser(self)
        self.bro3.resize(500,500)
        self.bro3.move(900,500)
        self.bro3.setFont(QtGui.QFont("Helvetica",12))
        #TextBrower
        self.bro4 = QTextBrowser(self)
        self.bro4.resize(190,200)
        self.bro4.move(10,540)
        self.bro4.setFont(QtGui.QFont("Helvetica",12))
        #TextBrower
        self.bro5 = QTextBrowser(self)
        self.bro5.resize(190,200)
        self.bro5.move(710,540)
        self.bro5.setFont(QtGui.QFont("Helvetica",12))

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
        self.dateEdit.move(100,150)
        self.dateEdit.setFont(QtGui.QFont("Helvetica",12))
        #DateEdit
        self.dateEdit1 = QDateEdit(self)
        self.dateEdit1.setMaximumDate(QtCore.QDate(self.Year,self.Month,self.Day))
        self.dateEdit1.setMaximumTime(QtCore.QTime(23, 59, 59))
        self.dateEdit1.setDate(QtCore.QDate(2021, 11, 2))
        self.dateEdit1.setCalendarPopup(True)
        self.dateEdit1.resize(150,50)
        self.dateEdit1.move(100,230)
        self.dateEdit1.setFont(QtGui.QFont("Helvetica",12))


    def stock(self,data,date1,date2):
        stock = str(data)
        start = date1
        end = date2

        try:
            df = pdr.get_data_yahoo(stock, start=start, end=end)
            print(df.to_csv())
        except:
            print("Error:", sys.exc_info()[0])
            print("Description:", sys.exc_info()[1])

        with open('stock.csv', 'w', newline='', encoding='utf-8') as f:
            f.write(df.to_csv())
        self.plot_stock()
        plt.close('all')

    def plot_stock(self):
        plt.style.use('ggplot')

        # Extracting Data for plotting
        data = pd.read_csv('stock.csv')
        ohlc = data.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]
        ohlc['Date'] = pd.to_datetime(ohlc['Date'])
        ohlc['Date'] = ohlc['Date'].apply(mpl_dates.date2num)
        ohlc = ohlc.astype(float)

        # Creating Subplots
        fig, ax = plt.subplots()

        candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='green', colordown='red', alpha=0.8)
        # Setting labels & titles
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        fig.suptitle('Stock')


        # Formatting Date
        date_format = mpl_dates.DateFormatter('%d-%m-%Y')
        ax.xaxis.set_major_formatter(date_format)
        fig.autofmt_xdate()

        fig.tight_layout()

        # python_candlestick_chart.py

        ohlc['SMA5'] = ohlc['Close'].rolling(5).mean()
        ax.plot(ohlc['Date'], ohlc['SMA5'], color='green', label='SMA5')

        fig.suptitle('Daily Candlestick Chart of NIFTY50 with SMA5')

        plt.legend()

        plt.savefig("C:/Users/Lenovo/Desktop/New folder/stock.png")
        self.bro1.clear()
        self.bro1.setStyleSheet('border-image: url(C:/Users/Lenovo/Desktop/New folder/stock.png);')
    
    def compare(self):
        data = self.inputbox.text()
        date1 = self.dateEdit.date().toPyDate()
        date2 = self.dateEdit1.date().toPyDate()
        if re.match('[ก-๙]',data) != None:
            data = self.inputbox.text()
            api = Twitter_API(data,'th',date1,date2)
            api.search()
            crawler = Search_thai_Crawler()
            crawler.get_thai_news(data)
            self.Sentiment(data,'th')

        else:
            data = self.inputbox.text()
            api = Twitter_API(data,'en',date1,date2)
            api.search()
            crawler = Search_Crawler()
            crawler.get_eng_news(data)
            self.Sentiment(data,'en')

    #check sentiment language
    def Sentiment(self,data,lan):
        if lan == 'th':
            self.Sentiment_api_pickle(data)
            self.Sentiment_crawler_pickle(data)
        elif lan == 'en':
            self.Sentiment_crawler_en(data)
            self.Sentiment_api_en(data)

############################ API ############################################
    def Sentiment_api_en(self,data):

        #Part-2: Sentiment Analysis Report
        df = pd.read_csv(str(data)+'_Data.csv',error_bad_lines=False)
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

        se = QPieSeries()

        se.append('Positive',int(pos))
        se.append('Negative',int(neg))
        se.append('Neutral',int(neu))
        
        self.bro4.clear()
        self.bro4.append(f"Positive = {pos}")
        self.bro4.append(f"Negative = {neg}")
        self.bro4.append(f"Neutral = {neu}")
        self.bro4.append(f"All = {tol}")

        chart = QChart()
        chart.addSeries(se)
        chart.setTitle("Sentiment"+str(data))
        chartview = QChartView(chart)
        chartview.setGeometry(0,0,600,500)
        chartview.setRenderHint(QPainter.Antialiasing)

        self.savepi = QPixmap(chartview.grab())
        self.savepi.save("C:/Users/Lenovo/Desktop/New folder/Sentiment_crawler.png", "PNG")
        self.bro2.setStyleSheet('border-image:url(C:/Users/Lenovo/Desktop/New folder/Sentiment_crawler.png);')
        
        with open(str(data)+'_sentiment.csv', 'w', newline='', encoding='utf-8') as f:
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

    def Sentiment_api_pickle(self,data):
        df = pd.read_csv(str(data)+'_Data.csv',error_bad_lines=False)
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

        print(" Positive = ", pos)
        print("Total Negative = ", neg)
        print("Total Neutral = ", neu)

        self.bro4.clear()
        self.bro4.append(f"Positive = {pos}")
        self.bro4.append(f"Negative = {neg}")
        self.bro4.append(f"Neutral = {neu}")
        self.bro4.append(f"Total = {tol}")

        chart = QChart()
        chart.addSeries(se)
        chart.setTitle("Sentiment"+str(data))
        chartview = QChartView(chart)
        chartview.setGeometry(0,0,600,500)
        chartview.setRenderHint(QPainter.Antialiasing)

        self.savepi = QPixmap(chartview.grab())
        self.savepi.save("C:/Users/Lenovo/Desktop/New folder/Sentiment_api.png", "PNG")
        self.bro2.setStyleSheet('border-image:url(C:/Users/Lenovo/Desktop/New folder/Sentiment_api.png);')

        with open(str(data)+'_api_sentiment.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['pos','neg','neu'])
            writer.writerow([pos,neg,neu])

############################ Crawler ############################################
    
    def Sentiment_crawler_en(self,data):
        
        #Part-2: Sentiment Analysis Report
        df = pd.read_csv(str(data)+'_crawler.csv',error_bad_lines=False)
        #Finding sentiment analysis (+ve, -ve and neutral)
        pos = 0
        neg = 0
        neu = 0
        for tweet in df['Description']:
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

        se = QPieSeries()

        se.append('Positive',int(pos))
        se.append('Negative',int(neg))
        se.append('Neutral',int(neu))
        
        self.bro5.clear()
        self.bro5.append(f"Positive = {pos}")
        self.bro5.append(f"Negative = {neg}")
        self.bro5.append(f"Neutral = {neu}")
        self.bro5.append(f"All = {tol}")

        chart = QChart()
        chart.addSeries(se)
        chart.setTitle("Programming Pie Chart")
        chartview = QChartView(chart)
        chartview.setGeometry(0,0,600,500)
        chartview.setRenderHint(QPainter.Antialiasing)

        self.savepi = QPixmap(chartview.grab())
        self.savepi.save("C:/Users/Lenovo/Desktop/New folder/Sentiment_crawler.png", "PNG")
        self.bro3.setStyleSheet('border-image:url(C:/Users/Lenovo/Desktop/New folder/Sentiment_crawler.png);')
        
        with open(str(data)+'_sentiment.csv', 'w', newline='', encoding='utf-8') as f:
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

    def Sentiment_crawler_pickle(self,data):
        df = pd.read_csv(str(data)+'_crawler.csv',error_bad_lines=False)
        A = self.loadData()
        pos = 0
        neg = 0
        neu = 0

        for tweet in df['Description']:
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

        self.bro5.clear()
        self.bro5.append(f"Positive = {pos}")
        self.bro5.append(f"Negative = {neg}")
        self.bro5.append(f"Neutral = {neu}")
        self.bro5.append(f"All = {tol}")

        chart = QChart()
        chart.addSeries(se)
        chart.setTitle("Programming Pie Chart")
        chartview = QChartView(chart)
        chartview.setGeometry(0,0,600,500)
        chartview.setRenderHint(QPainter.Antialiasing)

        self.savepi = QPixmap(chartview.grab())
        self.savepi.save("C:/Users/Lenovo/Desktop/New folder/Sentiment_api.png", "PNG")
        self.bro3.setStyleSheet('border-image:url(C:/Users/Lenovo/Desktop/New folder/Sentiment_api.png);')

        with open(str(data)+'_crawler_sentiment.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['pos','neg','neu'])
            writer.writerow([pos,neg,neu])


    def show_exit(self):
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    A = search_finance()
    A.show_exit()
    sys.exit(app.exec_())