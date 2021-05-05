from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QFrame
from Online_SSVEP_UI.online_UI_objects import BlinkButton
from random import random
from Online_SSVEP_UI.utils import read_json


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
# old JSON positions"button" : {"TL": [65, 50, 270, 210], "TR": [465, 50, 270, 210], "BL": [65, 340, 270, 210],"BR": [465, 340, 270, 210]}
# to programmatically trigger click - without the mouse use the following command:
# self.pushButton.Click()


class Ui_FourOptionsWindow(object):
    def setupUi(self, MainWindow, frame_loc=None):
        MainWindow.setObjectName("SSVEP")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: rgb(224, 236, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = BlinkButton(self.centralwidget, interval=1000, label=MainWindow.getContent()[0],
                                      onClick=MainWindow.layout_switcher)
        self.pushButton.setStyleSheet(INITIAL_BUTTON_STYLE)
        self.pushButton.blink()
        self.pushButton.setGeometry(QRect(*tuple(MainWindow.params["button"]["BL"])))
        self.pushButton.setObjectName("BL")

        self.pushButton_2 = BlinkButton(self.centralwidget, interval=500, label=MainWindow.getContent()[1],
                                        onClick=MainWindow.layout_switcher)
        self.pushButton_2.setStyleSheet(INITIAL_BUTTON_STYLE)
        self.pushButton_2.blink()
        self.pushButton_2.setGeometry(QtCore.QRect(*tuple(MainWindow.params["button"]["TL"])))
        self.pushButton_2.setObjectName("TL")

        self.pushButton_3 = BlinkButton(self.centralwidget, interval=100, label=MainWindow.getContent()[2],
                                        onClick=MainWindow.layout_switcher)
        self.pushButton_3.setStyleSheet(INITIAL_BUTTON_STYLE)
        self.pushButton_3.blink()
        self.pushButton_3.setGeometry(QtCore.QRect(*tuple(MainWindow.params["button"]["TR"])))
        self.pushButton_3.setObjectName("TR")

        self.pushButton_4 = BlinkButton(self.centralwidget, interval=200, label=MainWindow.getContent()[3],
                                        onClick=MainWindow.layout_switcher)
        self.pushButton_4.setStyleSheet(INITIAL_BUTTON_STYLE)
        self.pushButton_4.blink()
        self.pushButton_4.setGeometry(QtCore.QRect(*tuple(MainWindow.params["button"]["BR"])))
        self.pushButton_4.setObjectName("BR")

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
    def setupUi(self, MainWindow, frame_loc=None):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: rgb(224, 236, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        self.pushButton = BlinkButton(self.centralwidget, interval=500, label=MainWindow.getContent()[0],
                                      onClick=MainWindow.layout_switcher)
        self.pushButton.setStyleSheet(INITIAL_BUTTON_STYLE)
        self.pushButton.blink()
        self.pushButton.setGeometry(QtCore.QRect(*tuple(MainWindow.params["button_3"]["TL"])))
        self.pushButton.setObjectName("TL")

        self.pushButton_2 = BlinkButton(self.centralwidget, interval=100, label=MainWindow.getContent()[1],
                                        onClick=MainWindow.layout_switcher)
        self.pushButton_2.setStyleSheet(INITIAL_BUTTON_STYLE)
        self.pushButton_2.blink()
        self.pushButton_2.setGeometry(QtCore.QRect(*tuple(MainWindow.params["button_3"]["TR"])))
        self.pushButton_2.setObjectName("TR")

        self.pushButton_3 = BlinkButton(self.centralwidget, interval=200, label=MainWindow.getContent()[2],
                                        onClick=MainWindow.layout_switcher)
        self.pushButton_3.setStyleSheet(INITIAL_BUTTON_STYLE)
        self.pushButton_3.blink()
        self.pushButton_3.setGeometry(QtCore.QRect(*tuple(MainWindow.params["button_3"]["BR"])))
        self.pushButton_3.setObjectName("BR")

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
    # setupUi

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SSVEP"))
        self.pushButton.setText(_translate("MainWindow", self.pushButton.label))
        self.pushButton_2.setText(_translate("MainWindow", self.pushButton_2.label))
        self.pushButton_3.setText(_translate("MainWindow", self.pushButton_3.label))
    # retranslateUi

    def raise_all_buttons(self):
        self.frame.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.pushButton_3.raise_()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.decisionTree = read_json()
        self.params = read_json('params_offline.JSON')
        self.uiFour = Ui_FourOptionsWindow()
        self.uiThree = Ui_ThreeOptionsWindow()
        self.content = self.decisionTree.keys()
        # self.layout_switcher()
        self.threeFlag = self.decideThree()
        self.new_trial()
        self.choices = []
        self.choice_counter = 0
        self.choiceTH = 2
        self.currentChoice = ""

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

    def layout_switcher(self):
        self.choice_counter += 1
        choice_content = self.sender().text()
        choice_interval = self.sender().interval
        position_name = self.params["intervals"][str(choice_interval)]
        position = self.params[f'button{self.threeFlag}'][position_name]
        enlarge = [-10, -10, 20, 20]
        self.decideNextWindow(choice_content, [a + b for a, b in zip(position, enlarge)])

    def decideNextWindow(self, choice, position):
        if self.choice_counter == self.choiceTH and self.currentChoice == choice:
            self.choice_counter = 0
            self.currentChoice = ""
            self.choices.append(choice)
            self.content = self.getNextLayer()
            if len(self.getContent()) == 4:
                self.threeFlag = ""
                self.startFourOptionsWindow()
            elif len(self.getContent()) == 3:
                self.threeFlag = "_3"
                self.startThreeOptionsWindow()
            else:
                self.close()
        elif self.currentChoice != choice:
            self.currentChoice = choice
            self.new_trial(tuple(position))
            self.choice_counter = 1

    def new_trial(self, frame_loc=None):
        if len(self.getContent()) == 3:
            self.uiThree.setupUi(self, frame_loc)
        else:
            self.uiFour.setupUi(self, frame_loc)
        self.show()

    def getContent(self):
        return list(self.content)

    def getNextLayer(self):
        nextOptions = self.decisionTree
        for l in self.choices:
            if isinstance(nextOptions, dict):
                nextOptions = nextOptions[l]
            else:
                nextOptions = []
        return nextOptions

    def decideThree(self):
        if len(self.content) == 3:
            return "_3"
        else:
            return ""

    def clickFreq(self, freq):
        intervals = list(self.params["intervals"].keys())
        frequencies = self.calcFreq(intervals)
        destination = intervals[frequencies.index(freq)]
        self.pushButton.Click()  # TODO: find the right syntax to push button with (self.interval = destination)

    def calcFreq(self, interval):
        return interval / 10000  # TODO: find the right calculation



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    sys.exit(app.exec_())


