# Класс Game

import pygwidgets
import pygame
from constants import *


class Game:

    TIMES_LIST = [(10, 5), (10, 0), (30, 0), (30, 15), (45, 0), (5, 0), (5, 3)]

    BACKGROUND_IMAGE = pygame.image.load('images/background.png')
    BOARD_IMAGE = pygame.image.load('images/chess_board.jpg')


    def __init__(self, window):
        self.window = window
        self.default_time = Game.TIMES_LIST[0]
        self.font = pygame.font.Font(None, 40)
        self.new_game_button = pygwidgets.TextButton(self.window, (20, 640), 'NEW GAME', width=180, height=45,fontSize=22)
        self.choose_time_display = pygwidgets.DisplayText(self.window, (265, 655), 'CHOOSE TIME', width=180, height=45, fontSize=22)
        self.choose_time_button = pygwidgets.TextButton(self.window, (230, 640), '', width=180, height=45, fontSize=22)
        self.profile_button = pygwidgets.TextButton(self.window, (440, 640), 'PROFILE', width=180, height=45, fontSize=22)
        self.quit_button = pygwidgets.TextButton(self.window, (745, 640), 'QUIT', width=100, height=45, fontSize=22)

        self.buttons = [self.new_game_button, self.choose_time_button, self.profile_button, self.quit_button]

        self.board = Game.BOARD_IMAGE
        self.board_rect = self.board.get_rect()
        self.board_rect.top, self.board_rect.left = 20, 20






    def alter_time(self):

        current_time = self.default_time
        for index in range(0, len(Game.TIMES_LIST)):
            if current_time == Game.TIMES_LIST[index]:
                if index  == len(Game.TIMES_LIST)-1:
                    self.default_time = Game.TIMES_LIST[0]
                else:
                    self.default_time = Game.TIMES_LIST[index+1]
                break


    def check_time_button(self):
        if self.choose_time_button.state in ['armed', 'OVER']:
            msg = f'{str(self.default_time[0])} + {str(self.default_time[1])}'
            msg_image = self.font.render(msg, True, (0, 0, 0))
            self.window.blit(msg_image, (285, 650))

        else:
            self.choose_time_display.draw()








    def draw(self):
        self.window.fill(LIGHT_GRAY)
        for button in self.buttons:
            button.draw()
        self.check_time_button()
        self.window.blit(self.board, self.board_rect)
