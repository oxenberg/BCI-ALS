from pyOpenBCI import OpenBCICyton
import time
import numpy as np
from collections import deque

# work library
from inputModule.utils import read_params
from UItest import UISkeleton, UI
from PredictionModelModule import PredictionModel
from plotter import Plotter


class SignalReader:

    def __init__(self):
        self.params = read_params()  # global experiment params
        self.start_time = time.time()
        self.ITER = 0  # for counting the time
        self.int_action = self.params["DEFAULT_ACTION"]
        self.stims = []
        self.all_game_data = []
        self.predicted_labels_to_game = []
        # windows for 1 prediction and for batch
        self.batch = {"X": [], "y": []}
        self.window_data = deque(maxlen=self.params["PREDICTION_WINDOW_SIZE"])  # this window have prediction data

        # modules initialization
        self.board = OpenBCICyton(port='COM3', daisy=True)
        self.UItest = UI()  # UI module
        self.prediction_model = PredictionModel()
        self.plotter = Plotter(self.params["DEBUG"])
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
                prediction = self.prediction_model.predict(list(self.window_data))[0]
                self.UItest.step(prediction)
                stim = self.int_action
                self.predicted_labels_to_game.append(prediction)
            else:
                self.UItest.step()  # continue the time counting for the game
                stim = self.params["DEFAULT_ACTION"]

            self.window_data.append(data)
            self.all_game_data.append(data)
            self.stims.append(stim)

        # if we finish the experiment stop streaming
        elif self.UItest.end_all_rounds():
            self.plotter.collect_data(self.UItest.get_round(), self.predicted_labels_to_game, self.int_action)
            self.plotter.save_data()
            self.plotter.plot()
            self.board.stop_stream()
        # new game and in the first round init the values
        else:
            # collect data to plot
            self.plotter.collect_data(self.UItest.get_round(), self.predicted_labels_to_game, self.int_action)
            # not need to train for first round and train time
            if not self.UItest.get_round() == 1 and train_time:
                self.prediction_model.updateModel(self.all_game_data, self.stims)
                self.stims = []
                self.all_game_data = []

            self.predicted_labels_to_game = []
            # restart window data, ##need to change if we want more
            self.window_data.clear()
            # start new game with random action
            self.int_action = np.random.randint(1, len(self.params["ACTIONS"]) + 1)

            self.UItest.new_game(self.int_action)


        self.ITER += 1
