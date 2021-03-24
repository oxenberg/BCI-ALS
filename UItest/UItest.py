import time


class UItest:
    def __init__(self):
        """

        :rtype: object
        """
        self.time_to_wait = 2000
    def new_game(self,action):
        time.sleep(self.time_to_wait)
        print("####new game####")
        
        arrows = {
            1 : "<--",
            2 : "-->",
            3 : "--"
        }
        
        print(f"{arrows[action]}")
    
