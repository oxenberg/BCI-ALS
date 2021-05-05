import matplotlib.pyplot as plt
from mne.stats import bootstrap_confidence_interval
from mne.baseline import rescale

from pyOpenBCI import OpenBCICyton
from PyQt5 import QtCore, QtGui, QtWidgets

import numpy as np
import mne
import random
import time
import sys

# our modules
from inputModule import read_params


class DataCollector:
    '''
    get all the parameters from the params_offline.JSON

    used in the offline session the collect the data from the EEG device
    loop over the samples that  came from the device in 125 Hz
    activate the offline UI
    '''

    def __init__(self,UI):
        self.params_offline = read_params("params_offline.JSON")
        # important params for calculate time

        self.time_between_events_rate = self.set_time_from_json()

        self.board = OpenBCICyton(port=self.params_offline["port"], daisy=True)
        self.start_time = time.time()
        self.counter = 0
        self.UI = UI
        self.button_options = list(self.params_offline["button"].values())

        self.all_eeg_data = []

    def run_expirement(self, sample):
        """
        here we run all exp
        :param sample: array with all channels data
        """
        data = np.array(sample.channels_data) * self.params_offline["uVolts_per_count"]
        all_time = time.time() - self.start_time  # total time form exp beginning
        self.counter += 1  # count how many samples take until now
        if self.counter % self.time_between_events_rate == 0:
            button_index = random.randint(1, self.params_offline["MAX_SSVEP_OPTIONS"])
            choosen_button_loc = self.button_options[button_index-1]
            # self.UI.layout_switcher(choosen_button_loc)
            self.UI.update_loc.emit(choosen_button_loc)

        self.all_eeg_data.append(data)

        if int(all_time) >= self.params_offline["EXPERIMENT_DURATION"]:
            self.board.stop_stream()

    def start_expirement(self):
        self.board.start_stream(self.run_expirement)

    def end_expirment(self):
        self.board.disconnect()
        sys.exit(self.app.exec_())

    # def init_UI(self):
    #     app = QtWidgets.QApplication(sys.argv)
    #     main_window = MainWindow()
    #     app.exec_()
    #     return main_window, app

    def set_time_from_json(self):
        TIME_BETWEEN_EVENTS = self.params_offline["TIME_BETWEEN_EVENTS"]  # in seconds
        SAMPLE_RATE = self.params_offline["SAMPLE_RATE"]
        return SAMPLE_RATE * TIME_BETWEEN_EVENTS


if __name__ == "__main__":
    data_collector = DataCollector()
    data_collector.start_expirement()
