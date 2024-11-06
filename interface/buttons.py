# Класс умной кнопки, в которой переназначается функция нажатия
import pygwidgets
import pygame

from constants import *
from game import *

MOUSE_EVENTS_LIST = [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]

class ChooseTimeButton(pygwidgets.TextButton):

    TIMES_LIST = [(10, 5), (10, 0), (30, 0), (30, 15), (45, 0), (5, 0), (5, 3)]

    def __init__(self, window, loc, text, width=180, height=45, fontSize=22):
        self.default_time = ChooseTimeButton.TIMES_LIST[0]
        self.font = pygame.font.Font(None, 24)
        self.default_text_image = self.font.render('CHOOSE TIME', True, DARK_GRAY)
        super().__init__(window, loc, text, width, height, fontSize)

        self.new_coords = self.rect.move(35, 15)
        self.current_text = self.default_text_image


    def handleEvent(self, event):

        if event.type in MOUSE_EVENTS_LIST:

            event_point_in_button_rect = self.rect.collidepoint(event.pos)

            if event.type == pygame.MOUSEBUTTONDOWN and event_point_in_button_rect:
                self.state = self.STATE_ARMED
                self.alter_time()

            elif event_point_in_button_rect:
                self.display_time()
                self.state = self.STATE_OVER

            else:
                self.current_text = self.default_text_image
                self.state = self.STATE_IDLE

        super().handleEvent(event)



    def alter_time(self):
        current_time = self.default_time
        for index in range(0, len(ChooseTimeButton.TIMES_LIST)):
            if current_time == ChooseTimeButton.TIMES_LIST[index]:
                if index == len(ChooseTimeButton.TIMES_LIST) - 1:
                    self.default_time = ChooseTimeButton.TIMES_LIST[0]
                else:
                    self.default_time = ChooseTimeButton.TIMES_LIST[index + 1]
                break

    def display_time(self):
        msg = f'{str(self.default_time[0])} + {str(self.default_time[1])}'
        msg_image = self.font.render(msg, True, DARK_GRAY)
        self.current_text = pygame.transform.scale_by(msg_image, 1.5)

    def draw(self):
        super().draw()
        self.window.blit(self.current_text, self.new_coords)
