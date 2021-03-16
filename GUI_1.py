# refference https://www.youtube.com/watch?v=a9Mynu6pC4U&t=36s&ab_channel=ParwizForogh
from PyQt5.QtWidgets import*
import sys
from PyQt5.QtChart import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import pandas

class window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pan = pandas.read_csv('tweet_NLP_2.csv')
        self.setWindowTitle("PyQt PieChart")
        self.setGeometry(0,0,600,500)
        self.create_piechart()
        self.show()

    def create_piechart(self):
        se = QPieSeries()
        for i,j in zip(self.pan['word'],self.pan['number']):
            se.append(i,int(j))
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
        self.savepi.save("C:/Users/Lenovo/Desktop/New folder/a.png", "PNG")

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window1 = window()
    sys.exit(App.exec_())