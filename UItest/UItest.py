import time


class UItest:
    def __init__(self):
        """

        :rtype: object
        """
        self.current_time = 0
        self.time_to_wait = 2000
    def new_game(self,action):
        time.sleep(self.time_to_wait)
        self.current_time = 0
        print("####new game####")
        
        arrows = {
            1 : "<--",
            2 : "-->",
            3 : "--"
        }
        
        print(f"{arrows[action]}")
    def step(self,prediction):
        '''

        :param prediction: int with predicted move
        :return:
        '''
        self.current_time+=1
    def get_game_time(self):
        return self.current_time
