from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtCore import QTimer
import random


class BlinkButton(QPushButton):
    def __init__(self, parent, interval, label, onClick):
        QPushButton.__init__(self, parent)

        self.visible = True
        self.colorA = 'rgb(255, 193, 185)'
        self.colorB = 'rgb(255, 255, 255)'
        self.label = label
        timer = QTimer(parent=parent)
        timer.setInterval(interval)
        timer.timeout.connect(self.blink)
        timer.start()

        self.clicked.connect(onClick)

    def Tblink(self):
        if self.visible:
            self.setStyleSheet('background-color: ' + self.colorA)
        else:
            self.setStyleSheet('background-color: ' + self.colorB)
        self.visible = not self.visible

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


if __name__ == "__main__":
    app = QApplication([])
    app.exec_()