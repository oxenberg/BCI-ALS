from PyQt5 import QtWidgets
from UI_objects import Ui_ThreeOptionsWindow, Ui_FourOptionsWindow, OfflineWorkerThread


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.worker_init()
        self.uiFour = Ui_FourOptionsWindow()
        self.uiThree = Ui_ThreeOptionsWindow()
        self.new_trial()

    def startThreeOptionsWindow(self):
        self.uiThree.setupUi(self, self.params['3_screen_params'])
        self.show()

    def startFourOptionsWindow(self):
        self.uiFour.setupUi(self, self.params['4_screen_params'])
        self.show()

    def layout_switcher(self, loc):
        if not loc:
            loc = [465, 50, 270, 210]

        self.new_trial(tuple(loc))

    def new_trial(self, frame_loc=None):
        self.uiFour.setupUi(self, self.params['4_screen_params'], frame_loc)
        self.show()

    def worker_init(self):
        self.worker = OfflineWorkerThread()
        self.worker.start()
        self.worker.update_loc.connect(self.new_trial)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()

    sys.exit(app.exec_())