import sys
import unittest
from PyQt5.QtWidgets import *
from PyQt5.QtChart import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5 import *
import pandas as pd
from textblob import TextBlob
from nltk import NaiveBayesClassifier as nbc
from pythainlp.tokenize import word_tokenize
import codecs
from itertools import chain
import pickle
import os.path, time
from datetime import time

from Crawler_file1 import *
from NLP import *

class TestNumber(unittest.TestCase): # Test Unit test
    def test_main(self):
        controller = Controller()
        self.assertIsNotNone(controller)

class Progress(QThread): # Class progress bar

    _signal = pyqtSignal(int)

    def __init__(self):
        super(Progress, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        for i in range(100):
            time.sleep(0.05)
            self._signal.emit(i)

class Crawler_thread(QObject): # Class progress bar

    signal1 = pyqtSignal(str)
    signal2 = pyqtSignal(object)
    signal3 = pyqtSignal(str,int,int,int,int)
    finished = pyqtSignal()
    
    def __init__(self,data,slide,date1,date2):
        super().__init__()
        self.data = data
        self.slide = slide
        self.date1 = date1
        self.date2 = date2
    
    def check_search(self): # Fucntion check search word
        pan = pandas.read_csv('file_list_Crawler.csv')
        check = str(self.data)+'.csv'
        store_file = []
        for i in pan['file_name']: #Check word search in file_list_Crawler
            store_file.append(i)
        if check not in store_file: 
            crawler = Search_Crawler()
            crawler.check_lan(self.data)
            print("This one :"+ self.data)
            self.obj1 = NLP(self.data,'crawler')
            self.obj1.save_analysis(self.slide,self.data,'crawler')
            self.signal1.emit(self.data)
            self.get_time()

        else:
            self.get_time()
            self.signal1.emit(self.data)
            self.get_time()

        self.finished.emit()
    #Sentiment English
    def Sentiment_en(self):
        #Part-2: Sentiment Analysis Report
        #Finding sentiment analysis (+ve, -ve and neutral)
        pos = 0
        neg = 0
        neu = 0
        for tweet in self.df['Description']:
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

        self.signal3.emit(self.data,pos,neg,neu,tol)

    #Load Pickle
    def loadData(self):
        # for reading also binary mode is important
        dbfile = open('Model', 'rb')
        db = pickle.load(dbfile)
        dbfile.close()
        return db

    #Sentiment Thai
    def sentiment_pickel(self):
        A = self.loadData()
        pos = 0
        neg = 0
        neu = 0

        for data in self.df['Description']:

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

            featurized_test_sentence =  {i:(i in V) for i in A[1]}
            if A[0].classify(featurized_test_sentence) == 'pos':
                pos = pos+1
            elif A[0].classify(featurized_test_sentence) == 'neg':
                neg = neg+1
            else:
                neu = neu+1

        tol = pos + neg + neu
        
        self.signal3.emit(self.data,pos,neg,neu,tol)

    def get_time(self): # Function Get time from dateEdit


        day_1,day_2 = str(self.date1.day), str(self.date2.day)
        month1,month2 = str(self.date1.month), str(self.date2.month)
        year1, year2 = str(self.date1.year), str(self.date2.year)
        #print(day_1,month1,year1)
    
        pan = pandas.read_csv(str(self.data)+'_crawler.csv',error_bad_lines=False)
        if len(day_1) == 1:
            day_1 = '0' + day_1
        if len(day_2) == 1:
            day_2 = '0' + day_2
        if len(month1) == 1: 
            month1 = '0' + month1
        if len(month2) == 1:
            month2 = '0' + month2

        colume1 = pan['Posted'] >= f'{year1}-{month1}-{day_1} 00:00:00'
        colume2 = pan['Posted'] <= f'{year2}-{month2}-{day_2} 23:59:59'
        between = pan[colume1 & colume2]
        self.df = pd.DataFrame({'Posted': between['Posted'],'Description': between['Description'],'Link': between['Link']})
        if re.match('[ก-๙]',self.data) != None:
            self.sentiment_pickel()
        else:
            self.Sentiment_en()
        print(self.df)

        self.signal2.emit(self.df.sort_values(by="Posted"))


class Crawler_search(QWidget):

    switch_window1 = QtCore.pyqtSignal()

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

        self.thread = QThread()
        self.worker = Crawler_thread(data,slide,date1,date2) 

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.check_search)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.signal1.connect(self.Link)
        self.worker.signal2.connect(self.Link2)
        self.worker.signal3.connect(self.Link3)
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
        self.switch_window1.emit()

    #creating title QMainWindow
    def Creater(self):
        self.setWindowTitle("Web Crawler")
        self.resize(1780,920)
        self.move(50,50)

        #creating box QLineEdit
        self.inputbox = QLineEdit(self)
        self.inputbox.resize(300,30)
        self.inputbox.move(10,100)
        self.inputbox.setFont(QtGui.QFont("Helvetica",16))
        
        #creating progress bar
        self.pbar = QProgressBar(self)
        self.pbar.setValue(0)
        self.pbar.resize(300,30)
        self.pbar.move(10,200)

        #creating button QPushButton
        self.button = QPushButton("Enter",self)
        self.button.resize(100,30)
        self.button.move(320,100)
        self.button.clicked.connect(self.getTextValue)
        self.button.setFont(QtGui.QFont("Helvetica",14))
        #creating button QPushButton
        self.button2 = QPushButton("Back",self)
        self.button2.resize(150,80)
        self.button2.move(1600,800)
        self.button2.clicked.connect(self.Back)
        self.button2.setFont(QtGui.QFont("Helvetica",14))
        #creating button QPushButton
        self.button3 = QPushButton("Update Datetime",self)
        self.button3.resize(200,40)
        self.button3.move(10,250)
        self.button3.clicked.connect(self.update_time)
        self.button3.setFont(QtGui.QFont("Helvetica",14))
        #creating button QPushButton
        self.button4 = QPushButton("Compare",self)
        self.button4.resize(150,80)
        self.button4.move(1600,100)
        self.button4.setFont(QtGui.QFont("Helvetica",14))

        #set icon window
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap("../../Downloads/web-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(self.icon)

        #QLabel1
        self.label_1 = QLabel('Enter your word',self)
        self.label_1.move(20, 50)
        self.label_1.setFont(QtGui.QFont("Helvetica",20))
        #QLabel2
        self.label_2 = QLabel('10 Ranking word',self)
        self.label_2.move(800,15)
        self.label_2.setFont(QtGui.QFont("Helvetica",16))
        #QLabel3
        self.label_3 = QLabel('Sentiment',self)
        self.label_3.move(800,470)
        self.label_3.setFont(QtGui.QFont("Helvetica",16))
        #QLabel4
        self.label_4 = QLabel('Link of search word',self)
        self.label_4.move(20,300)
        self.label_4.setFont(QtGui.QFont("Helvetica",16))
        #QLabel5
        self.label_5 = QLabel('Select your language',self)
        self.label_5.move(20,150)
        self.label_5.setFont(QtGui.QFont("Helvetica",16))
        #QLabel7
        self.label_7 = QLabel('Since',self)
        self.label_7.move(500,10)
        self.label_7.setFont(QtGui.QFont("Helvetica",16))
        #QLabel7
        self.label_8 = QLabel('Until',self)
        self.label_8.move(500,150)
        self.label_8.setFont(QtGui.QFont("Helvetica",16))
        
        #ComboBox th and en
        self.slide = QComboBox(self)
        self.slide.addItem('th')
        self.slide.addItem('en')
        self.slide.move(280,150)
        self.slide.setFont(QtGui.QFont("Helvetica",16))

        #TextBrowser
        self.bro2 = QTextBrowser(self)
        self.bro2.resize(500,400)
        self.bro2.move(800,50)
        self.bro2.setFont(QtGui.QFont("Helvetica",12))
        #TextBrower
        self.bro4 = QTextBrowser(self)
        self.bro4.resize(500,400)
        self.bro4.move(800,500)
        self.bro4.setFont(QtGui.QFont("Helvetica",12))
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
        self.dateEdit.setDate(QtCore.QDate(2021, 11, 2))
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

    def signal_accept(self, msg): # Function Progress bar
        self.pbar.setValue(int(msg))
        if self.pbar.value() == 99:
            self.pbar.setValue(0)
    
    def Link(self,data):
        self.read_file_10rank(data)
    
    def Link2(self,df):
        model = pandasModel(df)
        self.view.setModel(model)
    
    def Link3(self,data,pos,neg,neu,tol):
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
        self.bro4.setStyleSheet('border-image:url(C:/Users/Lenovo/Desktop/New folder/Sentiment_api.png);')

        with open(str(data)+'_crawler_sentiment.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['pos','neg','neu'])
            writer.writerow([pos,neg,neu])
        self.button.setEnabled(True)
        self.button3.setEnabled(True)

    #Posted Headline and Link of word
    def read_file(self,query):
        pan = pd.read_csv(str(query)+'_crawler.csv',error_bad_lines=False)
        df = pd.DataFrame({'Posted': pan['Posted'],'Headline': pan['Headline'],'Link': pan['Link']})
        model = pandasModel(df)
        self.view.setModel(model)
    
    #10 Ranking word
    def read_file_10rank(self,query):
        self.dic10={}
        df = pandas.read_csv(str(query)+'_NLP_crawler.csv')
        for colume in df:
            self.dic10[colume]=[]
            for data in df[colume]:
                self.dic10[colume].append(data)
        self.bro2.clear()
        self.bro2.append('10 Ranking word')
        for word in self.dic10['10 ranking']:
            self.bro2.append(word)


    def show_exit(self):
        self.show()


    def update_time(self): # Function Update time
        data = self.inputbox.text()
        slide = self.slide.currentText()
        crawler = Search_Crawler()
        crawler.check_lan(data)
        print("This one :"+ data)
        self.obj1 = NLP(data,'crawler')
        self.obj1.save_analysis(slide,data,'crawler')
        self.read_file(data)
        self.read_file_10rank(data)
        self.get_time(data)


class pandasModel(QAbstractTableModel): #Class for creat AbstractTableModel
    
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
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
    A = Crawler_search()
    A.show_exit()
    sys.exit(app.exec_())