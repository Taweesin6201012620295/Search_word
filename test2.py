import csv
import pandas
from NLP import *

def analyze_word_en(data=""):
        data = re.sub("[0-9]",'',data)
        self.output = []
        self.check = {}
        self.nlp = spacy.load("en_core_web_md")
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
                                and self.filter_type(word))
            if( self.twitter_check ):
                self.output.append(word.text)
        return self.output
check_search(str(input()))

csvfile_output = open(str(data)+'_NLP.csv', 'w', newline='', encoding="utf-8")
fieldnames = ['word', 'number']
writer_output = csv.DictWriter( csvfile_output, fieldnames=fieldnames )
writer_output.writeheader()
    for temp in sort:
        writer_output.writerow({'word':temp,'number':sort[temp]})

#creating button QPushButton
        self.button2 = QPushButton("clear",self)
        self.button2.resize(200,40)
        self.button2.move(10,250)
        self.button2.clicked.connect(self.update_time)
        self.button2.setFont(QtGui.QFont("Helvetica",14))

    #show Graph ranking by matplotlib
    def Mathplot(self):
        pan = pandas.read_csv('tweet_NLP_2.csv')
        labels = []
        sizes = []
        for i,j in zip(pan['word'],pan['number']):
            labels.append(i)
            sizes.append(j)
        fig1, ax1 = plt.subplots()

        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
        ax1.axis('equal')
        ax1.figure.savefig('C:/Users/Lenovo/Desktop/New folder/abc.png')
        self.bro4.setStyleSheet('border-image:url(C:/Users/Lenovo/Desktop/New folder/abc.png);')

import os
import time

modTimesinceEpoc = os.path.getmtime('covid_Data.csv')
modificationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modTimesinceEpoc))
print("Last Modified Time : ", modificationTime )

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtChart import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5 import *

from Gui1 import*

class test(QWidget):
    def __init__(self): 
        #QApplication
        super().__init__()
        self.title = "PyQt5 QDialog"
        self.UI()

    def UI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(500,200,300,250)

        vbox = QVBoxLayout()

        self.btn = QPushButton("Open Second Dailog")
        self.btn.setFont(QtGui.QFont("Sanserif",15))
        self.btn.clicked.connect(self.second)
        vbox.addWidget(self.btn)
        self.setLayout(vbox)
        self.show()

    def second(self):
        my = QDialog(tweety_search())
        my.setModal(True)
        my.exec_()

App = QApplication(sys.argv)
A = test()
sys.exit(App.exec_())

###########################################################################################################
# refference https://www.youtube.com/watch?v=a9Mynu6pC4U&t=36s&ab_channel=ParwizForogh
import tweepy
from textblob import TextBlob
from PyQt5.QtWidgets import*
import sys
from PyQt5.QtChart import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import pandas

class window(QMainWindow):
    def __init__(self,query):
        super().__init__()
        consumer_key = 'a9H686ql30kmQTdtk5rlMX9fM'
        consumer_key_secret = 'R4czxY30ilsHjYB4wxTaJidesJKV2oacvFROPUrG8QXDlGjGON'
        access_token = '1348153243323355137-XlYJi94nnDHAmEO8Nxgd0yKxgLKYHU'
        access_token_secret = 'dIDtWvh6yxMrHOCpAFYqSHxZcC9uAw0znALAlbyX7rvMX'
        auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
        auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

        query = query
        max_tweets = 100
        searched_tweets = [status for status in tweepy.Cursor(self.api.search, q=query).items(max_tweets)]
        print(searched_tweets)
        #Part-2: Sentiment Analysis Report

        #Finding sentiment analysis (+ve, -ve and neutral)
        self.pos = 0
        self.neg = 0
        self.neu = 0
        for tweet in searched_tweets:
            analysis = TextBlob(tweet.text)
            if analysis.sentiment[0]>0:
                self.pos = self.pos +1
            elif analysis.sentiment[0]<0:
                self.neg = self.neg + 1
            else:
                self.neu = self.neu + 1

        print("Total Positive = ", self.pos)
        print("Total Negative = ", self.neg)
        print("Total Neutral = ", self.neu)
        
        self.setWindowTitle("PyQt PieChart")
        self.setGeometry(0,0,600,500)
        self.create_piechart()
        self.show()

    def create_piechart(self):
        se = QPieSeries()

        se.append('Positive',int(self.pos))
        se.append('Negative',int(self.neg))
        se.append('Neutral',int(self.neu))

        chart = QChart()
        chart.addSeries(se)
        chart.setTitle("Programming Pie Chart")
        chartview = QChartView(chart)
        chartview.setGeometry(0,0,600,500)
        chartview.setRenderHint(QPainter.Antialiasing)

        self.savepi = QPixmap(chartview.grab())
        self.label5 = QLabel(self)
        self.label5.setPixmap(self.savepi)
        self.label5.resize(chartview.width(), chartview.height())
        self.label5.move(0,0)
        self.savepi.save("C:/Users/Lenovo/Desktop/New folder/Sentiment.png", "PNG")

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window1 = window(str(input()))
    sys.exit(App.exec_())

#########################################################################3
 def emotion(self,path):
        #sentiment
        df = pd.read_csv(path)
        pos = 0
        neg = 0
        neu = 0
        for tweet in df['text']:
            analysis = TextBlob(tweet)
            if analysis.sentiment[0]>0:  #1 is positive
                    pos +=  1
            elif analysis.sentiment[0]<0: #-1 is a negative
                    neg +=  1
            else:   # 0 is independent  
                    neu +=  1

        se = QPieSeries()
        se.append('Positive',pos)
        se.append('Negative',neg)
        se.append('Neutral',neu)

        chart = QChart()
        chart.addSeries(se)
        chart.setTitle('Sentiment')

        chartview = QChartView(chart)
        chartview.setGeometry(0,0,521,421)
        chartview.setRenderHint(QPainter.Antialiasing)

        self.saveapi = QPixmap(chartview.grab())
        self.saveapi.save('C:/software/software2/pic/sent.png','PNG')
        self.sent.setStyleSheet('border-image: url(C:/software/software2/pic/sent.png);')

def Creater(self):
        self.setWindowTitle('Login')
        self.resize(800,400)

        self.button = QPushButton('API')
        self.button.clicked.connect(self.login)
        self.button.resize(100,30)
        self.button.move(200,100)
        self.button.setFont(QtGui.QFont("Helvetica",14))

        self.button2 = QPushButton('Crawler')
        self.button2.clicked.connect(self.login1)
        self.button2.resize(100,30)
        self.button2.move(400,100)
        self.button2.setFont(QtGui.QFont("Helvetica",14))


    def login(self):
        self.switch_window.emit()

    def login1(self):
        self.switch_window1.emit()

#creating button QPushButton
        self.button1 = QPushButton("twitter_API",self)
        self.button1.resize(150,80)
        self.button1.move(1600,30)
        self.button1.setFont(QtGui.QFont("Helvetica",14))
        #creating button QPushButton
        self.button2 = QPushButton("Web_Crawler",self)
        self.button2.resize(150,80)
        self.button2.move(1600,100)
        self.button2.setFont(QtGui.QFont("Helvetica",14))v
##############################################################################
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtChart import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5 import *

class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        self.dateEdit = QDateEdit(self)
        self.lbl = QLabel()
        self.dateEdit.setMaximumDate(QtCore.QDate(7999, 12, 28))
        self.dateEdit.setMaximumTime(QtCore.QTime(23, 59, 59))
        self.dateEdit.setCalendarPopup(True)

        layout = QGridLayout()
        layout.addWidget(self.dateEdit)
        layout.addWidget(self.lbl)
        self.setLayout(layout)

        self.dateEdit.dateChanged.connect(self.onDateChanged)

    def onDateChanged(self, qDate):
        print('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('MyWindow')

    main = MyWindow()
    main.show()

    sys.exit(app.exec_())

################################################################################
def analyze_word_en1(self, data=""):
        data = re.sub("[0-9]",'',data)
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
                                and self.filter_type(word))
            if( self.twitter_check ):
                self.output.append(word.text)
        return self.output

######################################################################################3

#Show Sentiment
    def show_sentiment(self,data):
        df = pd.read_csv(str(data)+'_crawler_sentiment.csv')
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
        self.bro4.setStyleSheet('border-image:url(C:/Users/Lenovo/Desktop/New folder/Sentiment_api.png);')

#########################################################################################################################

'''def check_search(self,data,slide,date1,date2): # Fucntion check search word
        pan = pandas.read_csv('file_list_API.csv')
        check = str(data)+'.csv'
        store_file = []
        for i in pan['file_name']:  #Check word search in file_list_API
            store_file.append(i)
        if check not in store_file:
            obj = Twitter_API(data,slide,date1,date2)
            obj.search()
            print("This one :"+data)
            self.obj1 = NLP(data,'api')
            self.obj1.save_analysis(slide,data,'api')
            self.read_file(data)
            self.read_file_10rank(data)
            self.create_piechart(data)
            self.get_time(data)

        else:
            self.read_file(data)
            self.read_file_10rank(data)
            self.get_time(data)
            self.create_piechart(data)
            self.show_sentiment(data)'''

###########################################################################################################################

'''def check_search(self,data,slide): # Fucntion check search word
        pan = pandas.read_csv('file_list_Crawler.csv')
        check = str(data)+'.csv'
        store_file = []
        for i in pan['file_name']: #Check word search in file_list_Crawler
            store_file.append(i)
        if check not in store_file: 
            crawler = Search_Crawler()
            crawler.check_lan(data)
            print("This one :"+ data)
            self.obj1 = NLP(data,'crawler')
            self.obj1.save_analysis(slide,data,'crawler')


        else:
            '''
