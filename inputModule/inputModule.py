from pyOpenBCI import OpenBCICyton
import time
import numpy as np
from collections import deque

# work library
from inputModule.utils import read_params
from UItest import UItest
from PredictionModelModule import PredictionModel


class SignalReader:

    def __init__(self):
        self.params = read_params()  # global experiment params
        self.start_time = time.time()
        self.ITER = 0  # for counting the time
        self.int_action = self.params["DEFAULT_ACTION"]
        self.stims = []
        self.all_game_data = []
        # windows for 1 prediction and for batch
        self.batch = {"X": [], "y": []}
        self.window_data = deque(maxlen=self.params["PREDICTION_WINDOW_SIZE"])  # this window have prediction data

        # modules initialization
        self.board = OpenBCICyton(port='COM3', daisy=True)
        self.UItest = UItest()  # UI module
        self.prediction_model = PredictionModel()

        self.counter = 0


    def start_experiment(self):
        '''
        this function activate all the online experiment session and games.
        '''

        self.board.start_stream(self.run_online)
        self.board.disconnect()

    def run_online(self, sample):
        self.counter += 1
        # read data from sensor
        data = np.array(sample.channels_data) * self.params["uVolts_per_count"]

        all_time = time.time() - self.start_time

        # round_not_end = bool(self.ITER % self.params["TIME_BETWEEN_GAMES"])
        predict_time = not bool(self.UItest.get_game_time() % self.params["TIME_BETWEEN_PREDICTIONS"])
        train_time = bool(self.UItest.get_round() % self.params["ROUNDS_BETWEEN_TRAIN"])
        # print(self.UItest.end_game())
        # in the first integration the round_not_end always be 0 and the else will activate
        if not self.UItest.end_game():
            # need to check if window gap time over and if the window not empty
            if predict_time and len(self.window_data) == self.params["PREDICTION_WINDOW_SIZE"] :
                prediction = self.prediction_model.predict(list(self.window_data))
                self.UItest.step(prediction[0])
                stim = self.int_action

            else:
                self.UItest.step()  # continue the time counting for the game
                stim = self.params["DEFAULT_ACTION"]

            self.window_data.append(data)
            self.all_game_data.append(data)
            self.stims.append(stim)

        # if we finish the experiment stop streaming
        elif self.UItest.end_all_rounds():
            self.board.stop_stream()
        # new game and in the first round init the values
        else:
            # not need to train for first round
            if not self.UItest.get_round() == 1:
                self.prediction_model.updateModel(self.all_game_data, self.stims)
            # restart window data, ##need to change if we want more
            self.window_data.clear()
            self.all_game_data = []
            self.stims = []
            # start new game with random action
            self.int_action = np.random.randint(1, len(self.params["ACTIONS"]) + 1)
            self.UItest.new_game(self.int_action)


        self.ITER += 1
