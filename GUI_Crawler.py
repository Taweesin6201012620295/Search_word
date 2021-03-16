import sys
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

from Crawler_file1 import *
from NLP_crawler import *
from test_crawler2 import * 

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
        self.check_search(data,slide)
    
    def check_search(self,data,slide):
        pan = pandas.read_csv('file_list_Crawler.csv')
        check = str(data)+'.csv'
        store_file = []
        for i in pan['file_name']:
            store_file.append(i)
        if check not in store_file:
            if slide == 'th':
                crawler = Search_thai_Crawler()
                crawler.get_thai_news(data)
                print("This one :"+data)
                self.obj1 = NLP_crawler(data)
                self.obj1.save_analysis(slide,data)
                self.read_file(data)
                self.read_file_10rank(data)
                self.Sentiment(data,slide)

            elif slide == 'en':
                crawler2 = Search_Crawler()
                crawler2.get_the_news(data)
                print("This one :"+data)
                self.obj1 = NLP_crawler(data)
                self.obj1.save_analysis(slide,data)
                self.read_file(data)
                self.read_file_10rank(data)
                self.Sentiment(data,slide)
        else:
            self.read_file(data)
            self.read_file_10rank(data)
            self.show_sentiment(data)

    def Back(self):
        self.switch_window1.emit()

    #creating title QMainWindow
    def Creater(self):
        self.setWindowTitle("Web Crawler")
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
        #self.button4.clicked.connect(self.Back)
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
        #QLabel2
        self.label_5 = QLabel('Select your language',self)
        self.label_5.move(20,150)
        self.label_5.setFont(QtGui.QFont("Helvetica",16))
        
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


        self.view = QTableView(self)
        self.view.resize(750,500)
        self.view.move(10,350)

    def read_filebro(self,query):
        self.dic={}
        df = pandas.read_csv(str(query)+'_crawler.csv')
        for colume in df:
            self.dic[colume]=[]
            for data in df[colume]:
                self.dic[colume].append(data)
        self.bro.clear()
        for word in self.dic['Link'][0:10]:
            self.bro.append(word)

    #readfile .csv
    def read_file(self,query):
        pan = pd.read_csv(str(query)+'_crawler.csv')
        df = pd.DataFrame({'Posted': pan['Posted'],'Headline': pan['Headline'],'Link': pan['Link']})
        model = pandasModel(df)
        self.view.setModel(model)
    
    #readfile .csv
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

    #check sentiment language
    def Sentiment(self,data,slide):
        if slide == 'th':
            self.Sentiment_th(data)
        elif slide == 'en':
            self.Sentiment_en(data)

    def Sentiment_en(self,data):
        
        #Part-2: Sentiment Analysis Report
        df = pd.read_csv(str(data)+'_crawler.csv')
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
        self.bro6.clear()
        self.bro6.append(f"Total Positive = {pos}")
        self.bro6.append(f"Total Negative = {neg}")
        self.bro6.append(f"Total Neutral = {neu}")
        self.bro6.append(f"Total All = {tol}")

        chart = QChart()
        chart.addSeries(se)
        chart.setTitle("Programming Pie Chart")
        chartview = QChartView(chart)
        chartview.setGeometry(0,0,600,500)
        chartview.setRenderHint(QPainter.Antialiasing)

        self.savepi = QPixmap(chartview.grab())
        self.savepi.save("C:/Users/Lenovo/Desktop/New folder/Sentiment_crawler.png", "PNG")
        self.bro4.setStyleSheet('border-image:url(C:/Users/Lenovo/Desktop/New folder/Sentiment_crawler.png);')
        
        with open(str(data)+'_sentiment.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['pos','neg','neu'])
            writer.writerow([pos,neg,neu])

    def Sentiment_th(self,data):
        df = pd.read_csv(str(data)+'_crawler.csv')
        pos = 0
        neg = 0
        neu = 0

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

        for tweet in df['Description']:
            test_sentence = tweet
            featurized_test_sentence =  {i:(i in word_tokenize(test_sentence.lower())) for i in vocabulary}
            if classifier.classify(featurized_test_sentence) == 'pos':
                pos = pos+1
            elif classifier.classify(featurized_test_sentence) == 'neg':
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
        chart.setTitle("Programming Pie Chart")
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

    def show_sentiment(self,data):
        df = pd.read_csv(str(data)+'_sentiment.csv')
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
        chart.setTitle("Programming Pie Chart")
        chartview = QChartView(chart)
        chartview.setGeometry(0,0,600,500)
        chartview.setRenderHint(QPainter.Antialiasing)

        self.savepi = QPixmap(chartview.grab())
        self.savepi.save("C:/Users/Lenovo/Desktop/New folder/Sentiment_api.png", "PNG")
        self.bro4.setStyleSheet('border-image:url(C:/Users/Lenovo/Desktop/New folder/Sentiment_api.png);')

    def show_pic(self):
        self.bro4.setStyleSheet('border-image:url(C:/Users/Lenovo/Desktop/New folder/Sentiment_api.png);')
        self.bro4.setStyleSheet('border-image:url(C:/Users/Lenovo/Desktop/New folder/Sentiment_crawler.png);')

    def show_exit(self):
        self.show()

    def update_time(self):
        data = self.inputbox.text()
        slide = self.slide.currentText()
        crawler = Search_Crawler()
        crawler.get_the_news(data)
        self.obj1 = NLP_crawler(data)
        self.obj1.save_analysis(slide,data)
        self.read_file(data)
        self.read_file_10rank(data)
        self.Sentiment(data,slide)


class pandasModel(QAbstractTableModel):
    
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