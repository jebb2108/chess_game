# Главная программа
# 1 - Импортируем модули

import pygame
import sys
import logging

from game import Game
from authorization import Authorization
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
chosen_piece = False



# 6 - Бесконечный цикл
while True:
    board_dict = None
    # 7 - Проверяем на наличие событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()


        if Authorization.LOGIN_AWAITING_STATUS:

            o_auth.event_manager(event)

            o_auth.login_input.handleEvent(event)
            o_auth.password_input.handleEvent(event)
            o_auth.login_button.handleEvent(event)
            o_auth.draw()

        elif o_game.game_mgr.playing:

            o_game.checkmate_window.hide()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    flag = not flag
                    chosen_piece = not chosen_piece

            elif event.type == pygame.MOUSEBUTTONDOWN:
                o_game.got_click(event.pos)

            elif event.type == pygame.MOUSEMOTION:
                o_game.run_through_all_rects(event.pos)

            o_game.new_game_button.handleEvent(event)
            o_game.choose_time_button.handleEvent(event)
            o_game.draw(event, flag)

            o_game.quit_button.handleEvent(event)

        else:
            o_game.checkmate_window.show()

            o_game.new_game_button.handleEvent(event)
            o_game.choose_time_button.handleEvent(event)
            o_game.draw(event, flag)

            o_game.quit_button.handleEvent(event)





        # 8 - Обновляем экран
        pygame.display.update()

        # 9 - Обновляем частоту кадров
        clock.tick(FRAMES_PER_SECOND)

