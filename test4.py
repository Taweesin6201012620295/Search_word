import sys
from PyQt5.QtWidgets import *
from PyQt5.QtChart import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5 import *

class dumpThread(QThread):
    
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def sendEstablismentCommands(self, connection):

        # Commands are sending sequently with proper delay-timers #

        connection.sendShell("telnet localhost 21000")
        time.sleep(0.5)
        connection.sendShell("admin")
        time.sleep(0.5)
        connection.sendShell("admin")
        time.sleep(0.5)
        connection.sendShell("cd imdb")
        time.sleep(0.5)
        connection.sendShell("dump subscriber")

        command = input('$ ')

    def run(self):
        # your logic here              
        # self.emit(QtCore.SIGNAL('THREAD_VALUE'), maxVal)
        self.sendEstablismentCommands(connection)    

class progressThread(QThread):
    
    progress_update = pyqtSignal(int) # or pyqtSignal(int)

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()


    def run(self):
        # your logic here
        while 1:      
            maxVal = 100
            self.progress_update.emit(maxVal) # self.emit(SIGNAL('PROGRESS'), maxVal)
            # Tell the thread to sleep for 1 second and let other things run
            time.sleep(1)

class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.connectButton.clicked.connect(self.connectToSESM)



    def connectToSESM(self):
        ## Function called when pressing connect button, input are being taken from edit boxes. ##
        ## dumpThread() method has been designed for working thread seperate from GUI. ##

        # Connection data are taken from "Edit Boxes"
        # username has been set as hardcoded

        ### Values Should Be Defined As Global ###
        username = "ntappadm"
        password = self.ui.passwordEdit.text()
        ipAddress = self.ui.ipEdit.text()

        # Connection has been established through paramiko shell library
        global connection

        connection = pr.ssh(ipAddress, username, password)
        connection.openShell()
        pyqtRemoveInputHook()  # For remove unnecessary items from console

        global get_thread

        get_thread = dumpThread() # Run thread - Dump Subscriber
        self.progress_thread = progressThread()

        self.progress_thread.start()
        self.connect(self.progress_thread, SIGNAL('PROGRESS'), self.updateProgressBar)

        get_thread.start()     




    def updateProgressBar(self, maxVal):

        for i in range(maxVal):
            self.ui.progressBar.setValue(self.ui.progressBar.value() + 1)
            time.sleep(1)
            maxVal = maxVal - 1

            if maxVal == 0:
                self.ui.progressBar.setValue(100)

    def parseSubscriberList(self):
        parsing = reParser()

    def done(self):
        QtGui.QMessageBox.information(self, "Done!", "Done fetching posts!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())