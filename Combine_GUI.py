import sys
from PyQt5.QtWidgets import *
from PyQt5.QtChart import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5 import *

from datetime import datetime, date

from Gui_API import *
from GUI_Crawler import *
from GUI_Finance import *

class Login(QWidget):

    switch_window = QtCore.pyqtSignal()
    switch_window1 = QtCore.pyqtSignal()
    switch_window2 = QtCore.pyqtSignal()

    def __init__(self): 
        #QApplication
        super().__init__()
        self.Creater()
    
    def Creater(self):
        self.setWindowTitle('Search word')
        self.resize(800,400)

        #QLabel1
        self.label_1 = QLabel('Welcome to word search',self)
        self.label_1.move(220, 30)
        self.label_1.setFont(QtGui.QFont("Helvetica",20))
        #QLabel2
        self.label_2 = QLabel('Please choose the type you want',self)
        self.label_2.move(200,100)
        self.label_2.setFont(QtGui.QFont("Helvetica",16))

        self.button = QPushButton('Twitter',self)
        self.button.clicked.connect(self.login)
        self.button.resize(200,60)
        self.button.move(150,180)
        self.button.setFont(QtGui.QFont("Helvetica",20))

        self.button2 = QPushButton('Crawler',self)
        self.button2.clicked.connect(self.login1)
        self.button2.resize(200,60)
        self.button2.move(450,180)
        self.button2.setFont(QtGui.QFont("Helvetica",20))

        self.button3 = QPushButton('Stock',self)
        self.button3.clicked.connect(self.login2)
        self.button3.resize(200,60)
        self.button3.move(150,300)
        self.button3.setFont(QtGui.QFont("Helvetica",20))

        self.button4 = QPushButton('Clear',self)
        self.button4.clicked.connect(self.Clear)
        self.button4.resize(100,50)
        self.button4.move(680,330)
        self.button4.setFont(QtGui.QFont("Helvetica",20))

        #set icon window
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap("../../Downloads/ms-word.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(self.icon)

    def login(self):
        self.switch_window.emit()

    def login1(self):
        self.switch_window1.emit()

    def login2(self):
        self.switch_window2.emit()

    def Clear(self):
        file_API = 'file_list_API.csv'
        headers = ["update_time",'file_name']
        csvfile = open(file_API, 'w', newline='')
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()

        file_Crawler = 'file_list_Crawler.csv'
        headers = ["update_time",'file_name']
        csvfile = open(file_Crawler, 'w', newline='')
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()


class Controller:

    def __init__(self):
        pass

    def show_window_one(self):
        self.one = Login()
        self.one.switch_window.connect(self.show_main)
        self.one.switch_window1.connect(self.show_window_two)
        self.one.switch_window2.connect(self.show_window_three)
        self.one.show()

    def show_main(self):
        self.window = tweety_search()
        self.window.switch_window.connect(self.close)
        self.one.close()
        self.window.show()

    def show_window_two(self):
        self.window_two = Crawler_search()
        self.window_two.switch_window1.connect(self.close1)
        self.one.close()
        self.window_two.show()
    
    def show_window_three(self):
        self.window_three = search_finance()
        self.window_three.switch_window2.connect(self.close2)
        self.one.close()
        self.window_three.show()

    def close(self):
        self.window.close()
        self.show_window_one()

    def close1(self):
        self.window_two.close()
        self.show_window_one()
    
    def close2(self):
        self.window_three.close()
        self.show_window_one()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = Controller()
    controller.show_window_one()
    sys.exit(app.exec_())