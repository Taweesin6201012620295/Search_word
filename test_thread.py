import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar
from PyQt5.QtCore import Qt
from threading import Thread 

class MyThread(Thread):

    def __init__(self, firstName):
        Thread.__init__(self)
        self.firstName = firstName

    def run(self):
        self.firstName
        print("Hello " + " from " + self.firstName)

class Example(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)
        self.pbar.setValue(50)
        
        self.setWindowTitle("QT Progressbar Example")
        self.setGeometry(32,32,280,100)
        self.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.handleTimer)
        self.timer.start(1000)

    def handleTimer(self):
        value = self.pbar.value()
        if value < 100:
            value = value + 1
            self.pbar.setValue(value)
        else:
            self.timer.stop()
            sys.exit(app.exec_())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()

    thr1 = MyThread(Example())
    thr1.start()
    thr1.join()
    thr2 = MyThread("Danny")
    thr2.start()

    sys.exit(app.exec_())