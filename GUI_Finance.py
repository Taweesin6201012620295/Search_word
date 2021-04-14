
from PyQt5.QtWidgets import *
from PyQt5.QtChart import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5 import *

from datetime import datetime, date

import re
import unittest
from pandas_datareader import data as pdr
import pandas as pd
import sys
import csv
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mpl_dates

from API import Twitter_API
from NLP import *

from Crawler_file1 import *

from Combine_GUI import*

class TestNumber(unittest.TestCase): # Test Unit test
    def test_main(self):
        controller = Controller()
        self.assertIsNotNone(controller)

class Progress(QThread): # Class progress bar

    finised = pyqtSignal()
    _signal = pyqtSignal(int)
    def __init__(self):
        super(Progress, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        for i in range(100):
            time.sleep(0.05)
            self._signal.emit(i)
        self.finised.emit()

class Finance_thread(QObject):

    finished = pyqtSignal()

    def __init__(self,data,data1,slide,date1,date2):
        super().__init__()
        self.data = data
        self.data = data1
        self.slide = slide
        self.date1 = date1
        self.date2 = date2

    def compare(self): # Send word to API and Crawler

        if re.match('[ก-๙]',self.data) != None: # If word is Thai word 
            
            api = Twitter_API(self.data,'th',self.date1,self.date2)
            api.search()
            crawler = Search_Crawler()
            crawler.check_lan(self.data)
            self.get_time(self.data)

        else: # If word is English word
            
            api = Twitter_API(self.data,'en',self.date1,self.date2)
            api.search()
            crawler = Search_Crawler()
            crawler.check_lan(self.data)
            self.get_time(self.data)

        self.finished.emit()

class Search_finance(QWidget):

    switch_window2 = QtCore.pyqtSignal()

    def __init__(self): 
        #QApplication
        super().__init__()
        self.Creater()

    def getTextValue(self):
        data = self.inputbox.text()
        data = self.inputbox1.text()
        date1 = self.dateEdit.date().toPyDate()
        date2 = self.dateEdit1.date().toPyDate()

        self.thread = QThread()
        self.finance = Finance_thread()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.check_search)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        #self.worker.signal.connect(self.Link)
        self.button.setEnabled(True)
        self.button3.setEnabled(True)
        self.thread.start()


        self.progress = Progress()
        self.progress._signal.connect(self.signal_accept)
        self.progress._signal.connect(self.progress.quit)
        self.progress.start()
        self.button.setEnabled(False)
        self.button3.setEnabled(False)

    def Back(self): #Back to Main GUI
        self.switch_window2.emit()

    def Creater(self):
        self.setWindowTitle("Finance")
        self.resize(1400,1000)
        self.move(50,30)

        #creating box QLineEdit
        self.inputbox = QLineEdit(self)
        self.inputbox.resize(200,30)
        self.inputbox.move(180,100)
        self.inputbox.setFont(QtGui.QFont("Helvetica",16))
        #creating box QLineEdit
        self.inputbox1 = QLineEdit(self)
        self.inputbox1.resize(200,30)
        self.inputbox1.move(180,150)
        self.inputbox1.setFont(QtGui.QFont("Helvetica",16))

        #creating progress bar
        self.pbar = QProgressBar(self)
        self.pbar.setValue(0)
        self.pbar.resize(300,30)
        self.pbar.move(10,350)

        #set icon window
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap("../../Downloads/Finance_icon_0919_250x252.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(self.icon)

        #QLabel1
        self.label_0 = QLabel('Keyword Stock',self)
        self.label_0.move(10, 100)
        self.label_0.setFont(QtGui.QFont("Helvetica",14))
        #QLabel1
        self.label_1 = QLabel('Keyword Search',self)
        self.label_1.move(10, 150)
        self.label_1.setFont(QtGui.QFont("Helvetica",14))
        #QLabel2
        self.label_2 = QLabel('Since',self)
        self.label_2.move(20, 210)
        self.label_2.setFont(QtGui.QFont("Helvetica",16))
        #QLabel3
        self.label_3 = QLabel('Until',self)
        self.label_3.move(20, 290)
        self.label_3.setFont(QtGui.QFont("Helvetica",16))
        #QLabel4
        self.label_4 = QLabel('Twitter',self)
        self.label_4.move(80, 500)
        self.label_4.setFont(QtGui.QFont("Helvetica",16))
        #QLabel5
        self.label_5 = QLabel('Web Crawler',self)
        self.label_5.move(730, 500)
        self.label_5.setFont(QtGui.QFont("Helvetica",16))
        #QLabel5
        self.label_5 = QLabel('Finance',self)
        self.label_5.move(550, 10)
        self.label_5.setFont(QtGui.QFont("Helvetica",16))

        #creating button QPushButton
        self.button = QPushButton("Stock",self)
        self.button.resize(100,30)
        self.button.move(390,100)
        self.button.clicked.connect(self.getTextValue)
        self.button.setFont(QtGui.QFont("Helvetica",14))
        #creating button QPushButton
        self.button1 = QPushButton("Search",self)
        self.button1.resize(100,30)
        self.button1.move(390,150)
        self.button1.clicked.connect(self.compare)
        self.button1.setFont(QtGui.QFont("Helvetica",14))
        #creating button QPushButton
        self.button2 = QPushButton("Back",self)
        self.button2.resize(200,60)
        self.button2.move(10,400)
        self.button2.clicked.connect(self.Back)
        self.button2.setFont(QtGui.QFont("Helvetica",14))

        #TextBrower
        self.bro1 = QTextBrowser(self)
        self.bro1.resize(500,500)
        self.bro1.move(650,0)
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
        self.dateEdit.setDate(QtCore.QDate(2021, 11, 2))
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.resize(150,40)
        self.dateEdit.move(100,210)
        self.dateEdit.setFont(QtGui.QFont("Helvetica",12))

        #DateEdit
        self.dateEdit1 = QDateEdit(self)
        self.dateEdit1.setMaximumDate(QtCore.QDate(self.Year,self.Month,self.Day))
        self.dateEdit1.setMaximumTime(QtCore.QTime(23, 59, 59))
        self.dateEdit1.setDate(QtCore.QDate(2021, 11, 2))
        self.dateEdit1.setCalendarPopup(True)
        self.dateEdit1.resize(150,40)
        self.dateEdit1.move(100,290)
        self.dateEdit1.setFont(QtGui.QFont("Helvetica",12))


    def signal_accept(self, msg): # Function Progress bar
        self.pbar.setValue(int(msg))
        if self.pbar.value() == 99:
            self.pbar.setValue(0)
            self.button.setEnabled(True)


    def stock(self,data,date1,date2): #Function search stock
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

    def plot_stock(self): #Function plot grahp stock
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
    

    def compare(self): # Send word to API and Crawler
        data = self.inputbox1.text()
        date1 = self.dateEdit.date().toPyDate()
        date2 = self.dateEdit1.date().toPyDate()
        if re.match('[ก-๙]',data) != None: # If word is Thai word 
            
            api = Twitter_API(data,'th',date1,date2)
            api.search()
            crawler = Search_Crawler()
            crawler.check_lan(data)
            self.get_time(data)

        else: # If word is English word
            
            api = Twitter_API(data,'en',date1,date2)
            api.search()
            crawler = Search_Crawler()
            crawler.check_lan(data)
            self.get_time(data)

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
    
    #Load Pickal
    def loadData(self):
        # for reading also binary mode is important
        dbfile = open('Model', 'rb')
        db = pickle.load(dbfile)
        dbfile.close()
        return db

############################ API ############################################
    
    #Sentiment English
    def Sentiment_api_en(self,data,df):
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

    #Sentiment Thai
    def Sentiment_api_pickle(self,data,df):

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
    #Sentiment English
    def Sentiment_crawler_en(self,data,df):
        
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

    #Sentiment Thai
    def Sentiment_crawler_pickle(self,data,df):

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


    def get_time(self,data): # Function Get time from dateEdit
        self.date1 = self.dateEdit.date().toPyDate()
        self.date2 = self.dateEdit1.date().toPyDate()

        day_1,day_2 = str(self.date1.day), str(self.date2.day)
        month1,month2 = str(self.date1.month), str(self.date2.month)
        year1, year2 = str(self.date1.year), str(self.date2.year)
        #print(day_1,month1,year1)
    
        pan = pandas.read_csv(str(data)+'_Data.csv')
        pan1 = pandas.read_csv(str(data)+'_crawler.csv',error_bad_lines=False)
        if len(day_1) == 1:
            day_1 = '0' + day_1
        if len(day_2) == 1:
            day_2 = '0' + day_2
        if len(month1) == 1: 
            month1 = '0' + month1
        if len(month2) == 1:
            month2 = '0' + month2

        colume = pan['time'] >= f'{year1}-{month1}-{day_1} 00:00:00'
        colume1 = pan['time'] <= f'{year2}-{month2}-{day_2} 23:59:59'
        between = pan[colume & colume1]
        
        colume2 = pan1['Posted'] >= f'{year1}-{month1}-{day_1} 00:00:00'
        colume3 = pan1['Posted'] <= f'{year2}-{month2}-{day_2} 23:59:59'
        between1 = pan1[colume2 & colume3]

        df = pd.DataFrame({'time': between['time'],'tweet': between['tweet']})
        df1 = pd.DataFrame({'time': between1['Posted'],'tweet': between1['Description']})

        print(df)
        print(df1)

        if re.match('[ก-๙]',data) != None:
            self.Sentiment_api_pickle(data,df)
            self.Sentiment_crawler_pickle(data,df1)
        else:
            self.Sentiment_api_en(data,df)
            self.Sentiment_crawler_en(data,df1)



    def show_exit(self):
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    A = Search_finance()
    A.show_exit()
    sys.exit(app.exec_())