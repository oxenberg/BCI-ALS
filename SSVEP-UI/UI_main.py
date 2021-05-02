from PyQt5 import QtCore, QtGui, QtWidgets
from UI_objects import BlinkButton
from random import random


# to programmatically trigger click - without the mouse use the following command:
# self.pushButton.Click()

class Ui_FourOptionsWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("SSVEP")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: rgb(255, 234, 169);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = BlinkButton(self.centralwidget, interval=1000, label='A', onClick=MainWindow.layout_switcher)
        self.pushButton.setGeometry(QtCore.QRect(150, 270, 131, 81))
        self.pushButton.setStyleSheet("background-color: rgb(170, 255, 255);")
        self.pushButton.setObjectName("A")

        self.pushButton_2 = BlinkButton(self.centralwidget, interval=500, label='B', onClick=MainWindow.layout_switcher)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 100, 131, 81))
        self.pushButton_2.setStyleSheet("background-color: rgb(170, 255, 255);")
        self.pushButton_2.setObjectName("B")

        self.pushButton_3 = BlinkButton(self.centralwidget, interval=100, label='C', onClick=MainWindow.layout_switcher)
        self.pushButton_3.setGeometry(QtCore.QRect(520, 100, 131, 81))
        self.pushButton_3.setStyleSheet("background-color: rgb(170, 255, 255);")
        self.pushButton_3.setObjectName("C")

        self.pushButton_4 = BlinkButton(self.centralwidget, interval=200, label='D', onClick=MainWindow.layout_switcher)
        self.pushButton_4.setGeometry(QtCore.QRect(520, 270, 131, 81))
        self.pushButton_4.setStyleSheet("background-color: rgb(170, 255, 255);")
        self.pushButton_4.setObjectName("D")
        self.pushButton_4.setText("D")

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
        self.uiFour = Ui_FourOptionsWindow()
        self.uiThree = Ui_ThreeOptionsWindow()
        self.layout_switcher()

    def startThreeOptionsWindow(self):
        self.uiThree.setupUi(self)
        self.show()

    def startFourOptionsWindow(self):
        self.uiFour.setupUi(self)
        self.show()

    def layout_switcher(self):
        if random() >= 0.5:
            self.startFourOptionsWindow()
        else:
            self.startThreeOptionsWindow()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()

    sys.exit(app.exec_())