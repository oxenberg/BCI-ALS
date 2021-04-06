import time
from inputModule.utils import read_params


class UItest:
    def __init__(self):
        """

        :rtype: object
        """
        # TODO this class init call early, so if you want to create your "GUI board" you can do it here.

        self.params = read_params()
        self.current_time = 0
        self.time_to_wait = 5
        self.round = 0

        # TODO this params is for the test only need to change to your GUI params
        # ------------------------------------------------------------------
        self.left_space = self.params["BAR_MAX"]
        self.right_space = self.params["BAR_MAX"]
        self.X_space = 1
        # ------------------------------------------------------------------

        self.current_game_direction = 0

    def reset_bar(self):
        # TODO change here to reset the GUI after game
        self.left_space = self.params["BAR_MAX"]
        self.right_space = self.params["BAR_MAX"]
        self.X_space = 1
        self.bar = f"|{' ' * self.left_space}{'X' * self.X_space}{' ' * self.right_space}|"

    def bar_is_full(self):
        # TODO change here to the way you checks if the bar full
        return self.X_space >= self.params["BAR_MAX"]

    def move_bar(self, action):
        action_name = self.params["ACTIONS"][str(action)]

        if not self.bar_is_full():

            # TODO change here what happen if the GUI got right or left
            if action_name == "RIGHT":

                self.X_space += 1
                self.right_space -= 1
                self.bar = f"|{' ' * self.left_space}{'X' * self.X_space}{' ' * self.right_space}|"
            elif action_name == "LEFT":
                self.X_space += 1
                self.left_space -= 1
                self.bar = f"|{' ' * (self.left_space - 1)}{'X' * (self.X_space + 1)}{' ' * self.right_space}|"

        # no need feedback for None

    def new_game(self, action):
        self.reset_bar()
        self.current_time = 0
        self.current_game_direction = action
        # TODO change here print the "new game" notification and the direction to think about
        #  please see reset_bar function for change the bar status
        print(f"##########new game {self.round}/{self.params['ROUNDS_TO_PLAY']}##########")

        # dict to map the income request for the direction of the game to printable value
        arrows = {
            1: "<--",
            2: "-->",
            3: "--"
        }

        print(f"{arrows[action]}")
        print(self.bar, end='\r')
        time.sleep(self.time_to_wait)

    def step(self, prediction=None):
        '''

        :param prediction: int with predicted move
        :return:
        '''
        # TODO no need to change
        if prediction == self.current_game_direction:
            self.move_bar(prediction)
        self.current_time += 1
        print(self.bar)

    def get_game_time(self):
        # TODO no need to change
        return self.current_time

    def end_game(self):
        # TODO no need to change
        # if the time of the round ends or you in the init round or the bar is full
        if self.current_time >= self.params["GAME_TIME_LIMIT"] or self.round == 0 or self.bar_is_full():
            self.round += 1
            return True
        else:
            return False

    def end_all_rounds(self):
        if self.round > self.params["ROUNDS_TO_PLAY"]:
            # TODO change to what happen if the game end
            print("game end, thanks")
            return True
        return False

    def get_round(self):
        # TODO no need to change
        return self.round
