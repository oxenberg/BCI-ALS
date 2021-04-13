from UItest import UI
import pygame as pg
import random

#########################################
#            READ THIS                  #
#########################################
# For this to work without a helmet, you must comment out the line:
# "from .inputModule import SignalReader" in the file "inputModule\__init__.py"


def run_simulation(num_trials=1):

    actions = [random.randint(1,3) for j in range(num_trials)]

    for i in range(num_trials):
        print("new game")
#        pg.event.get()
        ui.new_game(action=actions[i])
       # breaktime(breaks=10)


def breaktime(breaks=1):
    delay = ui.params['EXPERIMENT_DURATION'] - (ui.blink_duration * ui.blinks)
    for i in range(breaks):
     #   pg.event.get()
        print("Starting break #" + str(i))
        pg.time.delay(round(delay/breaks))

if __name__ == '__main__':
    ui = UI()
    A = 1
    run_simulation(num_trials=ui.params['ROUNDS_TO_PLAY'])