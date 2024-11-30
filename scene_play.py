import sys

import pyghelpers
import pygwidgets
import pygame

from pygame.locals import *
from constants import *
from buttons import ChooseTimeButton, ChessClock
from core_files.manager import Manager


class ScenePlay(pyghelpers.Scene):

    BOARD_IMAGE = pygame.image.load('images/chess_board.jpg')

    DEVELOPER_TOOL_ACTIVE = False

    def __init__(self, window):
        self.window = window

        self.game_mgr = Manager(window)

        self.font = pygame.font.Font(None, 40)

        self.tossing_girl = pygwidgets.Animation(window, (550, 100), tossing_girl_list, autoStart=False, loop=True)

        self.new_game_button = pygwidgets.TextButton(self.window, (20, 640), 'NEW GAME', width=180, height=45,
                                                     fontSize=22, callBack=self.reset, nickname='new game')

        self.choose_time_button = ChooseTimeButton(self.window, (230, 640), '', width=180, height=45, fontSize=22)

        self.profile_button = pygwidgets.TextButton(self.window, (440, 640), 'PROFILE', width=180, height=45,
                                                    fontSize=22)

        self.quit_button = pygwidgets.TextButton(self.window, (745, 640), 'QUIT', width=100, height=45, fontSize=22)

        self.checkmate_window = pygwidgets.DisplayText(self.window, (250, 305), 'CHECKMATE', textColor=(200, 0, 0),
                                                       fontSize=50)

        self.buttons = [self.new_game_button, self.choose_time_button, self.profile_button, self.quit_button]

        self.white_clock = ChessClock(self.window, (656, 50), COLOR_WHITE, self.choose_time_button.get_time())
        self.black_clock = ChessClock(self.window, (760, 50), COLOR_BLACK, self.choose_time_button.get_time())

        # self.black_timer_clock = pygwidgets.DisplayText(self.window, (700, 50), '', textColor=DARK_GRAY, fontSize=50)
        # self.white_timer_clock = pygwidgets.DisplayText(self.window, (800, 50), '', textColor=DARK_GRAY, fontSize=50)

        knight_collection = pygwidgets.ImageCollection(self.window, (200, 264),
                                                       {COLOR_WHITE: 'white_Knight.png',
                                                        COLOR_BLACK: 'black_Knight.png'},
                                                       COLOR_WHITE, path='images/')
        bishop_collection = pygwidgets.ImageCollection(self.window, (260, 264),
                                                       {COLOR_WHITE: 'white_Bishop.png',
                                                        COLOR_BLACK: 'black_Bishop.png'},
                                                       COLOR_WHITE, path='images/')
        rock_collection = pygwidgets.ImageCollection(self.window, (200, 319),
                                                     {COLOR_WHITE: 'white_Rock.png', COLOR_BLACK: 'black_Rock.png'},
                                                     COLOR_WHITE, path='images/')
        queen_collection = pygwidgets.ImageCollection(self.window, (260, 319),
                                                      {COLOR_WHITE: 'white_Queen.png', COLOR_BLACK: 'black_Queen.png'},
                                                      COLOR_WHITE, path='images/')
        self.all_four_collections_list = [
            knight_collection, bishop_collection,
            rock_collection, queen_collection
        ]

        self.board = ScenePlay.BOARD_IMAGE
        self.board_rect = self.board.get_rect()
        self.board_rect.top, self.board_rect.left = 20, 20

        self.board_rects = self.create_rects()
        self.linked_rects_dict = dict().fromkeys(range(64), IDLE)

        self.checkmate_status = False
        self.chosen_piece = None
        self.cursor = None

        self.pressed_keys = set()

    def getSceneKey(self):
        return SCENE_PLAY

    def enter(self, data):
        self.game_mgr.game_start_sound.play()
        self.tossing_girl.show()
        self.tossing_girl.start()
        return self.reset(the_nickname='new game')

    def reset(self, the_nickname):
        if the_nickname == 'new game':
            del self.game_mgr
            self.game_mgr = Manager(self.window)
            self.tossing_girl.play()

        return

    def handleInputs(self, eventsList, keyPressedList):
        for event in eventsList:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                self.got_click(event.pos)


            if self.quit_button.handleEvent(event):
                self.goToScene(SCENE_AUTH)

            self.new_game_button.handleEvent(event)
            self.choose_time_button.handleEvent(event)
            self.profile_button.handleEvent(event)

        if keyPressedList[pygame.K_m] and pygame.K_m not in self.pressed_keys:
            ScenePlay.DEVELOPER_TOOL_ACTIVE = not ScenePlay.DEVELOPER_TOOL_ACTIVE
            self.pressed_keys.add(pygame.K_m)
            self.tossing_girl.pause()



        return self.check_keys_down()

    def check_keys_down(self):
        key_pressed = pygame.key.get_pressed()
        if True in key_pressed:
            return
        else:
            self.pressed_keys.clear()

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
            self.game_mgr.promotion_getter(self.show_promotion(), next_move_coords)
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

    def show_promotion(self):

        o_knight = self.game_mgr.settings.class_mapping['Knight']
        o_bishop = self.game_mgr.settings.class_mapping['Bishop']
        o_rook = self.game_mgr.settings.class_mapping['Rock']
        o_queen = self.game_mgr.settings.class_mapping['Queen']

        color = (COLOR_WHITE, COLOR_BLACK)[self.game_mgr.whose_turn_it_is.current_move - 2]

        while self.game_mgr.pawn_awaiting:

            for collection in self.all_four_collections_list:
                collection.replace(color)

            pygame.draw.rect(self.window, WHITE, [196, 260, 118, 118], 0)
            self.all_four_collections_list[0].draw()
            self.all_four_collections_list[1].draw()
            self.all_four_collections_list[2].draw()
            self.all_four_collections_list[3].draw()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[0] in range(200, 500) and event.pos[1] in range(260, 420):

                        if (event.pos[0] in range(200, 255) and
                                event.pos[1] in range(260, 315)):
                            self.game_mgr.turn_pawn_into_piece = False
                            return o_knight

                        elif (event.pos[0] in range(260, 315) and
                              event.pos[1] in range(260, 315)):
                            self.game_mgr.turn_pawn_into_piece = False
                            return o_bishop

                        elif (event.pos[0] in range(200, 255) and
                              event.pos[1] in range(319, 374)):
                            self.game_mgr.turn_pawn_into_piece = False
                            return o_rook

                        elif (event.pos[0] in range(260, 315) and
                              event.pos[1] in range(319, 374)):
                            self.game_mgr.turn_pawn_into_piece = False
                            return o_queen

        return None

    def update(self):

        current_turn = COLOR_BLACK if self.game_mgr.whose_turn_it_is.get_turn() == 1 else COLOR_WHITE

        self.black_clock.update(current_turn)
        self.white_clock.update(current_turn)

        if not self.game_mgr.checkmate:
            # self.check_on_clock()
            self.tossing_girl.update()
            mouse_pos = pygame.mouse.get_pos()
            self.run_through_all_rects(mouse_pos)
            return

        self.tossing_girl.pause()
        ScenePlay.DEVELOPER_TOOL_ACTIVE = False
        return

    def check_on_clock(self):

        return

    def show_developer_table(self):
        if ScenePlay.DEVELOPER_TOOL_ACTIVE:
            # message: 4
            pygame.draw.rect(self.window, LIGHT_GRAY, [630, 20, 650, 600])
            selected_info_text = f'Number of\nselected: {[tile for tile in self.linked_rects_dict.values()].count(SELECTED)}'
            cursor_img = self.font.render(selected_info_text, True, DARK_GRAY)
            self.window.blit(cursor_img, (650, 270))

            # Message: 1
            whose_turn_in_num = self.game_mgr.whose_turn_it_is.current_move
            text = f'Whose turn:\n--> {('white', 'black')[whose_turn_in_num - 1]} <--'
            text_img = self.font.render(text, True, DARK_GRAY)
            self.window.blit(text_img, (650, 50))

            # message: 5
            if self.game_mgr.default_message:
                # text_img = self.font.render('message:\n' + self.game_mgr.default_message, True, DARK_GRAY)
                text_img = self.font.render(f'Pieces in total: {len(self.game_mgr.all_poss_moves)}', True,
                                            DARK_GRAY)
                self.window.blit(text_img, (650, 350))

            # Message: 3
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

        return self.show_tiles()

    def show_tiles(self):
        if ScenePlay.DEVELOPER_TOOL_ACTIVE:
            pygame.draw.rect(self.window, RED, (50, 50, 540, 540), 5)
            for rect in self.board_rects:
                pygame.draw.rect(self.window, GREEN, [rect.left, rect.top, rect.width, rect.height], 2)
                if self.linked_rects_dict[self.board_rects.index(rect)] in [SELECTED, HOVER]:
                    pygame.draw.rect(self.window, GREEN, [rect.left, rect.top, rect.width, rect.height], 10)
        else:
            self.tossing_girl.start()

        return

    def attach_pieces_to_board(self):
        for piece in self.game_mgr.all_poss_moves:
            piece.draw()

    def draw(self):
        self.window.fill(LIGHT_GRAY)

        self.tossing_girl.draw()

        for button in self.buttons:
            button.draw()
        self.window.blit(self.board, self.board_rect)

        self.show_developer_table()
        self.show_tiles()

        self.attach_pieces_to_board()

        self.black_clock.draw()
        self.white_clock.draw()

        if self.game_mgr.checkmate:
            pygame.draw.rect(self.window, LIGHT_GRAY, (196, 260, 314, 120), 0)
            pygame.draw.rect(self.window, BLACK, (196, 260, 314, 120), 4)
            self.checkmate_window.draw()

    def leave(self):
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

    @staticmethod
    def convert_selected_into_coords(key):
        coords = [key // 8, key % 8]
        return tuple(coords)
