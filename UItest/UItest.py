import time
from inputModule.utils import read_params


class UItest:
    def __init__(self):
        """

        :rtype: object
        """
        self.params = read_params()
        self.current_time = 0
        self.time_to_wait = 2000
        self.round = 0
        self.left_space = 8
        self.right_space = 8
        self.X_space = 1
        self.bar = f"|{' ' * self.left_space}{'X' * self.X_space}{' ' * self.right_space}|"

    def move_bar(self, action):
        action_name = self.params["ACTIONS"][str(action)]

        if action_name == "RIGHT":
            self.bar = f"|{' ' * self.left_space}{'X' * self.X_space + 1}{' ' * self.right_space - 1}|"
        elif action_name == "RIGHT":
            self.bar = f"|{' ' * self.left_space - 1}{'X' * self.X_space + 1}{' ' * self.right_space}|"

        # no need feedback for None

    def new_game(self, action):
        time.sleep(self.time_to_wait)
        self.round += 1
        self.current_time = 0
        print("####new game####")

        arrows = {
            1: "<--",
            2: "-->",
            3: "--"
        }
        self.move_bar(action)
        print(f"{arrows[action]}")

    def step(self, prediction=None):
        '''

        :param prediction: int with predicted move
        :return:
        '''
        self.current_time += 1
        print(self.bar)

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
