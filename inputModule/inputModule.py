from pyOpenBCI import OpenBCICyton
import json
import time
import numpy as np

#work library
from UItest import UItest

class signalReader:

    def __init__(self):
        self.params = self.read_params()  # global experiment params
        self.start_time = time.time()
        self.ITER = {"COUNT": 0}  # for counting the time

        self.board = OpenBCICyton(port='COM3', daisy=True)
        self.UItest = UItest() # UI module

        self.board.start_expirement(self.run_expirement())

    def read_params(self):
        params_file = open('../params.JSON', )
        params = json.load(params_file)

        # fill more params with explanation
        uVolts_per_count = (4500000) / 24 / (2 ** 23 - 1)  # uV/count
        params["uVolts_per_count"] = uVolts_per_count
        return params

    def start_experiment(self):
        self.board.start_stream(self.run_expirement)
        self.board.disconnect()

    def run_experiment(self, sample):
        data = np.array(sample.channels_data) * self.params["uVolts_per_count"]

        all_time = time.time() - self.start_time

        self.ITER["COUNT"] += 1
        if (self.ITER["COUNT"] % self.params["TIME_BETWEEN_GAMES"]) == 0:
            # start new game with random action
            int_action = np.random.randint(1, len(self.params["ACTIONS"])+1)
            self.UItest.new_game()

            stim.append(int_action)
        else:
            stim.append(0)
        array_data.append(data)

        # if we finish the experiment time drop the thread
        if int(all_time) >= self.params["EXPERIMENT_DURATION"]:
            self.board.stop_stream()
