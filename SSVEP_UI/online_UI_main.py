from PyQt5 import QtWidgets
from UI_objects import Ui_ThreeOptionsWindow, Ui_FourOptionsWindow
from SSVEP_UI.utils import read_json


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.decisionTree = read_json()
        self.params = read_json('params_offline.JSON')
        self.uiFour = Ui_FourOptionsWindow()
        self.uiThree = Ui_ThreeOptionsWindow()
        self.content = self.decisionTree.keys()
        self.frame_type = self.decideFrameType()
        self.new_trial()
        self.choices = []
        self.choice_counter = 0
        self.choiceTH = 2
        self.currentChoice = ""

    def startThreeOptionsWindow(self):
        self.uiThree.setupUi(self, self.params['3_screen_params'])
        self.show()

    def startFourOptionsWindow(self):
        self.uiFour.setupUi(self, self.params['4_screen_params'])
        self.show()

    def layout_switcher(self):
        self.choice_counter += 1
        sender = self.sender()
        button_idx = sender.index
        choice_content = sender.label
        position = self.params[self.frame_type + '_screen_params']['positions'][button_idx]

        self.decideNextWindow(choice_content, position)

    def decideNextWindow(self, choice, position):
        if self.choice_counter == self.choiceTH and self.currentChoice == choice:
            self.choice_counter = 0
            self.choices.append(choice)
            self.currentChoice = ''
            self.content = self.getNextLayer()
            self.frame_type = self.decideFrameType()
            if int(self.frame_type) == 4:
                self.startFourOptionsWindow()
            elif int(self.frame_type) == 3:
                self.startThreeOptionsWindow()
            else:
                self.close()
        elif self.currentChoice != choice:
            enlarge = [-10, -10, 20, 20]
            pos = [p + d for p, d in zip(position, enlarge)]
            self.currentChoice = choice
            self.new_trial(tuple(pos))
            self.choice_counter = 1

    def new_trial(self, frame_loc=None):
        if len(self.getContent()) == 3:
            self.uiThree.setupUi(self, params=self.params['3_screen_params'], frame_loc=frame_loc)
        else:
            self.uiFour.setupUi(self, params=self.params['4_screen_params'], frame_loc=frame_loc)
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

    def decideFrameType(self):
        return str(len(self.content))

    def getOutput(self):
        return self.choices

    def clickFreq(self, freq):
        freqs = list(self.params[self.frame_type + '_screen_params']["frequencies"].values())
        if self.frame_type == 3:
            self.uiThree.buttons[freqs.index(freq)].click()
        elif self.frame_type == 4:
            self.uiFour.buttons[freqs.index(freq)].click()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    sys.exit(app.exec_())


