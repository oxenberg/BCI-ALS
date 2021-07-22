from PyQt5 import QtWidgets
from SSVEP_UI.UI_objects import (
    Ui_OneOptionWindow, Ui_TwoOptionsWindow, Ui_ThreeOptionsWindow, Ui_FourOptionsWindow, Ui_FiveOptionsWindow,
    Ui_SixOptionsWindow, Ui_SevenOptionsWindow, Ui_EightOptionsWindow, Ui_NineOptionsWindow, OnlineWorkerThread
)
from SSVEP_UI.utils import read_json


class MainWindow(QtWidgets.QMainWindow):
    """
    The Object of the Main Window on which the SSVEP squares are displayed
    Contains attributes for appropriate  amount of squares
    """
    def __init__(self, parent=None):
        """
                :param decisionTree:  dictionary, organized according to characterization
                :param params: dictionary, several important constants
                :param ui(1-9): UI object, the squares the will be displayed
                :param content: list, the content to dispaly
                :param frame_type: , numer of squares
                :param worker: thread, communication with data collected, currently not valid
                :param choices: list, remember previous choices for output
                :param choices_counter: int, remember depth of tree (for "back" option)
                :param choice_TH: int, num of times required for a choice (increase accuracy)
                :param currentChoice: string, remember last choice to verify TH
                """
        super(MainWindow, self).__init__(parent)
        self.decisionTree = read_json('./SSVEP_UI/online_UI_example.JSON')
        self.params = read_json('params_offline.JSON')
        self.uiOne = Ui_OneOptionWindow()
        self.uiTwo = Ui_TwoOptionsWindow()
        self.uiThree = Ui_ThreeOptionsWindow()
        self.uiFour = Ui_FourOptionsWindow()
        self.uiFive = Ui_FiveOptionsWindow()
        self.uiSix = Ui_SixOptionsWindow()
        self.uiSeven = Ui_SevenOptionsWindow()
        self.uiEight = Ui_EightOptionsWindow()
        self.uiNine = Ui_NineOptionsWindow()
        self.content = self.decisionTree.keys()
        self.frame_type = self.decideFrameType()
        self.worker = OnlineWorkerThread()
        # self.worker_init()
        self.new_trial()
        self.choices = []
        self.choice_counter = 0
        self.choiceTH = 2
        self.currentChoice = ""

    """
        the following functions are setting up the layout of squares according to their amount.
        Each amount has a layout, set in self.params (according to JSON)
    """
    def startOneOptionWindow(self):
        self.uiOne.setupUi(self, self.params['1_screen_params'])
        self.show()

    def startTwoOptionsWindow(self):
        self.uiTwo.setupUi(self, self.params['2_screen_params'])
        self.show()

    def startThreeOptionsWindow(self):
        self.uiThree.setupUi(self, self.params['3_screen_params'])
        self.show()

    def startFourOptionsWindow(self):
        self.uiFour.setupUi(self, self.params['4_screen_params'])
        self.show()

    def startFiveOptionsWindow(self):
        self.uiFive.setupUi(self, self.params['5_screen_params'])
        self.show()

    def startSixOptionsWindow(self):
        self.uiSix.setupUi(self, self.params['6_screen_params'])
        self.show()

    def startSevenOptionsWindow(self):
        self.uiSeven.setupUi(self, self.params['7_screen_params'])
        self.show()

    def startEightOptionsWindow(self):
        self.uiEight.setupUi(self, self.params['8_screen_params'])
        self.show()

    def startNineOptionsWindow(self):
        self.uiNine.setupUi(self, self.params['9_screen_params'])
        self.show()

    def layout_switcher(self):
        """
            called after choice of certain square.
            decides what to display next, if a frame around choice or changing screen (if reached choiceTH)
        """
        self.choice_counter += 1
        sender = self.sender()
        button_idx = sender.index
        choice_content = sender.label
        position = self.params[self.frame_type + '_screen_params']['positions'][button_idx]
        self.decideNextWindow(choice_content, position)

    def decideNextWindow(self, choice, position):
        """
            Helper function, sets frame around choice if choiceTH not met,
            or sets up the next screen according to decisionTree if choiceTH was met
        """
        if self.choice_counter == self.choiceTH and self.currentChoice == choice:
            self.choice_counter = 0
            self.choices.append(choice)
            self.currentChoice = ''
            self.content = self.getNextLayer(choice)
            self.frame_type = self.decideFrameType()
            if int(self.frame_type) == 1:
                self.startOneOptionWindow()
            elif int(self.frame_type) == 2:
                self.startTwoOptionsWindow()
            elif int(self.frame_type) == 3:
                self.startThreeOptionsWindow()
            elif int(self.frame_type) == 4:
                self.startFourOptionsWindow()
            elif int(self.frame_type) == 5:
                self.startFiveOptionsWindow()
            elif int(self.frame_type) == 6:
                self.startSixOptionsWindow()
            elif int(self.frame_type) == 7:
                self.startSevenOptionsWindow()
            elif int(self.frame_type) == 8:
                self.startEightOptionsWindow()
            elif int(self.frame_type) == 9:
                self.startNineOptionsWindow()
            else:
                # self.worker.terminate = True
                self.close()

        elif self.currentChoice != choice:
            enlarge = [-10, -10, 20, 20]
            pos = [p + d for p, d in zip(position, enlarge)]
            self.currentChoice = choice
            self.new_trial(tuple(pos))
            self.choice_counter = 1

    def new_trial(self, frame_loc=None):
        """
            Setup the frame for new decision making
        """
        if len(self.getContent()) == 1:
            self.uiOne.setupUi(self, params=self.params['1_screen_params'], frame_loc=frame_loc)
        elif len(self.getContent()) == 2:
            self.uiTwo.setupUi(self, params=self.params['2_screen_params'], frame_loc=frame_loc)
        elif len(self.getContent()) == 3:
            self.uiThree.setupUi(self, params=self.params['3_screen_params'], frame_loc=frame_loc)
        elif len(self.getContent()) == 4:
            self.uiFour.setupUi(self, params=self.params['4_screen_params'], frame_loc=frame_loc)
        elif len(self.getContent()) == 5:
            self.uiFive.setupUi(self, params=self.params['5_screen_params'], frame_loc=frame_loc)
        elif len(self.getContent()) == 6:
            self.uiSix.setupUi(self, params=self.params['6_screen_params'], frame_loc=frame_loc)
        elif len(self.getContent()) == 7:
            self.uiSeven.setupUi(self, params=self.params['7_screen_params'], frame_loc=frame_loc)
        elif len(self.getContent()) == 8:
            self.uiEight.setupUi(self, params=self.params['8_screen_params'], frame_loc=frame_loc)
        elif len(self.getContent()) == 9:
            self.uiNine.setupUi(self, params=self.params['9_screen_params'], frame_loc=frame_loc)
        self.show()

    def getContent(self):
        """
            get the list of all choices
        """
        return list(self.content)

    def getNextLayer(self, choice):
        """
            move within decisionTree according to choice
            Uses list of choices to find the appropriate location
        """
        if choice == "Back":
            self.choices.pop()
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
        """
            Apply "click" to a square according to it's frequency
            used for complete system with data stream
        """
        freqs = list(self.params[self.frame_type + '_screen_params']["frequencies"].values())
        if self.frame_type == 1:
            self.uiOne.buttons[freqs.index(freq)].click()
        elif self.frame_type == 2:
            self.uiTwo.buttons[freqs.index(freq)].click()
        elif self.frame_type == 3:
            self.uiThree.buttons[freqs.index(freq)].click()
        elif self.frame_type == 4:
            self.uiFour.buttons[freqs.index(freq)].click()
        elif self.frame_type == 5:
            self.uiFive.buttons[freqs.index(freq)].click()
        elif self.frame_type == 6:
            self.uiSix.buttons[freqs.index(freq)].click()
        elif self.frame_type == 7:
            self.uiSeven.buttons[freqs.index(freq)].click()
        elif self.frame_type == 8:
            self.uiEight.buttons[freqs.index(freq)].click()
        elif self.frame_type == 9:
            self.uiNine.buttons[freqs.index(freq)].click()

    def worker_init(self):
        self.worker.start()
        self.worker.message_queue.connect(self.clickFreq)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    sys.exit(app.exec_())


