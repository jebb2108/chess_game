# Модуль для добавления функциональных кнопок,
# переназначая свойства базового класса PygWidgetsButton
import pyghelpers
import pygwidgets
import pygame

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

    def get_time(self):
        return self.default_time

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

        self.font.set_point_size(42)
        msg = f'{str(self.default_time[0])} + {str(self.default_time[1])}'
        msg_image = self.font.render(msg, True, DARK_GRAY)
        msg_rect = msg_image.get_rect()
        msg_rect.center = self.rect.center

        self.msg_image = pygwidgets.Image(self.window, msg_rect, msg_image)
        self.msg_image.scale(50, True)
        self.current_text = False

    def draw(self):
        super().draw()
        if self.current_text:
            self.window.blit(self.current_text, self.new_coords)
        else:
            self.msg_image.draw()

class ChessClock():
    def __init__(self, window, loc, color, time):
        self.window = window
        self.loc = loc
        self.rect = pygame.Rect(self.loc[0], self.loc[1], 100, 45)
        self.color = color
        self.time = time[0] * 60

        self.font = pygame.font.Font(None, 24)
        self.clock = pyghelpers.CountDownTimer(self.time, True)
        self.clock.start()


    def update(self, curr_turn):

        if self.clock.ended():
            return False

        elif ((self.color == COLOR_WHITE and curr_turn == COLOR_BLACK) or
                (self.color == COLOR_BLACK and curr_turn == COLOR_WHITE)):
            self.change_state(True)

            if self.clock.pauseCounter > 0:
                if self.clock.timePaused:
                    self.clock.resume()

            return True

        else:
            self.clock.pause()
            self.change_state(False)
            return True

    def change_state(self, active: bool):
        if active:
            self.active_color = WHITE if self.color == COLOR_WHITE else BLACK
            self.text_color = BLACK if self.color == COLOR_WHITE else WHITE
        else:
            self.active_color = GRAY
            self.text_color = LIGHT_GRAY

        text = self.font.render(self.clock.getTimeInHHMMSS(), True, self.text_color)
        text_rect = text.get_rect()
        text_rect.center = self.rect.center
        self.time_as_img = pygwidgets.Image(self.window, text_rect, text)




    def draw(self):
        pygame.draw.rect(self.window, self.active_color, self.rect, 0, 5)
        #Граница
        pygame.draw.rect(self.window, DARK_GRAY, self.rect, 2, 5)
        self.time_as_img.draw()



