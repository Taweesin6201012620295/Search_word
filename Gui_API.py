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
import unittest
from datetime import time
from textblob import TextBlob
import matplotlib.pyplot as plt
from tempfile import NamedTemporaryFile
import shutil
import codecs
from itertools import chain
from nltk import NaiveBayesClassifier as nbc
from geopy.geocoders import Nominatim
import plotly.express as px

from API import *
from NLP import *
from Combine_GUI import*

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

class API_thread(QObject): # Class progress bar
    
    signal1 = pyqtSignal(str)
    signal2 = pyqtSignal(object)
    signal3 = pyqtSignal(str,int,int,int,int)
    signal4 = pyqtSignal(str)
    finished = pyqtSignal()
    
    def __init__(self,data,slide,date1,date2):
        super().__init__()
        self.data = data
        self.slide = slide
        self.date1 = date1
        self.date2 = date2
    
    def check_search(self): # Fucntion check search word

        pan = pandas.read_csv('file_list_API.csv')
        check = str(self.data)+'.csv'
        store_file = []
        for i in pan['file_name']:  #Check word search in file_list_API
            store_file.append(i)
        if check not in store_file:
            obj = Twitter_API(self.data,self.slide,self.date1,self.date2)
            obj.search()
            print("This one :"+self.data)
            self.obj1 = NLP(self.data,'api')
            self.obj1.save_analysis(self.slide,self.data,'api')
            self.signal1.emit(self.data)
            self.get_time()

        else :
            self.get_time()

        self.finished.emit()
    
    #Sentiment English
    def Sentiment_en(self):
        #Part-2: Sentiment Analysis Report
        #Finding sentiment analysis (+ve, -ve and neutral)
        pos = 0
        neg = 0
        neu = 0
        for tweet in self.df['tweet']:
            analysis = TextBlob(tweet)
            if analysis.sentiment[0]>0:
                pos = pos +1
            elif analysis.sentiment[0]<0:
                neg = neg + 1
            else:
                neu = neu + 1
        tol = pos + neg + neu

        self.signal3.emit(self.data,pos,neg,neu,tol)

    #Load Pickel
    def loadData(self):
        # for reading also binary mode is important
        dbfile = open('Model', 'rb')
        db = pickle.load(dbfile)
        dbfile.close()
        return db

    #Sentiment Thai
    def Sentiment_pickel(self):
        A = self.loadData()
        pos = 0
        neg = 0
        neu = 0

        for tweet in self.df['tweet']:

            data = tweet
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

            featurized_test_sentence =  {i:(i in V )for i in A[1]}
            if A[0].classify(featurized_test_sentence) == 'pos':
                pos = pos+1
            elif A[0].classify(featurized_test_sentence) == 'neg':
                neg = neg+1
            else:
                neu = neu+1

        tol = pos + neg + neu

        self.signal3.emit(self.data,pos,neg,neu,tol)

    def geopy(self):

        geolocator = Nominatim(user_agent="sample app")
        headers = ['Address', 'Lat', 'Lon']
        file_name = str(self.data)+'_map.csv'

        for i in self.df['places']:
            try:
                if str(i) != 'nan':
                    data = geolocator.geocode(str(i))
                    data.raw.get("lat"), data.raw.get("lon")
                    data.point.latitude, data.point.longitude

                    csvfile = open(file_name, 'r', newline='', encoding='utf-8')
                    csvfile = open(file_name, 'a', newline='', encoding='utf-8')
                    writer = csv.DictWriter(csvfile, fieldnames=headers)
                    article = (i, data.point.latitude, data.point.longitude)
                    writer.writerow( {'Address':article[0], 'Lat':article[1], 'Lon':article[2]} )
                    csvfile.close()
                    print("2")

            except FileNotFoundError:
                csvfile = open(file_name, 'w', newline='', encoding='utf-8')
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                article = (i, data.point.latitude, data.point.longitude)
                writer.writerow( {'Address':article[0], 'Lat':article[1], 'Lon':article[2]} )
                csvfile.close()
                print("1")

            except AttributeError:
                print('3')
                pass
        try:
            df = pd.read_csv(str(self.data)+'_map.csv')
            fig = px.scatter_geo(df, 
                                # longitude is taken from the df["lon"] columns and latitude from df["lat"]
                                lon="Lon", 
                                lat="Lat", 
                                # choose the map chart's projection
                                projection="natural earth",
                                # columns which is in bold in the pop up
                                hover_name = "Address",
                                # format of the popup not to display these columns' data
                                hover_data = {"Address":False,
                                            "Lon": False,
                                            "Lat": False})

            # scatter_geo allow to change the map date based on the information from the df dataframe, but we can separately specify the values that are common to all
            # change the size of the markers to 25 and color to red
            fig.update_traces(marker=dict(size=25, color="red"))
            # fit the map to surround the points
            fig.update_geos(fitbounds="locations", showcountries = True)
            # add title
            fig.update_layout(title = 'Your customers')
            fig.write_image(f"C:/Users/Lenovo/Desktop/New folder/{self.data}_map.png")
            self.signal4.emit(self.data)
        except FileNotFoundError:
            pass


    def get_time(self): # Function Get time from dateEdit

        day_1,day_2 = str(self.date1.day), str(self.date2.day)
        month1,month2 = str(self.date1.month), str(self.date2.month)
        year1, year2 = str(self.date1.year), str(self.date2.year)
        #print(day_1,month1,year1)
    
        pan = pandas.read_csv(str(self.data)+'_Data.csv')
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
        self.df = pd.DataFrame({'time': between['time'],'tweet': between['tweet'],'places': between['places']})
        print(self.df)
        if re.match('[ก-๙]',self.data) != None:
            self.signal1.emit(self.data)
            self.Sentiment_pickel()
            self.signal2.emit(self.df.sort_values(by="time"))
            self.geopy()
        else:
            self.signal1.emit(self.data)
            self.Sentiment_en()
            self.signal2.emit(self.df.sort_values(by="time"))
            self.geopy()


class tweety_search(QWidget):

    switch_window = QtCore.pyqtSignal()

    def __init__(self): 
        #QApplication
        super().__init__()
        self.Creater()

    #copy text from line edit
    def getTextValue(self):
        self.pbar.setValue(10)
        data = self.inputbox.text()
        slide = self.slide.currentText()
        date1 = self.dateEdit.date().toPyDate()
        date2 = self.dateEdit1.date().toPyDate()

        self.thread = QThread()
        self.worker = API_thread(data,slide,date1,date2)
        self.progress = Progress()
    
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.check_search)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.signal1.connect(self.Link)
        self.worker.signal2.connect(self.Link2)
        self.worker.signal3.connect(self.Link3)
        self.worker.signal4.connect(self.Link4)
        self.button.setEnabled(False)

        self.thread.start()
        self.button.setEnabled(True)
        '''self.progress._signal.connect(self.signal_accept)
        self.progress._signal.connect(self.progress.quit)
        self.progress.start()'''

        self.button.setEnabled(False)

    def Back(self): #Back to Main GUI
        self.switch_window.emit()

    #creating title QMainWindow
    def Creater(self):
        self.setWindowTitle("Tweet search")
        self.resize(1780,920)
        self.move(50,50)

        #creating box QLineEdit
        self.inputbox = QLineEdit(self)
        self.inputbox.resize(300,30)
        self.inputbox.move(10,100)
        self.inputbox.setFont(QtGui.QFont("Helvetica",16))

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
        '''#creating button QPushButton
        self.button1 = QPushButton("Update Datetime",self)
        self.button1.resize(200,40)
        self.button1.move(10,250)
        self.button1.clicked.connect(self.update_time)
        self.button1.setFont(QtGui.QFont("Helvetica",14))'''
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
        self.label_3 = QLabel('Map',self)
        self.label_3.move(650,470)
        self.label_3.setFont(QtGui.QFont("Helvetica",16))
        #QLabel5
        self.label_5 = QLabel('Ranking Graph',self)
        self.label_5.move(650,15)
        self.label_5.setFont(QtGui.QFont("Helvetica",16))
        #QLabel6
        self.label_6 = QLabel('Sentiment',self)
        self.label_6.move(1300,15)
        self.label_6.setFont(QtGui.QFont("Helvetica",16))
        #QLabel6
        self.label_7 = QLabel('Since',self)
        self.label_7.move(450,10)
        self.label_7.setFont(QtGui.QFont("Helvetica",16))
        #QLabel6
        self.label_8 = QLabel('Until',self)
        self.label_8.move(450,150)
        self.label_8.setFont(QtGui.QFont("Helvetica",16))

        #ComboBox th and en
        self.slide = QComboBox(self)
        self.slide.addItem('th')
        self.slide.addItem('en')
        self.slide.move(280,150)
        self.slide.setFont(QtGui.QFont("Helvetica",16))

        #TextBrowser
        self.bro1 = QTextBrowser(self)
        self.bro1.resize(800,450)
        self.bro1.move(720,460)
        self.bro1.setFont(QtGui.QFont("Helvetica",12))
        #TextBrowser
        self.bro2 = QTextBrowser(self)
        self.bro2.resize(200,280)
        self.bro2.move(1100,50)
        self.bro2.setFont(QtGui.QFont("Helvetica",12))
        #TextBrowser
        self.bro3 = QTextBrowser(self)
        self.bro3.resize(450,400)
        self.bro3.move(650,50)
        self.bro3.setFont(QtGui.QFont("Helvetica",12))
        #TextBrower
        self.bro5 = QTextBrowser(self)
        self.bro5.resize(450,400)
        self.bro5.move(1300,50)
        self.bro5.setFont(QtGui.QFont("Helvetica",12))
        #TextBrower
        self.bro6 = QTextBrowser(self)
        self.bro6.resize(230,150)
        self.bro6.move(1520,450)
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
        self.dateEdit.move(450,50)
        self.dateEdit.setFont(QtGui.QFont("Helvetica",12))
        #DateEdit
        self.dateEdit1 = QDateEdit(self)
        self.dateEdit1.setMaximumDate(QtCore.QDate(self.Year,self.Month,self.Day))
        self.dateEdit1.setMaximumTime(QtCore.QTime(23, 59, 59))
        self.dateEdit1.setDate(QtCore.QDate(2021, 11, 2))
        self.dateEdit1.setCalendarPopup(True)
        self.dateEdit1.resize(150,50)
        self.dateEdit1.move(450,200)
        self.dateEdit1.setFont(QtGui.QFont("Helvetica",12))

        self.view = QTableView(self)
        self.view.resize(600,500)
        self.view.move(10,350)

    '''def signal_accept(self, msg): # Function Progress bar
        self.pbar.setValue(int(msg))
        if self.pbar.value() == 99:
            self.pbar.setValue(0)'''
    
    '''def signal_accept(self, msg): # Function Progress bar
        self.now += int(msg)
        bar = self.now / self.total*100
        self.pbar.setValue(bar)

        if self.pbar.value() == 99:
            self.pbar.setValue(0)'''

    def Link(self,data):
        self.read_file_10rank(data)
        self.create_piechart(data)
        self.pbar.setValue(20)

    def Link2(self,df):
        model = pandasModel(df)
        self.view.setModel(model)
        self.pbar.setValue(80)

    def Link3(self,data,pos,neg,neu,tol):
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
            self.pbar.setValue(60)
    
    def Link4(self,name):
        self.bro1.setStyleSheet(f'border-image:url(C:/Users/Lenovo/Desktop/New folder/{name}_map.png);')
        self.pbar.setValue(100)
        time.sleep(1)
        self.pbar.setValue(0)
        self.button.setEnabled(True)

    #10 Ranking word
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

    '''#update datetime
    def update_time(self):
        obj = Twitter_API(self.data,self.slide,self.date1,self.date2)
        obj.search()
        obj1 = NLP(self.data,'api')
        obj1.save_analysis(self.slide,self.data,'api')
        self.signal1.emit(self.data)
        self.get_time()'''

    #Show and Exit
    def show_exit(self):
        self.show()

class pandasModel(QAbstractTableModel): #Class for creat AbstractTableModel
    
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