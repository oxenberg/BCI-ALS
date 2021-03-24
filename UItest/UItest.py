import time
from inputModule import read_params

class UItest:
    def __init__(self):
        """

        :rtype: object
        """
        self.params = read_params()
        self.current_time = 0
        self.time_to_wait = 2000
        self.round = 0
    def new_game(self, action):
        time.sleep(self.time_to_wait)
        self.round +=1
        self.current_time = 0
        print("####new game####")

        arrows = {
            1: "<--",
            2: "-->",
            3: "--"
        }

        print(f"{arrows[action]}")

    def step(self, prediction):
        '''

        :param prediction: int with predicted move
        :return:
        '''
        self.current_time += 1

    def get_game_time(self):
        return self.current_time

    def end_game(self):
        if self.current_time >= self.params["GAME_TIME_LIMIT"]:
            return True
        else:
            return False

    def end_all_rounds(self):
        return False
    def get_round(self):
        return self.round