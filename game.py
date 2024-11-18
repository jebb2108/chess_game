# Класс Game
import pygwidgets

from core_files.manager import Manager
from buttons import ChooseTimeButton
from authorization import Authorization
from constants import *


class Game:
    BACKGROUND_IMAGE = pygame.image.load('images/background.png')
    BOARD_IMAGE = pygame.image.load('images/chess_board.jpg')

    def __init__(self, window):

        self.window = window

        self.game_mgr = Manager(window)

        self.font = pygame.font.Font(None, 40)

        self.new_game_button = pygwidgets.TextButton(self.window, (20, 640), 'NEW GAME', width=180, height=45,
                                                     fontSize=22, callBack=self.reset)

        self.choose_time_button = ChooseTimeButton(self.window, (230, 640), '', width=180, height=45, fontSize=22)

        self.profile_button = pygwidgets.TextButton(self.window, (440, 640), 'PROFILE', width=180, height=45,
                                                    fontSize=22)

        self.quit_button = pygwidgets.TextButton(self.window, (745, 640), 'QUIT', width=100, height=45, fontSize=22,
                                                 callBack=self.exit)

        self.checkmate_window = pygwidgets.DisplayText(self.window, (250, 305), 'CHECKMATE', textColor=(200, 0, 0),
                                                       fontSize=50)

        self.buttons = [self.new_game_button, self.choose_time_button, self.profile_button, self.quit_button]

        self.board = Game.BOARD_IMAGE
        self.board_rect = self.board.get_rect()
        self.board_rect.top, self.board_rect.left = 20, 20

        self.board_rects = self.create_rects()
        self.linked_rects_dict = dict().fromkeys(range(64), IDLE)

        self.chosen_piece = None
        self.cursor = None

    def reset(self, callBack):
        pass

    def got_click(self, mouse_pos):
        for rect in self.board_rects:
            if rect.collidepoint(mouse_pos):
                rect_int = self.board_rects.index(rect)
                coords = self.convert_selected_into_coords(rect_int)

                if self.chosen_piece:
                    self.linked_rects_dict[rect_int] = SELECTED

                elif self.game_mgr.get_class_as_str(coords) != 'Empty':
                    self.linked_rects_dict[rect_int] = SELECTED



        return self.check_selected(mouse_pos)

    def run_through_all_rects(self, mouse_pos):
        # Отслеживает состояние всех
        # клеток: IDLE, HOVER, SELECTED
        for rect in self.board_rects:
            key = self.board_rects.index(rect)

            if rect.collidepoint(mouse_pos) and self.linked_rects_dict[key] in [IDLE, HOVER]:
                self.linked_rects_dict[key] = HOVER

            else:

                if self.linked_rects_dict[key] == HOVER:
                    self.linked_rects_dict[key] = IDLE

        return

    def check_selected(self, mouse_pos):
        all_selected_keys = [key for key, value in
                             self.linked_rects_dict.items() if value == SELECTED]

        if 0 < len(all_selected_keys) < 2:
            key = all_selected_keys[0]
            self.appoint_active_piece(key)

        elif len(all_selected_keys) == 2:

            chosen_piece_coords = self.get_coords_of_chosen_piece(mouse_pos)
            the_other_index = \
            [num for num in all_selected_keys
             if self.convert_selected_into_coords(num) != chosen_piece_coords][0]
            next_move_coords = self.convert_selected_into_coords(the_other_index)

            # Связанная функция с базовым классом для того, чтобы попытаться сходить фигурой
            self.game_mgr.initiate_move(self.chosen_piece, next_move_coords)
            self.linked_rects_dict = {key: IDLE for key in self.linked_rects_dict}
            self.chosen_piece = None

        return

    def get_coords_of_chosen_piece(self, mouse_pos) -> tuple:
        try:
            coords = self.chosen_piece.loc
        except AttributeError:
            coords = [self.convert_selected_into_coords(self.board_rects.index(rect))
                      for rect in self.board_rects if rect.collidepoint(mouse_pos)]
            return tuple(coords)
        else:
            return tuple(coords)

    def appoint_active_piece(self, key_indx):
        try:
            res = self.convert_selected_into_coords(key_indx)
        except TypeError:
            return
        else:
            coord_y, coord_x = res
            self.chosen_piece = self.game_mgr.board[coord_y][coord_x]

    @staticmethod
    def convert_selected_into_coords(key):
        coords = [key // 8, key % 8]
        return tuple(coords)

    def show_tiles(self, flag):
        if flag:
            pygame.draw.rect(self.window, RED, (50, 50, 540, 540), 5)
            for rect in self.board_rects:
                pygame.draw.rect(self.window, GREEN, [rect.left, rect.top, rect.width, rect.height], 2)
                if self.linked_rects_dict[self.board_rects.index(rect)] in [SELECTED, HOVER]:
                    pygame.draw.rect(self.window, GREEN, [rect.left, rect.top, rect.width, rect.height], 10)

        return None

    def show_developer_table(self, event, flag):
        if flag:
            # message: 4
            pygame.draw.rect(self.window, LIGHT_GRAY, [630, 20, 650, 600])
            selected_info_text = f'Number of\nselected: {[tile for tile in self.linked_rects_dict.values()].count(SELECTED)}'
            cursor_img = self.font.render(selected_info_text, True, DARK_GRAY)
            self.window.blit(cursor_img, (650, 270))

            # Message: 1
            whose_turn_in_num = self.game_mgr.whose_turn_it_is.current_move
            text = f'Whose turn:\n--> {('white', 'black')[whose_turn_in_num-1]} <--'
            text_img = self.font.render(text, True, DARK_GRAY)
            self.window.blit(text_img, (650, 50))

            # message: 5
            if self.game_mgr.default_message:
                # text_img = self.font.render('message:\n' + self.game_mgr.default_message, True, DARK_GRAY)
                text_img = self.font.render(f'Pieces in total: {len(self.game_mgr.all_poss_moves)}', True, DARK_GRAY)
                self.window.blit(text_img, (650, 350))

            # Message: 3
            if self.cursor or event.type == pygame.MOUSEBUTTONDOWN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.cursor = event.pos
                mouse_pos_text = f'Cursor loc:\n{self.cursor}'
                cursor_img = self.font.render(mouse_pos_text, True, DARK_GRAY)
                self.window.blit(cursor_img, (650, 200))

            # Message: 2.1
            if issubclass(type(self.chosen_piece), self.game_mgr.settings.class_mapping['Piece']):
                class_name = self.chosen_piece.__class__.__name__
                its_loc = self.chosen_piece.loc
                text = f'There is {class_name}.\nIts loc: {its_loc}'
                text_img = self.font.render(text, True, DARK_GRAY)
                self.window.blit(text_img, (650, 120))

            # Message: 2.2
            else:
                text = 'NO PIECE'
                text_img = self.font.render(text, True, DARK_GRAY)
                self.window.blit(text_img, (650, 120))



    def attach_pieces_to_board(self):
        for piece in self.game_mgr.all_poss_moves:
            piece.draw()

    def draw(self, event, flag=False):
        if flag is False:
            flag = False
        self.window.fill(LIGHT_GRAY)
        for button in self.buttons:
            button.draw()
        self.window.blit(self.board, self.board_rect)
        self.show_tiles(flag)
        self.show_developer_table(event, flag)
        self.attach_pieces_to_board()

        if self.checkmate_window.visible:
            pygame.draw.rect(self.window, LIGHT_GRAY, (196, 260, 314, 120), 0)
            pygame.draw.rect(self.window, BLACK, (196, 260, 314, 120), 4)
            self.checkmate_window.draw()

    def exit(self, CallBack):
        self.playing = True
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
                single_rect = pygame.Rect(width_adjustment, top_border + height_adjustment, 55, 55)
                rects_list.append(single_rect)

            height_adjustment += 55 + offset_xy

        return rects_list
