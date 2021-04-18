import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QProgressBar, QVBoxLayout, QApplication

class Progress(QThread):
    _signal = pyqtSignal(int)
    def __init__(self):
        super(Progress, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        for i in range(100):
            time.sleep(0.1)
            self._signal.emit(i)

class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.setWindowTitle('QProgressBar')
        self.btn = QPushButton('Click me')
        self.btn.clicked.connect(self.btnFunc)
        self.pbar = QProgressBar(self)
        self.pbar.setValue(0)
        self.resize(300, 100)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.pbar)
        self.vbox.addWidget(self.btn)
        self.setLayout(self.vbox)
        self.show()

    def btnFunc(self):
        self.thread = Progress()
        self.thread._signal.connect(self.signal_accept)
        self.thread.start()
        self.btn.setEnabled(False)

    def signal_accept(self, msg):
        self.pbar.setValue(int(msg))
        if self.pbar.value() == 99:
            self.pbar.setValue(0)
            self.btn.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

'''
import sys
import time

from PySide2 import QtCore
from PySide2.QtCore import Qt
import PySide2.QtWidgets as QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    """Main window, with one button for exporting stuff"""

    def __init__(self, parent=None):
        super().__init__(parent)
        central_widget = QtWidgets.QWidget(self)
        layout = QtWidgets.QHBoxLayout(self)
        button = QtWidgets.QPushButton("Press me...")
        button.clicked.connect(self.export_stuff)
        layout.addWidget(button)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def export_stuff(self):
        """Opens dialog and starts exporting"""
        some_window = MyExportDialog(self)
        some_window.exec_()


class MyAbstractExportThread(QtCore.QThread):
    """Base export thread"""
    change_value = QtCore.Signal(int)

    def run(self):
        cnt = 0
        while cnt < 100:
            cnt += 1
            self.operation()
            self.change_value.emit(cnt)

    def operation(self):
        pass


class MyExpensiveExportThread(MyAbstractExportThread):

    def operation(self):
        """Something that takes a lot of CPU power"""
        some_val = 0
        for i in range(1000000):
            some_val += 1


class MyInexpensiveExportThread(MyAbstractExportThread):

    def operation(self):
        """Something that doesn't take a lot of CPU power"""
        time.sleep(.1)


class MyExportDialog(QtWidgets.QDialog):
    """Dialog which does some stuff, and shows its progress"""

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowCloseButtonHint)
        self.setWindowTitle("Exporting...")
        layout = QtWidgets.QHBoxLayout()
        self.progress_bar = self._create_progress_bar()
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)
        self.worker = MyInexpensiveExportThread()  # Works fine
        # self.worker = MyExpensiveExportThread()  # Super laggy
        self.worker.change_value.connect(self.progress_bar.setValue)
        self.worker.start()
        self.worker.finished.connect(self.close)

    def _create_progress_bar(self):
        progress_bar = QtWidgets.QProgressBar(self)
        progress_bar.setMinimum(0)
        progress_bar.setMaximum(100)
        return progress_bar


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())'''