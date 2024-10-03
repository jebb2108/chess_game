import pygame
import pygwidgets

from settings import *

class ChooseMatch:

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 48)
        self.settings = Settings()
        self.default_option = 10
        self.display_button = self._create_display_button()

    def _create_display_button(self):
        button = pygwidgets.TextButton(self.screen, self.settings.DISPLAY_BUTTON_LOC, '',
                                       width=self.settings.DISPLAY_BUTTON_WIDTH)

        # text = f'{self.settings.time} + {self.settings.time_increase}'
        # my_font = pygame.font.SysFont('Comic Sans MS', 30)
        # text_surface = my_font.render(text, True, self.settings.DARK_GRAY)



        return button

    def display_menu(self):
        pygame.draw.rect(self.screen, self.settings.MATCHMAKING_WINDOW_COLOR,
                         self.settings.MATCHMAKING_WINDOW_LOC, 0)
        return None

    def display_play_button(self):
        button = pygwidgets.TextButton(self.screen, self.settings.PLAY_BUTTON_LOC, 'Start Game',
                                       width=self.settings.PLAY_BUTTON_WIDTH,
                                       textColor=(150, 0, 0), fontSize=40)
        return button.draw()

    def display_time_button(self):
        loc = self.settings.DISPLAY_BUTTON_LOC
        self.display_button.draw()
        text = f'{self.settings.time} + {self.settings.time_increase}'
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = my_font.render(text, True, self.settings.DARK_GRAY)
        return self.screen.blit(text_surface, (loc[0]+14, loc[1]-4))


    def show_options(self):
            self.display_menu()
            self.display_time_button()
            self.display_play_button()
            return None