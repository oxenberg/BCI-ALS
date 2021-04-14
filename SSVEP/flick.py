import pygame
from pygame.locals import *
from SSVEP import checkerboard
from numpy import mean
import time
import os
import sys

pygame.init()
pygame.font.init()
from inputModule.utils import read_params
VERBOSE = False


class Flick:
    """
    |   Object for creating one pygame window and animate it
    """
    def __init__(self, freq, x=0, y=0):

        self.params = read_params()
        self.freq = freq
        self.x = int(x)
        self.y = int(y)
        self.win_x, self.win_y = (500, 400)     # Size of flicker window
        self.board_pos = (0, 0)

        self.IMAGES = [
                  checkerboard.create(0),
                  checkerboard.create(1)
                  ]

    def _freq_controller(self, clock, freq_array):
        """
        |   Frequency Controller, that reduces constant jitter offset
        """
        dt = clock.tick()/1000.0
        freq_array.append(1.0/dt)
        act_freq = mean(freq_array)
        error = self.freq-act_freq
        self.integral += error*dt
        derivative = (error - self.prev_error)/dt
        self.prev_error = error
        corr = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        if VERBOSE:
            print("Actual Freq", 1.0/dt)
            print("Error: ", self.freq-1./dt)
            print("Correction: ",corr)
        if corr <0:
            breakpoint = 1
        return self.freq + corr

    def _set_window_position(self):
        if (self.x + self.y > 0):
            if self.x > 0:
                pos_x = self.x - self.win_x/2
            else:
                pos_x = self.x
            if self.y > 0:
                pos_y = self.y - self.win_y/2
            else:
                pos_y = self.y
            os.environ['SDL_VIDEO_CENTERED'] = '0'
            os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (pos_x, pos_y)
        else:
            os.environ['SDL_VIDEO_CENTERED'] = '1'
        return False


    def flicker(self, win = pygame.display.set_mode((1920, 1080), 0), posx = 3, posy=3, offline = True, time_between = 0):
        """
        |   Opens a window and animates a flickering checkerboard
        |   Input:
        |       duration - duration of the flickering panel in seconds
        """
        self.integral = 0.
        self.prev_error = 0
        self.Kp, self.Ki, self.Kd = (1.4, 1.4, 0.05)
        _freq_array = []
        timer_event = USEREVENT + 1
        #self._set_window_position()
        if not offline:
            duration = self.params["GAME_TIME_LIMIT"]
        else:
            duration = time_between
        if duration != 0:
            window = win  #  pygame.display.set_mode((1920, 1080), 0)
            self.board_pos = (GetSystemMetrics(0)/posx, GetSystemMetrics(1)/posy)
            print(f"flicker duration {duration}")
            pygame.time.set_timer(timer_event, duration)
        else:
            window = pygame.display.set_mode((self.win_x, self.win_y), 0)
        pygame.display.set_caption("Frequency %s Hz" % self.freq)
        pygame.mouse.set_visible(False)
        clock = pygame.time.Clock()
        start = clock.tick()
        period = 1./(self.freq)
        break_this = False
        while not break_this:
            for event in pygame.event.get():
                if event.type == QUIT:
                    # pygame.quit()
                    # sys.exit()
                    print("quit")
                    break_this = True
                    break
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        # pygame.quit()
                        print("escape")
                        break_this = True
                        break
                        return False
                if event.type == timer_event:
                    # pygame.quit()
                    print("end round")
                    break_this = True
                    break
                    return False

            window.blit(self.IMAGES[0], self.board_pos)
            pygame.display.update()
            time.sleep(period)
            period = 1./self._freq_controller(clock, _freq_array)
            window.blit(self.IMAGES[1], self.board_pos)
            pygame.display.update()
            time.sleep(period)
            period = 1./self._freq_controller(clock, _freq_array)
