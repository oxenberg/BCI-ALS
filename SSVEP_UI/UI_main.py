from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRect, QThread, pyqtSignal
from PyQt5.QtWidgets import QFrame
from SSVEP_UI.UI_objects import BlinkButton
from Offline.DataCollector import DataCollector
from random import random


WHITE = 'rgb(255, 255, 255)'
INITIAL_BUTTON_STYLE = "QPushButton {\n"
"  border-color: rgb(66, 69, 183);\n"
"  border-width: 5px;        \n"
"  border-style: solid;\n"
"  border-radius: 40px;\n"
"  padding:30px;\n"
"  background-color: rgb(255, 255, 255);\n"
"}\n"
""
# to programmatically trigger click - without the mouse use the following command:
# self.pushButton.Click()

class Ui_FourOptionsWindow(object):
    def setupUi(self, MainWindow, frame_loc=None):
        MainWindow.setObjectName("SSVEP")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: rgb(224, 236, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = BlinkButton(self.centralwidget, interval=1000, label='A', onClick=MainWindow.layout_switcher)
        self.pushButton.setStyleSheet(INITIAL_BUTTON_STYLE)
        self.pushButton.blink()
        self.pushButton.setGeometry(QRect(75, 350, 250, 190))
        self.pushButton.setObjectName("A")

        self.pushButton_2 = BlinkButton(self.centralwidget, interval=500, label='B', onClick=MainWindow.layout_switcher)
        self.pushButton_2.setStyleSheet(INITIAL_BUTTON_STYLE)
        self.pushButton_2.blink()
        self.pushButton_2.setGeometry(QtCore.QRect(75, 60, 250, 190))
        self.pushButton_2.setObjectName("B")

        self.pushButton_3 = BlinkButton(self.centralwidget, interval=100, label='C', onClick=MainWindow.layout_switcher)
        self.pushButton_3.setStyleSheet(INITIAL_BUTTON_STYLE)
        self.pushButton_3.blink()
        self.pushButton_3.setGeometry(QtCore.QRect(475, 60, 250, 190))
        self.pushButton_3.setObjectName("C")

        self.pushButton_4 = BlinkButton(self.centralwidget, interval=200, label='D', onClick=MainWindow.layout_switcher)
        self.pushButton_4.setStyleSheet(INITIAL_BUTTON_STYLE)
        self.pushButton_4.blink()
        self.pushButton_4.setGeometry(QtCore.QRect(475, 350, 250, 190))
        self.pushButton_4.setObjectName("D")

        if frame_loc:
            self.frame = QFrame(self.centralwidget)
            self.frame.setObjectName(u"frame")
            self.frame.setGeometry(QRect(*frame_loc))
            self.frame.setStyleSheet(u"background-color: rgb(224, 236, 255, 0);\n"
                                     "border-color: rgb(207, 255, 192);\n"
                                     "border-width: 6px;        \n"
                                     "border-style: solid;\n"
                                     "border-radius: 40px;\n"
                                     "border-color: rgb(13, 186, 1);")
            self.frame.setFrameShape(QFrame.StyledPanel)
            self.raise_all_buttons()

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SSVEP"))
        self.pushButton.setText(_translate("MainWindow", self.pushButton.label))
        self.pushButton_2.setText(_translate("MainWindow", self.pushButton_2.label))
        self.pushButton_3.setText(_translate("MainWindow", self.pushButton_3.label))
        self.pushButton_4.setText(_translate("MainWindow", self.pushButton_4.label))

    def raise_all_buttons(self):
        self.frame.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.pushButton_3.raise_()
        self.pushButton_4.raise_()

class Ui_ThreeOptionsWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet(u"background-color: rgb(255, 234, 169);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        self.pushButton = BlinkButton(self.centralwidget, interval=500, label='A', onClick=MainWindow.layout_switcher)
        self.pushButton.setObjectName(u"pushButton_2")
        self.pushButton.setGeometry(QtCore.QRect(120, 100, 131, 81))
        self.pushButton.setStyleSheet(u"background-color: rgb(170, 255, 255);")

        self.pushButton_2 = BlinkButton(self.centralwidget, interval=100, label='B', onClick=MainWindow.layout_switcher)
        self.pushButton_2.setObjectName(u"pushButton_3")
        self.pushButton_2.setGeometry(QtCore.QRect(550, 100, 131, 81))
        self.pushButton_2.setStyleSheet(u"background-color: rgb(170, 255, 255);")

        self.pushButton_3 = BlinkButton(self.centralwidget, interval=200, label='C', onClick=MainWindow.layout_switcher)
        self.pushButton_3.setObjectName(u"pushButton_4")
        self.pushButton_3.setGeometry(QtCore.QRect(340, 330, 131, 81))
        self.pushButton_3.setStyleSheet(u"background-color: rgb(170, 255, 255);")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SSVEP"))
        self.pushButton.setText(_translate("MainWindow", self.pushButton.label))
        self.pushButton_2.setText(_translate("MainWindow", self.pushButton_2.label))
        self.pushButton_3.setText(_translate("MainWindow", self.pushButton_3.label))
    # retranslateUi


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.worker_init()
        self.uiFour = Ui_FourOptionsWindow()
        self.uiThree = Ui_ThreeOptionsWindow()
        # self.layout_switcher()
        self.new_trial()

    def startThreeOptionsWindow(self):
        self.uiThree.setupUi(self)
        self.show()

    def startFourOptionsWindow(self):
        self.uiFour.setupUi(self)
        self.show()

    def old_layout_switcher(self):
        if random() >= 0.5:
            self.startFourOptionsWindow()
        else:
            self.startThreeOptionsWindow()

    def layout_switcher(self,loc):

        if not loc:
            loc = [465, 50, 270, 210]

        self.new_trial(tuple(loc))

    def new_trial(self, frame_loc=None):
        self.uiFour.setupUi(self, frame_loc)
        self.show()

    def worker_init(self):
        self.worker = WorkerThread()
        self.worker.start()
        self.worker.update_loc.connect(self.new_trial)

class WorkerThread(QThread):
    update_loc = pyqtSignal(list)
    def __init__(self):
        super().__init__()
        self.data_collector = DataCollector(self)
    def run(self):
        self.data_collector.start_expirement()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()

    sys.exit(app.exec_())
