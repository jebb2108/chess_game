# Главная программа

# 1 - Импортируем модули

import os
import pygame
import pygwidgets
import sys

from game import *
from authorization import *
from settings import *

# 2 - Определяем константы
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 720
FRAMES_PER_SECOND = 30

# 3 - Инициализируем окружение
pygame.init()
pygame.display.set_caption('Chess Game')
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# 4 - Загружаем элементы: изображения, звуки и т.д.
BACKGROUND_IMAGE = pygame.image.load('images/background.png')
BOARD_IMAGE = pygame.image.load('images/chess_board.jpg')

# 5 - Инициализируем переменные
o_auth = Authorization(window)
o_game = Game(window)
login_awaiting_status = True


# 6 - Бесконечный цикл
while True:
    # 7 - Проверяем на наличие событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

        if login_awaiting_status:
            o_auth.login_input.handleEvent(event)
            o_auth.password_input.handleEvent(event)
            o_auth.draw()

            if o_auth.login_button.handleEvent(event) and o_auth.check_authorization():
                login_awaiting_status = False
                break


        else:
            o_game.new_game_button.handleEvent(event)
            if o_game.choose_time_button.handleEvent(event):
                o_game.alter_time()

            o_game.draw()

            if o_game.quit_button.handleEvent(event):
                o_auth.login_input.setValue('')
                o_auth.password_input.setValue('')
                login_awaiting_status = True
                window.fill(BLACK)
                break



        # 8 - Обновляем экран
        pygame.display.update()

        # 9 - Обновляем частоту кадров
        clock.tick(FRAMES_PER_SECOND)