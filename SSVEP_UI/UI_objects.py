from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QFrame
from Offline.OfflineDataCollector import OfflineDataCollector
from Model_Pipline.Data_Collector import DataCollectorOnline

INITIAL_BUTTON_STYLE = "QPushButton {\n"
"  border-color: rgb(66, 69, 183);\n"
"  border-width: 5px;        \n"
"  border-style: solid;\n"
"  border-radius: 40px;\n"
"  padding:30px;\n"
"  background-color: rgb(255, 255, 255);\n"
"}\n"
""


class BlinkButton(QPushButton):
    def __init__(self, parent, index, frequency, label, onClick):
        QPushButton.__init__(self, parent)

        self.visible = True
        self.label = label
        self.frequency = frequency
        self.index = index

        interval = self.calcInterval(frequency)
        timer = QTimer(parent=parent)
        timer.setInterval(interval)
        timer.timeout.connect(self.blink)
        timer.start()

        self.clicked.connect(onClick)

    def blink(self):
        if self.visible:
            self.setStyleSheet("QPushButton {\n"
                               "  border-color: rgb(66, 69, 183);\n"
                               "  border-width: 5px;        \n"
                               "  border-style: solid;\n"
                               "  border-radius: 40px;\n"
                               "  padding:30px;\n"
                               "  background-color: rgb(255, 193, 185);\n"
                               "}\n"
                               "")
        else:
            self.setStyleSheet("QPushButton {\n"
                               "  border-color: rgb(66, 69, 183);\n"
                               "  border-width: 5px;        \n"
                               "  border-style: solid;\n"
                               "  border-radius: 40px;\n"
                               "  padding:30px;\n"
                               "  background-color: rgb(255, 255, 255);\n"
                               "}\n"
                               "")
        self.visible = not self.visible

    def calcInterval(self, freq):
        return 500 / freq


class Ui_TwoOptionsWindow(object):
    def setupUi(self, MainWindow, params, frame_loc=None):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: rgb(224, 236, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        self.buttons = []
        for i in range(2):
            pb = BlinkButton(self.centralwidget, index=i, frequency=params['frequencies'][i],
                             label=MainWindow.getContent()[i], onClick=MainWindow.layout_switcher)
            pb.setStyleSheet(INITIAL_BUTTON_STYLE)
            pb.blink()
            pb.setGeometry(QtCore.QRect(*tuple(params["positions"][i])))
            pb.setFont(QFont('Times', 20))
            pb.setObjectName(str(i))
            self.buttons.append(pb)

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
        for pb in self.buttons:
            pb.setText(_translate("MainWindow", pb.label))
    # retranslateUi

    def raise_all_buttons(self):
        self.frame.raise_()
        for pb in self.buttons:
            pb.raise_()


class Ui_ThreeOptionsWindow(object):
    def setupUi(self, MainWindow, params, frame_loc=None):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: rgb(224, 236, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        self.buttons = []
        for i in range(3):
            pb = BlinkButton(self.centralwidget, index=i, frequency=params['frequencies'][i], label=MainWindow.getContent()[i],
                                      onClick=MainWindow.layout_switcher)
            pb.setStyleSheet(INITIAL_BUTTON_STYLE)
            pb.blink()
            pb.setGeometry(QtCore.QRect(*tuple(params["positions"][i])))
            pb.setFont(QFont('Times', 20))
            pb.setObjectName(str(i))
            self.buttons.append(pb)

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
        for pb in self.buttons:
            pb.setText(_translate("MainWindow", pb.label))
    # retranslateUi

    def raise_all_buttons(self):
        self.frame.raise_()
        for pb in self.buttons:
            pb.raise_()


class Ui_FourOptionsWindow(object):
    def setupUi(self, MainWindow, params, frame_loc=None):
        MainWindow.setObjectName("SSVEP")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: rgb(224, 236, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.buttons = []
        for i in range(4):
            pb = BlinkButton(self.centralwidget, index=i, frequency=params['frequencies'][i], label=MainWindow.getContent()[i],
                                      onClick=MainWindow.layout_switcher)
            pb.setStyleSheet(INITIAL_BUTTON_STYLE)
            pb.blink()
            pb.setGeometry(QtCore.QRect(*tuple(params["positions"][i])))
            pb.setFont(QFont('Times', 20))
            pb.setObjectName(str(i))
            self.buttons.append(pb)

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
        for pb in self.buttons:
            pb.setText(_translate("MainWindow", pb.label))

    def raise_all_buttons(self):
        self.frame.raise_()
        for pb in self.buttons:
            pb.raise_()


class Ui_FiveOptionsWindow(object):
    def setupUi(self, MainWindow, params, frame_loc=None):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: rgb(224, 236, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        self.buttons = []
        for i in range(5):
            pb = BlinkButton(self.centralwidget, index=i, frequency=params['frequencies'][i], label=MainWindow.getContent()[i],
                                      onClick=MainWindow.layout_switcher)
            pb.setStyleSheet(INITIAL_BUTTON_STYLE)
            pb.blink()
            pb.setGeometry(QtCore.QRect(*tuple(params["positions"][i])))
            pb.setFont(QFont('Times', 20))
            pb.setObjectName(str(i))
            self.buttons.append(pb)

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
        for pb in self.buttons:
            pb.setText(_translate("MainWindow", pb.label))
    # retranslateUi

    def raise_all_buttons(self):
        self.frame.raise_()
        for pb in self.buttons:
            pb.raise_()


class Ui_SixOptionsWindow(object):
    def setupUi(self, MainWindow, params, frame_loc=None):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: rgb(224, 236, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        self.buttons = []
        for i in range(6):
            pb = BlinkButton(self.centralwidget, index=i, frequency=params['frequencies'][i], label=MainWindow.getContent()[i],
                                      onClick=MainWindow.layout_switcher)
            pb.setStyleSheet(INITIAL_BUTTON_STYLE)
            pb.blink()
            pb.setGeometry(QtCore.QRect(*tuple(params["positions"][i])))
            pb.setFont(QFont('Times', 20))
            pb.setObjectName(str(i))
            self.buttons.append(pb)

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
        for pb in self.buttons:
            pb.setText(_translate("MainWindow", pb.label))
    # retranslateUi

    def raise_all_buttons(self):
        self.frame.raise_()
        for pb in self.buttons:
            pb.raise_()


class Ui_SevenOptionsWindow(object):
    def setupUi(self, MainWindow, params, frame_loc=None):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: rgb(224, 236, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        self.buttons = []
        for i in range(7):
            pb = BlinkButton(self.centralwidget, index=i, frequency=params['frequencies'][i], label=MainWindow.getContent()[i],
                                      onClick=MainWindow.layout_switcher)
            pb.setStyleSheet(INITIAL_BUTTON_STYLE)
            pb.blink()
            pb.setGeometry(QtCore.QRect(*tuple(params["positions"][i])))
            pb.setFont(QFont('Times', 20))
            pb.setObjectName(str(i))
            self.buttons.append(pb)

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
        for pb in self.buttons:
            pb.setText(_translate("MainWindow", pb.label))
    # retranslateUi

    def raise_all_buttons(self):
        self.frame.raise_()
        for pb in self.buttons:
            pb.raise_()


class Ui_EightOptionsWindow(object):
    def setupUi(self, MainWindow, params, frame_loc=None):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: rgb(224, 236, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        self.buttons = []
        for i in range(8):
            pb = BlinkButton(self.centralwidget, index=i, frequency=params['frequencies'][i], label=MainWindow.getContent()[i],
                                      onClick=MainWindow.layout_switcher)
            pb.setStyleSheet(INITIAL_BUTTON_STYLE)
            pb.blink()
            pb.setGeometry(QtCore.QRect(*tuple(params["positions"][i])))
            pb.setFont(QFont('Times', 20))
            pb.setObjectName(str(i))
            self.buttons.append(pb)

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
        for pb in self.buttons:
            pb.setText(_translate("MainWindow", pb.label))
    # retranslateUi

    def raise_all_buttons(self):
        self.frame.raise_()
        for pb in self.buttons:
            pb.raise_()


class Ui_NineOptionsWindow(object):
    def setupUi(self, MainWindow, params, frame_loc=None,show_content = True):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: rgb(224, 236, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.buttons_size = 9
        if show_content:
            self.content = MainWindow.getContent()
        else:
            self.content = [""] * self.buttons_size

        self.buttons = []
        for i in range(self.buttons_size):
            pb = BlinkButton(self.centralwidget, index=i, frequency=params['frequencies'][i], label=self.content[i],
                                      onClick=MainWindow.layout_switcher)
            pb.setStyleSheet(INITIAL_BUTTON_STYLE)
            pb.blink()
            pb.setGeometry(QtCore.QRect(*tuple(params["positions"][i])))
            pb.setFont(QFont('Times', 20))
            pb.setObjectName(str(i))
            self.buttons.append(pb)

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
        for pb in self.buttons:
            pb.setText(_translate("MainWindow", pb.label))
    # retranslateUi

    def raise_all_buttons(self):
        for pb in self.buttons:
            pb.raise_()
        self.frame.raise_()


class OfflineWorkerThread(QThread):
    update_loc = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.data_collector = OfflineDataCollector(self)

    def run(self):
        self.data_collector.start_expirement()


class OnlineWorkerThread(QThread):
    message_queue = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.terminate = False
        self.data_collector = DataCollectorOnline(self)

    def run(self):
        self.data_collector.start_experiment()


if __name__ == "__main__":
    app = QApplication([])
    app.exec_()
