# Главная программа
# 1 - Импортируем модули

import pygame
import sys
import logging

import pygwidgets

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
o_game.checkmate_window.hide()

flag = False
chosen_piece = False

def check_keys_down(event):
    global flag, chosen_piece

    if event.key == pygame.K_m:
        flag = not flag
        chosen_piece = not chosen_piece
        o_game.tossing_girl.pause()




def check_events():

    # 7 - Проверяем на наличие событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

        if o_game.game_mgr.playing and event.type == pygame.KEYDOWN:
            check_keys_down(event)

        if event.type == pygame.MOUSEMOTION:
            o_game.run_through_all_rects(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if o_game.game_mgr.playing:
                mouse_pos = pygame.mouse.get_pos()
                o_game.got_click(mouse_pos)
                o_game.cursor = pygame.mouse.get_pos()

        if o_auth.LOGIN_AWAITING_STATUS:
            o_auth.event_manager(event)
            o_auth.login_input.handleEvent(event)
            o_auth.password_input.handleEvent(event)
            o_auth.login_button.handleEvent(event)


        elif o_game.game_mgr.playing:
            o_game.new_game_button.handleEvent(event)
            o_game.choose_time_button.handleEvent(event)
            o_game.quit_button.handleEvent(event)

        else:
            o_game.new_game_button.handleEvent(event)
            o_game.choose_time_button.handleEvent(event)
            o_game.draw()

            o_game.quit_button.handleEvent(event)
            o_game.checkmate_window.show()

# 6 - Бесконечный цикл
while True:

    check_events()

    if o_auth.LOGIN_AWAITING_STATUS:
        o_auth.draw()

    elif o_game.game_mgr.playing:
        o_game.start()
        o_game.draw()
        o_game.show_developer_table(flag)


    # 8 - Обновляем экран
    pygame.display.update()

    # 9 - Обновляем частоту кадров
    clock.tick(FRAMES_PER_SECOND)

