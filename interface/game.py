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

        self.board_dict = dict()




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

    def show_borders(self, flag):
        alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        offset_xy = 10
        if flag:
            rect = pygame.draw.rect(self.window, RED, (50, 50, 540, 540), 5)
            left_border, top_border = rect[0] + 15, rect[1] + 15
            height_adjustment = 0

            for level in range(1, 9):
                width_adjustment = 0

                for num, char in enumerate(alpha, 0):
                    pygame.draw.rect(self.window, GREEN, (left_border + width_adjustment, top_border + height_adjustment, 55, 55), 2)
                    width_adjustment += 55 + offset_xy
                    resulted_numeric_coords = [(left_border+width_adjustment, top_border+height_adjustment), (level-1, num)]
                    visual_coords_by_alphabet = f'{str(char).title()}{str(level)}'
                    self.board_dict[visual_coords_by_alphabet] = resulted_numeric_coords

                height_adjustment += 55 + offset_xy


        return None


    def draw(self, flag=False):
        self.window.fill(LIGHT_GRAY)
        for button in self.buttons:
            button.draw()
        self.check_time_button()
        self.window.blit(self.board, self.board_rect)
        self.show_borders(flag)

