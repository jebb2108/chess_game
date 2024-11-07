# Класс Game

import pygame
import pygwidgets

from board import Board, Piece
from settings import Settings
from buttons import ChooseTimeButton
from authorization import Authorization
from constants import *


# class LoginData(Authorization):
#
#     def __init__(self, window):
#         super().__init__(window)
#         self.name = self.login_input
#         self.password = self.password_input


class Game:

    BACKGROUND_IMAGE = pygame.image.load('images/background.png')
    BOARD_IMAGE = pygame.image.load('images/chess_board.jpg')

    def __init__(self, window):

        self.window = window

        self.board_inst = Board(window)

        self.font = pygame.font.Font(None, 40)

        self.new_game_button = pygwidgets.TextButton(self.window, (20, 640), 'NEW GAME', width=180, height=45, fontSize=22)

        self.choose_time_button = ChooseTimeButton(self.window, (230, 640), '', width=180, height=45, fontSize=22)

        self.profile_button = pygwidgets.TextButton(self.window, (440, 640), 'PROFILE', width=180, height=45, fontSize=22)

        self.quit_button = pygwidgets.TextButton(self.window, (745, 640), 'QUIT', width=100, height=45, fontSize=22,
                                                 callBack=self.exit)

        self.buttons = [self.new_game_button, self.choose_time_button, self.profile_button, self.quit_button]

        self.board = Game.BOARD_IMAGE
        self.board_rect = self.board.get_rect()
        self.board_rect.top, self.board_rect.left = 20, 20

        self.board_rects = self.create_rects()
        self.linked_rects_dict = dict().fromkeys(range(64), IDLE)

        self.chosen_piece = None

        self.cursor = None

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


        comprehension = [key for key, value in self.linked_rects_dict.items() if value == SELECTED]
        for key, value in self.linked_rects_dict.items():
            if value == SELECTED:

                if len(comprehension) == 1:
                    self.appoint_active_piece(key)

                elif len(comprehension) > 1:

                    # Связанная функция с базовым классом для того, чтобы попытаться сходить фигурой
                    # self.attempt_piece_to_move(self.chosen_piece, key)

                    self.chosen_piece = None
                    for item in list(comprehension):
                        self.linked_rects_dict[item] = IDLE




            if value == HOVER and not (self.board_rects[key].collidepoint(pygame.mouse.get_pos())):
                self.linked_rects_dict[key] = IDLE

        return



    def appoint_active_piece(self, key_indx):
        try:
            res = self.convert_selected_into_coord(key_indx)
        except TypeError:
            return False
        else:
            coord_y, coord_x = res
            self.chosen_piece = self.board_inst.board[coord_y][coord_x]
            return True


    @staticmethod
    def convert_selected_into_coord(key):
        coords = (key // 8, key % 8)
        return coords

    def attach_pieces_to_board(self):
        for piece in self.board_inst.all_pieces:
            coords = piece.loc
            pixel_coords = Settings.pixel_mapping[coords]
            self.window.blit(piece.image, pixel_coords)


    def show_tiles(self, flag):
        if flag:
            pygame.draw.rect(self.window, RED, (50, 50, 540, 540), 5)
            for rect in self.board_rects:
                pygame.draw.rect(self.window, GREEN, [rect.left, rect.top, rect.width, rect.height], 2)
                if self.linked_rects_dict[self.board_rects.index(rect)] in [SELECTED, HOVER]:
                    pygame.draw.rect(self.window, GREEN, [rect.left, rect.top, rect.width, rect.height], 10)

        return None

    def exit(self, CallBack):
        Authorization.LOGIN_AWAITING_STATUS = True
        self.window.fill(BLACK)

    @staticmethod
    def create_rects():
        rects_list = []
        offset_xy = 10
        left_border, top_border = 50 + 15, 50 + 15
        height_adjustment = 0
        for _ in range(1, 9):
            width_adjustment = 0

            for _ in range(8):
                width_adjustment += 55 + offset_xy
                # if len(rects_list) != 64:
                single_rect = pygame.Rect(width_adjustment, top_border + height_adjustment, 55, 55)
                rects_list.append(single_rect)

            height_adjustment += 55 + offset_xy

        return rects_list

    # def generate_board_rects(self):
    #     pixel_rect_ls = {}
    #     for rect in self.board_rects:
    #         value = self.board_rects.index(rect)
    #         formated_key = (value // 8, value % 8)
    #         pixel_rect_ls[formated_key] = [rect.left, rect.top]
    #
    #     with open('pixel_rect_ls.txt', 'w') as f:
    #         f.write(r'pixel_mapping = {'f'\n')
    #         for coords, pixel in pixel_rect_ls.items():
    #             f.write(f'\t{coords}: {pixel},\n')
    #         f.write('}\n')
    #
    #     return print(pixel_rect_ls)

    def show_active_piece(self, event, flag):
        if flag:
            pygame.draw.rect(self.window, LIGHT_GRAY, [630, 20, 650, 600])
            if self.cursor or event.type == pygame.MOUSEBUTTONDOWN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.cursor = event.pos
                mouse_pos_text = f'Cursor loc:\n{self.cursor}'
                cursor_img = self.font.render(mouse_pos_text, True, DARK_GRAY)
                self.window.blit(cursor_img, (650, 120))

            if issubclass(type(self.chosen_piece), Piece):
                class_name = self.chosen_piece.__class__.__name__
                its_loc = self.chosen_piece.get_loc()
                text = f'There is {class_name}.\nIts loc: {its_loc}'

            else:
                text = 'NO PIECE'

            text_img = self.font.render(text, True, DARK_GRAY)
            self.window.blit(text_img, (650, 50))


    def draw(self, event, flag=False):
        if flag is False:
            flag = False
        self.window.fill(LIGHT_GRAY)
        for button in self.buttons:
            button.draw()
        self.window.blit(self.board, self.board_rect)
        self.show_tiles(flag)
        self.show_active_piece(event, flag)
        self.attach_pieces_to_board()
        # self.generate_board_rects()



