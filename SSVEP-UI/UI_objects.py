from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtCore import QTimer

class BlinkButton(QPushButton):
    def __init__(self, parent, interval, label, onClick):
        QPushButton.__init__(self, parent)

        self.visible = True
        self.colorA = 'rgb(170, 255, 255)'
        self.colorB = 'rgb(255, 255, 255)'
        self.label = label

        timer = QTimer(parent=parent)
        timer.setInterval(interval)
        timer.timeout.connect(self.blink)
        timer.start()

        self.clicked.connect(onClick)

    def blink(self):
        if self.visible:
            self.setStyleSheet('background-color: ' + self.colorA)
        else:
            self.setStyleSheet('background-color: ' + self.colorB)

        self.visible = not self.visible

    def onClick(self):
        return random.random() >= 0.5


if __name__ == "__main__":
    app = QApplication([])
    app.exec_()