# Главная программа
from gc import callbacks

# 1 - Импортируем модули

import pygame
import sys

from game import *
from authorization import *
from constants import *

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
flag = False



# 6 - Бесконечный цикл
while True:
    board_dict = None
    # 7 - Проверяем на наличие событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                print(board_dict)
                flag = not flag

        if Authorization.LOGIN_AWAITING_STATUS:

            o_auth.login_input.handleEvent(event)
            o_auth.password_input.handleEvent(event)
            o_auth.login_button.handleEvent(event)


            if o_auth.login_input.getValue() != '' and o_auth.password_input.getValue() != '':
                    o_auth.login_button.enable()
            else:
                o_auth.login_button.disable()

            o_auth.draw()

        else:

            o_game.event_manager(event)
            o_game.new_game_button.handleEvent(event)
            o_game.choose_time_button.handleEvent(event)
            o_game.draw(flag)

            o_game.quit_button.handleEvent(event)



        # 8 - Обновляем экран
        pygame.display.update()

        # 9 - Обновляем частоту кадров
        clock.tick(FRAMES_PER_SECOND)