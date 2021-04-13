import SSVEP.flick
from UItest import UISkeleton
import pygame as pg
import time
from SSVEP import flick
from multiprocessing import Process


from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


class UI(UISkeleton.UISkeletonClass):
    def __init__(self):
        UISkeleton.UISkeletonClass.__init__(self)

        # Initialize pygame
        pg.init()

        # Define constants for the screen width and height
        self.screen_width = 800
        self.screen_height = 600

        # Create the screen object
        # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))

        # Fill the screen with white
        self.screen.fill((255, 255, 255))

        # state unified font for the game
        pg.font.init()
        self.font = pg.font.SysFont('Comic Sans MS', 30)

        # used for filling bar
        self.progress = 0
        self.bar_params = {'pos': (self.screen_width / 2 - 100, self.screen_height * 3 / 4 - 10), 'size': (200, 20),
                           'border_color': (0, 0, 0), 'bar_color': (0, 128, 0)}

        # used for pre-trial stimulus
        self.blinks = 3
        self.blink_duration = 0.333

        # arrow image parameters
        self.current_image = None
        self.image_center = (self.screen_width / 2, self.screen_height / 4)

        # display start screen
        self.start_screen()

    def start_screen(self):
        screen_width, screen_height = self.screen_width, self.screen_height

        button = pg.Rect(screen_width / 2 - 50, screen_height * 3 / 4 - 50, 100, 100)
        hellosurface = self.font.render('Hello', False, (0, 0, 0))
        hello_rect = hellosurface.get_rect(center=(screen_width / 2, screen_height / 4))

        startsurface = self.font.render('start', True, (170, 170, 170))
        start_rect = startsurface.get_rect(center=(screen_width / 2, screen_height * 3 / 4))

        pg.draw.rect(self.screen, [100, 100, 100], button)
        self.screen.blit(startsurface, start_rect)
        self.screen.blit(hellosurface, hello_rect)

        pg.display.flip()

        running = True
        while running:
            # Look at every event in the queue
            for event in pg.event.get():
                # Did the user hit a key?
                if event.type == KEYDOWN:
                    # Was it the Escape key? If so, stop the loop.
                    if event.key == K_ESCAPE:
                        running = False

                # Did the user click the window close button? If so, stop the loop.
                elif event.type == QUIT:
                    running = False

                # checks if a mouse is clicked
                elif event.type == pg.MOUSEBUTTONDOWN:

                    mouse_pos = event.pos  # gets mouse position

                    # checks if mouse position is over the button

                    if button.collidepoint(mouse_pos):
                        # erase text and button
                        self.screen.fill((255, 255, 255), hello_rect)
                        self.screen.fill((255, 255, 255), button)

                        # show empty bar for beginning of experiment
                        self.show_bar(**self.bar_params)

                        # update display
                        pg.display.flip()
                        running = False

    def show_bar(self, pos, size, border_color, bar_color, reset=False):
        pg.draw.rect(self.screen, border_color, (*pos, *size), 1)
        inner_pos = (pos[0] + 3, pos[1] + 3)
        inner_size = ((size[0] - 6) * (self.progress / self.params['BAR_MAX']), size[1] - 6)
        if reset:
            bar_color = (255, 255, 255)
            inner_size = ((size[0] - 6), size[1] - 6)
            pg.draw.rect(self.screen, bar_color, (*inner_pos, *inner_size))
        else:
            pg.draw.rect(self.screen, bar_color, (*inner_pos, *inner_size))
        pg.display.flip()
    def reset_bar(self):
        self.progress = 0
        self.show_bar(**self.bar_params, reset=True)

    def move_bar(self, action):
        action_name = self.params["ACTIONS"][str(action)]

        if not self.bar_is_full() and action_name != 'NONE':
            self.progress += 1
            self.show_bar(**self.bar_params)

    def bar_is_full(self):
        return self.progress == self.params['BAR_MAX']

    def new_game(self, action):

        pg.font.init()  # had a problem with trying to access the font from another thread
        self.font = pg.font.SysFont('Comic Sans MS', 30)

        new_round_surface = self.font.render('new round', False, (0, 0, 0))
        new_round_rect = new_round_surface.get_rect(center=(self.screen_width / 2, self.screen_height / 8))

        self.screen.blit(new_round_surface, new_round_rect)
        pg.display.flip()
        if self.current_image:
            im_rect = self.current_image.get_rect(center=self.image_center)
            self.screen.fill((255, 255, 255), im_rect)
            pg.display.flip()

        self.reset_bar()
        self.current_time = 0
        self.current_game_direction = action

        action_name = self.params['ACTIONS'][str(self.current_game_direction)]

        self.current_image = None
        if action_name == 'LEFT':
            self.current_image = pg.image.load(r'UIResources\left.png')

        elif action_name == 'RIGHT':
            self.current_image = pg.image.load(r'UIResources\right.png')

        else:
            self.current_image = pg.image.load(r'UIResources\idle.png')

        self.current_image = pg.transform.scale(self.current_image,(200,100))
        im_rect = self.current_image.get_rect(center=self.image_center)
        self.screen.blit(self.current_image, im_rect)
        pg.display.flip()

        for i in range(self.blinks):
            self.screen.fill((255, 255, 255), im_rect)
            pg.display.flip()
            time.sleep(self.blink_duration)
            self.screen.blit(self.current_image, im_rect)
            pg.display.flip()
            time.sleep(self.blink_duration)

        self.screen.fill((255, 255, 255), new_round_rect)
        pg.display.flip()
        if action_name == 'LEFT':
            flick.Flick(float(11)).flicker(win=self.screen, posx=6, posy=6)
        elif action_name == 'RIGHT':
            flick.Flick(float(17)).flicker(win=self.screen, posx=1.5, posy=6)
        elif action_name == 'NONE':
            self.dont_stop(breaks=10)

        pg.time.delay(self.time_to_wait * 1000)
        pg.event.get()
        # time.sleep(self.time_to_wait)

    def dont_stop(self, breaks=1):
        delay = self.params['GAME_TIME_LIMIT'] - (self.blink_duration * self.blinks)
        for i in range(breaks):
            #pg.event.get()
            print("Starting break #" + str(i))
            pg.time.delay(round(delay / breaks))
        pg.event.get()


    def run_ssvep(self, freqz=1,posxx=1,posyy=1):
        flick.Flick(float(freqz)).flicker(win=self.screen, posx=posxx, posy=posyy)

    def end_all_rounds(self):
        if self.round > self.params["ROUNDS_TO_PLAY"]:
            self.screen.fill((255, 255, 255))
            finishsurface = self.font.render('Game Finished - thanks for playing', False, (0, 0, 0))
            finish_rect = finishsurface.get_rect(center=(self.screen_width / 2, self.screen_height / 4))
            self.screen.blit(finishsurface, finish_rect)
            pg.display.flip()
            return True
        return False


if __name__ == '__main__':
    ui = UI()

