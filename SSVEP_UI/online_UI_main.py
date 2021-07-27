from PyQt5 import QtWidgets
from SSVEP_UI.UI_objects import (
    Ui_OneOptionWindow, Ui_TwoOptionsWindow, Ui_ThreeOptionsWindow, Ui_FourOptionsWindow, Ui_FiveOptionsWindow,
    Ui_SixOptionsWindow, Ui_SevenOptionsWindow, Ui_EightOptionsWindow, Ui_NineOptionsWindow, OnlineWorkerThread
)
from SSVEP_UI.utils import read_json
from datetime import datetime

ZERO_FIVE_KEY = '0-5'
SIX_NINE_KEY = '6-9'
ONE_SEVEN_KEY = '1-7'
HALF_KEY = '.5'
NUMERICAL_KEYS = [ZERO_FIVE_KEY, SIX_NINE_KEY, ONE_SEVEN_KEY, HALF_KEY]
NUMERICAL_VALS = [str(i) for i in range(10)] + ['.5']
ZERO_FIVE_DICT = dict(zip([str(i) for i in range(6)], [str(i) for i in range(6)]))
SIX_NINE_DICT = dict(zip([str(i) for i in range(6, 10)], [str(i) for i in range(6, 10)]))
ONE_SEVEN_DICT = dict(zip([str(i) for i in range(1, 8)], [str(i) for i in range(1, 8)]))
# NUMBERS = dict(ZERO_FIVE_KEY=ZERO_FIVE_DICT, SIX_NINE_KEY=SIX_NINE_DICT)
NUMBERS = {ZERO_FIVE_KEY: ZERO_FIVE_DICT, SIX_NINE_KEY: SIX_NINE_DICT, ONE_SEVEN_KEY: ONE_SEVEN_DICT}
EXIT = 'Exit'
RESTART = 'Restart'
TERMINAL_KEYS = [EXIT, RESTART]


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
        # self.decisionTree = read_json('./SSVEP_UI/online_UI_example.JSON')
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
        # self.worker = OnlineWorkerThread()
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

    def type_is_numerical(self, choice):
        return choice in NUMERICAL_KEYS

    def is_terminal(self, choice):
        return choice in TERMINAL_KEYS

    def decideNextWindow(self, choice, position):
        """
            Helper function, sets frame around choice if choiceTH not met,
            or sets up the next screen according to decisionTree if choiceTH was met
        """

        # "0-4": "Numbers"
        # "5-9": "Numbers"
        # ".5": "Decimal"
        # "End Number": {"next step dict"}

        # print('Decide')
        # print(self.content)
        # print(self.frame_type)
        if self.choice_counter == self.choiceTH and self.currentChoice == choice:
            self.choice_counter = 0
            self.choices.append(choice)
            self.currentChoice = ''
            if self.type_is_numerical(choice) and choice != HALF_KEY:
                print('type is num')
                cat = self.choices[-1]
                self.content = NUMBERS[cat]
                self.frame_type = self.decideFrameType()
                self.choices.pop()
                print('removed the num key')
            else:
                self.content = self.getNextLayer(choice)
                self.frame_type = self.decideFrameType()

            # if self.content == -1:
            #     self.close()
            #     return
            print('------------')
            print(self.content)
            print(self.frame_type)
            # found a leaf, end of the tree, start all over
            # if int(self.frame_type) == 0 or int(self.frame_type) > 9:
            tmp = False
            # if choice == "Restart":
            # found a terminal leaf, reached to end of tree, choice is exit or restart
            if int(self.frame_type) == -1 and not self.type_is_numerical(choice):
                # self.worker.terminate = True
                print('=== in the if, found a leaf ===')
                print(self.choices)
                print(self.content)
                print(self.frame_type)
                self.export_choices()
                print('exported')

                if choice == "Exit":
                    self.close()
                    return
                # choice is restart
                self.content = self.getNextLayer(choice, found_leaf=True)
                self.frame_type = self.decideFrameType()
                print('**********')
                print(self.content)
                print(self.frame_type)
                # self.close()
                tmp = True
            if tmp:
                print("got -1 and tmp is true")
                tmp = False
            # found a leaf, could be - end of tree, back option, numbers options (0-5, 6-9, .5)


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
            # else:
                # self.worker.terminate = True
                # self.export_choices()
                # print(self.choices)
                # self.close()

        elif self.currentChoice != choice:
            enlarge = [-10, -10, 20, 20]
            pos = [p + d for p, d in zip(position, enlarge)]
            self.currentChoice = choice
            self.new_trial(tuple(pos))
            self.choice_counter = 1

    def export_choices(self):
        exported_file_name = datetime.now().isoformat(timespec='minutes').replace(':', '')
        exported_file_path = f'{exported_file_name}.txt'
        with open(exported_file_path, 'w') as f:
            for c in self.choices:
                f.write(c)
                f.write('\n')

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

    def is_choice_number(self, choice):
        return choice in NUMERICAL_VALS

    def is_choice_float(self, l):
        try:
            float(l)
            return True
        except ValueError:
            return False
        # l.isnumeric() or l == '.5'


    def getNextLayer(self, choice, found_leaf=False):
        """
            move within decisionTree according to choice
            Uses list of choices to find the appropriate location
        """
        print('nextLayer')
        print(self.choices)
        if found_leaf:
            self.choices = []
            return dict(Exit="Exit", Restart="Restart")
        # if choice == "Exit":
        #     self.close()
        #     return -1
        if choice == "Restart":
            self.choices = []
        if choice == "Back":
            # pop twice:
            # 1st to remove the 'back' choice
            # 2nd to remove the last choice
            self.choices.pop()
            self.choices.pop()
        if self.is_choice_number(choice):
            val = self.choices.pop()
            if len(self.choices) > 0 and self.choices[-1].isnumeric():
                val = self.choices.pop() + val
            self.choices.append(val)
        nextOptions = self.decisionTree
        # reached_leaf = False
        choices_in_tree = self.choices[:-1] if self.is_choice_number(choice) else self.choices
        # for l in self.choices:
        for l in choices_in_tree:
            if isinstance(nextOptions, dict):
                if self.is_choice_float(l):
                    continue
                nextOptions = nextOptions[l]
            else:
                # never reaching here
                print('====== in the else ======')
                nextOptions = []
                # nextOptions = dict(Exit="Exit", Restart="Restart")
                # reached_leaf = True
        return nextOptions

    def decideFrameType(self):
        # print('frame')
        # print(self.content)
        if not isinstance(self.content, str):
            return str(len(self.content))
        return str(-1)

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
    # with open('SSVEP')
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    sys.exit(app.exec_())


