# Класс Game

import pygwidgets
import pygame

from constants import *
from settings import Settings


class Game:
    TIMES_LIST = [(10, 5), (10, 0), (30, 0), (30, 15), (45, 0), (5, 0), (5, 3)]

    BACKGROUND_IMAGE = pygame.image.load('images/background.png')
    BOARD_IMAGE = pygame.image.load('images/chess_board.jpg')

    def __init__(self, window):
        self.window = window
        self.default_time = Game.TIMES_LIST[0]
        self.font = pygame.font.Font(None, 40)
        self.new_game_button = pygwidgets.TextButton(self.window, (20, 640), 'NEW GAME', width=180, height=45,
                                                     fontSize=22)
        self.choose_time_display = pygwidgets.DisplayText(self.window, (265, 655), 'CHOOSE TIME', width=180, height=45,
                                                          fontSize=22)
        self.choose_time_button = pygwidgets.TextButton(self.window, (230, 640), '', width=180, height=45, fontSize=22)
        self.profile_button = pygwidgets.TextButton(self.window, (440, 640), 'PROFILE', width=180, height=45,
                                                    fontSize=22)
        self.quit_button = pygwidgets.TextButton(self.window, (745, 640), 'QUIT', width=100, height=45, fontSize=22)

        self.buttons = [self.new_game_button, self.choose_time_button, self.profile_button, self.quit_button]

        self.board = Game.BOARD_IMAGE
        self.board_rect = self.board.get_rect()
        self.board_rect.top, self.board_rect.left = 20, 20

        self.board_rects = list()
        self.linked_rects_dict = dict().fromkeys(range(64), IDLE)

    def event_manager(self, event):
        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
            pos_x, pos_y = pygame.mouse.get_pos()
            for rect in self.board_rects:
                key = self.board_rects.index(rect)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if rect.collidepoint(pos_x, pos_y):
                        if self.linked_rects_dict[key] == HOVER:
                            self.linked_rects_dict[key] = SELECTED

                else:
                    if self.linked_rects_dict[key] == IDLE:
                        self.linked_rects_dict[key] = HOVER

        for key, value in self.linked_rects_dict.items():
            if value == SELECTED:
                gen = list([key for key, value in self.linked_rects_dict.items() if value == SELECTED])
                if len(gen) > 1:
                    for item in gen:
                        self.linked_rects_dict[item] = IDLE

            if value == HOVER and not (self.board_rects[key].collidepoint(pygame.mouse.get_pos())):
                self.linked_rects_dict[key] = IDLE

    def alter_time(self):
        current_time = self.default_time
        for index in range(0, len(Game.TIMES_LIST)):
            if current_time == Game.TIMES_LIST[index]:
                if index == len(Game.TIMES_LIST) - 1:
                    self.default_time = Game.TIMES_LIST[0]
                else:
                    self.default_time = Game.TIMES_LIST[index + 1]
                break

    def check_time_button(self):
        if self.choose_time_button.state in ['armed', 'OVER']:
            msg = f'{str(self.default_time[0])} + {str(self.default_time[1])}'
            msg_image = self.font.render(msg, True, (0, 0, 0))
            self.window.blit(msg_image, (285, 650))

        else:
            self.choose_time_display.draw()

    def show_borders(self, flag):
        offset_xy = 10

        if flag:
            pygame.draw.rect(self.window, RED, (50, 50, 540, 540), 5)

        left_border, top_border = 50 + 15, 50 + 15
        height_adjustment = 0

        for _ in range(1, 9):
            width_adjustment = 0

            for _ in range(8):
                if flag:
                    pygame.draw.rect(self.window, GREEN,
                                     (left_border + width_adjustment, top_border + height_adjustment, 55, 55), 2)

                width_adjustment += 55 + offset_xy
                if len(self.board_rects) != 64:
                    single_rect = pygame.Rect(width_adjustment, top_border + height_adjustment, 55, 55)
                    self.board_rects.append(single_rect)

            height_adjustment += 55 + offset_xy

        if flag:
            for key, value in self.linked_rects_dict.items():
                if value in [SELECTED, HOVER]:
                    rect = self.board_rects[key]
                    pygame.draw.rect(self.window, GREEN, [rect.x, rect.y, 55, 55], 10)

        # print(self.chained_rects_dict)
        return None


    def draw(self, flag=False):
        self.window.fill(LIGHT_GRAY)
        for button in self.buttons:
            button.draw()
        self.check_time_button()
        self.window.blit(self.board, self.board_rect)
        self.show_borders(flag)
