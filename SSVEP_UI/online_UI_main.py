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
COMMASPACE = ', '

import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders

from fpdf import FPDF

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
                path = self.export_choices()
                print('exported')
                self.convert_to_pdf_and_email(path)
                print('converted to pdf')
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
        parsed_choices = self.parse_choices(self.choices)

        exported_file_name = datetime.now().isoformat(timespec='minutes').replace(':', '')
        exported_file_path = f'{exported_file_name}.txt'
        with open(exported_file_path, 'w', encoding="utf-8") as f:
            for c in parsed_choices:
                f.write(c)
                f.write('\n')
        return exported_file_path



    def convert_to_pdf(self, path):
        # save FPDF() class into
        # a variable pdf
        pdf = FPDF()
        # Add a page
        pdf.add_page()
        # set style and size of font
        # that you want in the pdf
        pdf.set_font("Arial", style="BU", size=11)
        # open the text file in read mode
        f = open(path, "r")
        # insert the texts in pdf
        line = 0
        for x in f:
            if line == 1:
                pdf.set_font(family="Arial", style="", size=11)
            if line == 3:
                pdf.set_font(family="Arial", style="B", size=11)
            pdf.cell(200, 8, txt=x, ln=1, align='L')
            line = line + 1

        # save the pdf with name .pdf
        pdf_path = path.replace('.txt', '.pdf')
        pdf.output(pdf_path)
        f.close()
        return pdf_path

    # def send_email(self, path):
    #     send_from = 'afouri92@gmail.com'
    #     send_to = ['afouri@post.bgu.ac.il']
    #     server = "localhost"
    #     port = 587
    #
    #     msg = MIMEMultipart()
    #
    #     msg['From'] = send_from
    #     msg['To'] = COMMASPACE.join(send_to)
    #     msg['Date'] = formatdate(localtime=True)
    #     msg['Subject'] = 'test mail'
    #
    #     msg.attach(MIMEText('test mail text'))
    #
    #     with open(path, "rb") as fil:
    #         part = MIMEApplication(
    #             fil.read(),
    #             Name=basename(path)
    #         )
    #     # After the file is closed
    #     part['Content-Disposition'] = 'attachment; filename="%s"' % basename(path)
    #     msg.attach(part)
    #
    #     smtp = smtplib.SMTP(server)
    #     smtp.sendmail(send_from, send_to, msg.as_string())
    #     smtp.close()

    def convert_to_pdf_and_email(self, path):
        pdf_path = self.convert_to_pdf(path)
        # self.send_email(pdf_path)

    def parse_choices(self, choices):
        parsed = []

        location = choices[2].split()[-1]
        if location == "Left":
            location = "LT"
        else:
            location = "RT"
        parsed.append("ME-"+choices[1]+": Prostate, " + location + " " + choices[3] + ", biopsy")
        is_benign = choices[4] == "Benign"
        gleason = ","  # only relevant if score is 7
        pattern = ""  # only relevant if score is 7
        if is_benign:
            parsed.append("Benign prostatic tissue.")
        else:
            carcinoma = choices[5].split()
            gleason_score = int(choices[7]) + int(choices[9])
            if gleason_score < 7:
                grade_group = "1"
            elif gleason_score < 8:
                if choices[7] < choices[9]:  # 3 + 4
                    grade_group = "2"
                    gleason = "(3 + 4), "
                else:  # 4 + 3
                    grade_group = "3"
                    gleason = " (4 + 3), "
                pattern = choices[12] + "% " + choices[11] + ", "
            elif gleason_score < 9:
                grade_group = "4"
            else:
                grade_group = "5"

            parsed.append(carcinoma[0] + " " + carcinoma[-1] + ", " + "Gleason Score " + gleason + pattern + "grade group-" + grade_group + ".")
            if gleason_score == 7:
                tissue_cores = choices[14]
                tumor_cores = choices[16]
                tissue_length = float(choices[18])
                tumor_length = float(choices[20])
            else:
                tissue_cores = choices[12]
                tumor_cores = choices[14]
                tissue_length = float(choices[16])
                tumor_length = float(choices[18])

            parsed.append("Tumor involves " + tumor_cores + " of " + tissue_cores + " tissue cores and approx. " + str(round(tumor_length/tissue_length*100)) +
                          "% of submitted tissue length (" + str(round(tumor_length, 1)) + " of " + str(round(tissue_length, 1)) + " mm).")

        parsed.append("May Michael Scott L.N. 153418")
        return parsed

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


