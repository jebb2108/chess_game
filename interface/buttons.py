# Модуль для добавления функциональных кнопок,
# переназначая свойства базового класса PygWidgetsButton

import pygwidgets
import pygame

#
from constants import *

# список событий мыши, на которые реагирует кнопка
MOUSE_EVENTS_LIST = [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]


class ChooseTimeButton(pygwidgets.TextButton):
    # время в формате (минуты, секунды)
    TIMES_LIST = [(10, 5), (10, 0), (30, 0), (30, 15), (45, 0), (5, 0), (5, 3)]

    def __init__(self, window, loc, text, width=180, height=45, fontSize=22):
        self.state = self.STATE_IDLE
        self.default_time = ChooseTimeButton.TIMES_LIST[0]
        self.font = pygame.font.Font(None, 24)
        self.default_text_image = self.font.render('CHOOSE TIME', True, DARK_GRAY)
        super().__init__(window, loc, text, width, height, fontSize)

        self.new_coords = self.rect.move(35, 15)
        self.current_text = self.default_text_image

    def handleEvent(self, event):

        # кнопка заботится только о событиях мыши
        if event.type in MOUSE_EVENTS_LIST:

            # создает переменную для координат курсора
            event_point_in_button_rect = self.rect.collidepoint(event.pos)

            # иначе, если курсор в пределах кнопки,
            # то кнопка меняет свое состояние на активную
            if event_point_in_button_rect:
                self.state = self.STATE_OVER
                self.display_time()

                # нажата левая кнопка мыши
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.state = self.STATE_ARMED
                    self.alter_time()


            else:
                self.current_text = self.default_text_image
                self.state = self.STATE_IDLE

        # после модификации кнопки,
        # вызываем метод родительского класса
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
