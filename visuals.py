# Модуль для добавления функциональных кнопок,
# переназначая свойства базового класса PygWidgetsButton
import time

import pyghelpers
import pygwidgets
import pygame

from constants import *


class Timer:

    def __init__(self, n_seconds, stop_at_zero=True, nickname=None, call_back=None):
        self.n_starting_seconds = n_seconds
        self.stop_at_zero = stop_at_zero
        self.nickname = nickname
        self.call_back = call_back

        self.running = False
        self.reached_zero = False
        self.remaining_seconds = float(n_seconds)
        # считает кол-во пауз, чтобы предупредить ошибку
        self.pause_counter = 0

    def start(self, new_starting_seconds=None):
        seconds_now = time.time()
        if new_starting_seconds is not None:
            self.n_starting_seconds = new_starting_seconds
        self.seconds_end = seconds_now + self.n_starting_seconds
        self.reached_zero = False
        self.running = True
        self.paused = False
        self.time_paused = None
        self.pause_counter = 0

    def get_time(self):
        if not self.running or self.paused:
            return self.remaining_seconds

        self.remaining_seconds = self.seconds_end - time.time()
        if self.stop_at_zero and (self.remaining_seconds <= 0):
            self.remaining_seconds = 0.0
            self.running = False
            self.reached_zero = True

        return self.remaining_seconds  # возвращает вещественное число

    def get_time_in_seconds(self):
        n_seconds = int(self.get_time())
        return n_seconds

    def get_time_formated(self):
        n_seconds = self.get_time()
        mins, secs = divmod(n_seconds, 60)

        if mins > 0:
            output = '{mins:02d}:{secs:02d}'.format(mins=int(mins), secs=int(secs))
        else:
            output = '00:{secs:02d}'.format(secs=int(secs))

        self.seconds_elapsed = output
        return output

    def stop(self):
        """ Останавливает таймер и сбрасывает все значения """
        self.get_time()  # помнит конечное время в секундах
        self.running = False
        self.paused = False
        self.pause_counter = 0

    def ended(self):

        """ Вызывается, когда нужно проверить, закончился ли таймер.
           Должно быть вызвано после каждого прохождения цикла в игре """

        self.get_time()  # Вызывается, чтобы установить self.reachedZero
        if self.reached_zero:
            self.reached_zero = False  # Обновляет значение
            if self.call_back is not None:
                self.call_back(self.nickname)
            return True
        else:
            return False

    def pause(self):
        """Ставит таймер на паузу"""
        self.pause_counter = self.pause_counter + 1
        self.time_paused = time.time()
        self.paused = True

    def resume(self):
        """ Продолжает работу таймера после паузы """
        if self.pause_counter == 0:
            print('Warning - called resume timer but the timer is not paused ... ignored')
        else:
            self.pause_counter = self.pause_counter - 1
        if self.pause_counter != 0:
            return  # don't resume

        # OK to resume
        pause_time = time.time() - self.time_paused
        self.seconds_end = self.seconds_end + pause_time
        self.paused = False


class ChooseTimeButton(pygwidgets.TextButton):
    # список событий мыши, на которые реагирует кнопка
    MOUSE_EVENTS_LIST = [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]
    # время в формате (минуты, секунды)
    TIMES_LIST = [(10, 5), (10, 0), (30, 0), (30, 15), (45, 0), (5, 0), (5, 3)]

    def __init__(self, window, loc, text, width=180, height=45, fontSize=22):
        self.state = self.STATE_IDLE
        self.set_default_time()
        self.font = pygame.font.Font(None, 24)
        self.default_text_image = self.font.render('CHOOSE TIME', True, DARK_GRAY)
        super().__init__(window, loc, text, width, height, fontSize)

        self.new_coords = self.rect.move(35, 15)
        self.current_text = self.default_text_image

    def set_default_time(self):
        self.default_time = ChooseTimeButton.TIMES_LIST[0]

    def handleEvent(self, event):

        # кнопка заботится только о событиях мыши
        if event.type in ChooseTimeButton.MOUSE_EVENTS_LIST:

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


class ChessClock(Timer):

    FONT = pygame.font.Font(None, 24)

    def __init__(self, window, loc, color, starting_time):

        self.window = window
        self.loc = loc
        self.color = color

        n_seconds = starting_time[0] * 60
        self.time_increase = starting_time[1]
        super().__init__(n_seconds, True)

        self.rect = None

    def set_increase_time(self, time_increase):
        self.time_increase = time_increase

    def increase_time(self):
        self.remaining_seconds += self.time_increase

    def set_color(self):

        if self.rect is None:
            self.rect = pygame.Rect(self.loc[0], self.loc[1], 100, 45)

        if not self.paused:
            self.active_color = WHITE if self.color == COLOR_WHITE else BLACK
            self.text_color = BLACK if self.color == COLOR_WHITE else WHITE
        else:
            self.active_color = GRAY
            self.text_color = LIGHT_GRAY

        text = ChessClock.FONT.render(self.get_time_formated(), True, self.text_color)
        text_rect = text.get_rect()
        text_rect.center = self.rect.center
        self.time_as_img = pygwidgets.Image(self.window, text_rect, text)

        return

    def draw(self):
        pygame.draw.rect(self.window, self.active_color, self.rect, 0, 5)
        #Граница
        pygame.draw.rect(self.window, DARK_GRAY, self.rect, 2, 5)
        self.time_as_img.draw()







