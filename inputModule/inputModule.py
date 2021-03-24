from pyOpenBCI import OpenBCICyton
import json
import time
import numpy as np

# work library
from inputModule.utils import read_params
from UItest import UItest
from PredictionModelModule import PredictionModel




class SignalReader:

    def __init__(self):
        self.params = read_params()  # global experiment params
        self.start_time = time.time()
        self.ITER =  0  # for counting the time
        #windows for 1 prediction and for batch
        self.batch = {"X" : [], "y" : []}
        self.window_data = [] # this window have prediction data

        # modules initialization
        self.board = OpenBCICyton(port='COM3', daisy=True)
        self.UItest = UItest() # UI module

        self.board.start_expirement(self.run_expirement())

    def start_experiment(self):
        self.board.start_stream(self.run_expirement)
        self.board.disconnect()

    def run_online(self, sample):
        # read data from sensor
        data = np.array(sample.channels_data) * self.params["uVolts_per_count"]

        all_time = time.time() - self.start_time

        round_not_end = bool(self.ITER % self.params["TIME_BETWEEN_GAMES"])

        # in the first integration the round_not_end always be 0 and the else will activate
        if round_not_end:
            # need to check if window full for prediction
            if
                PredictionModel.predict(self.window_data)
                self.UItest.step()

        else:
            # restart window data, ##need to change if we want more
            self.window_data = []
            # start new game with random action
            int_action = np.random.randint(1, len(self.params["ACTIONS"])+1)
            self.UItest.new_game(int_action)


            stim.append(0)


        array_data.append(data)
        self.ITER["COUNT"] += 1


        # if we finish the experiment time drop the thread
        if int(all_time) >= self.params["EXPERIMENT_DURATION"]:
            self.board.stop_stream()
