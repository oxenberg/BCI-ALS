from pyOpenBCI import OpenBCICyton
from _collections import deque

import numpy as np
import time
import sys

# our modules
from arduino.model import SnrModel
from inputModule import read_params
from arduino.UI import UI
from SSVEP_UI import labelToFrequency


class DataCollectorOnline:
    '''
    get all the parameters from the params_offline.JSON

    used in the offline session the collect the data from the EEG device
    loop over the samples that  came from the device in 125 Hz
    activate the offline UI
    '''

    def __init__(self):
        self.params = read_params("../params_offline.JSON")
        # important params for time calculation

        self.time_between_events_rate = self.set_time_from_json()

        self.board = OpenBCICyton(port=self.params["port"], daisy=True)
        self.start_time = time.time()
        self.counter = 0
        self.UI = UI()
        self.model = SnrModel()
        # self.pipeline = ModelPipeline()
        self.data_queue = deque(maxlen=self.params["PREDICTION_WINDOW_SIZE"])

    def run_experiment(self, sample):
        """
        here we run all exp
        :param sample: array with all channels data
        """
        data = np.array(sample.channels_data) * self.params["uVolts_per_count"]
        all_time = time.time() - self.start_time  # total time form exp beginning
        self.counter += 1  # count how many samples taken until now
        if self.counter % self.time_between_events_rate == 0 and \
                len(self.data_queue) == self.params["PREDICTION_WINDOW_SIZE"]:

            # TODO: need to fill classification
            # freqLabel = self.pipeline.predict(list(self.data_queue))
            freqLabel = self.model.predict(self.data_queue)
            # frequency = labelToFrequency(freqLabel)
            # self.ui_thread.message_queue.emit(frequency)


            self.UI.input(freqLabel)

        self.data_queue.append(data)

        if int(all_time) >= self.params["EXPERIMENT_DURATION"]:
            self.board.stop_stream()

    def start_experiment(self):
        self.board.start_stream(self.run_experiment)
        self.board.disconnect()
        self.model.save_data()

    def set_time_from_json(self):
        TIME_BETWEEN_EVENTS = self.params["TIME_BETWEEN_EVENTS"]  # in seconds
        SAMPLE_RATE = self.params["SAMPLE_RATE"]
        return SAMPLE_RATE * TIME_BETWEEN_EVENTS


