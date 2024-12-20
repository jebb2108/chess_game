import sys

import pyghelpers
import pygwidgets
import pygame

from pygame.locals import *
from constants import *
from core_files.pixels import pixel_mapping
from visuals import ChooseTimeButton, ChessClock
from core_files.manager import Manager


class ScenePlay(pyghelpers.Scene):

    BOARD_IMAGE = pygame.image.load('images/chess_board.jpg')
    CHOSEN_RECT_IMAGE = pygame.image.load('images/cross_target.png')

    WIN_STATE = None
    CHECKMATE_STATE = False
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

        self.timer_display = pygwidgets.DisplayText(self.window, (668, 27), 'TIMER FOR EACH:', textColor=DARK_GRAY, fontSize=30)

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
        self.tossing_girl.show()
        self.tossing_girl.play()
        self.current_player = COLOR_WHITE

        default_time = self.choose_time_button.get_time()
        self.white_clock = ChessClock(self.window, (656, 50), COLOR_WHITE, default_time)
        self.black_clock = ChessClock(self.window, (760, 50), COLOR_BLACK, default_time)
        self.white_clock.start(), self.black_clock.start()
        self.black_clock.pause()

        return

    def reset(self, the_nickname):
        if the_nickname == 'new game':
            self.game_mgr.game_start_sound.play()
            del self.game_mgr
            self.game_mgr = Manager(self.window)
            ScenePlay.WIN_STATE = None
            ScenePlay.CHECKMATE_STATE = False
            return self.renew_clocks()

    def renew_clocks(self):

        # Возвращает ход белым
        self.current_player = COLOR_WHITE

        # Извлекает и обрабатывает кортеж времени
        time = self.choose_time_button.get_time()
        new_time = float(time[0] * 60)
        increase_time = time[1]

        # Останавливает таймер
        self.white_clock.stop()
        self.black_clock.stop()

        # Явно устанавливает время
        self.white_clock.set_time(new_time)
        self.black_clock.set_time(new_time)

        # Запускает часы для первого хода
        self.white_clock.start(new_time)
        self.black_clock.start(new_time)

        # Устанавливает новое значение возрастания
        self.white_clock.set_increase_time(increase_time)
        self.black_clock.set_increase_time(increase_time)

        # Ставит таймер черных на паузу
        self.black_clock.pause()

    def handleInputs(self, eventsList, keyPressedList):

        for event in eventsList:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if (event.type == MOUSEBUTTONDOWN and
                    ScenePlay.WIN_STATE not in [COLOR_WHITE, COLOR_BLACK]):
                self.cursor = event.pos
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
                rect_indx = self.board_rects.index(rect)
                coords = self.convert_selected_into_coords(rect_indx)

                if self.chosen_piece:
                    self.linked_rects_dict[rect_indx] = SELECTED

                elif self.game_mgr.get_class_as_str(coords) != 'Empty':
                    self.linked_rects_dict[rect_indx] = SELECTED

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

        if len(all_selected_keys) == 1:
            key = all_selected_keys.pop()
            if self.approve_selection(key):
                self.appoint_active_piece(key)
                return
            self.linked_rects_dict = {key: IDLE for key in self.linked_rects_dict}

        elif len(all_selected_keys) == 2:

            chosen_piece_coords = self.get_coords_of_chosen_piece(mouse_pos)
            the_other_index = \
                [num for num in all_selected_keys
                 if self.convert_selected_into_coords(num) != chosen_piece_coords][0]
            next_move_coords = self.convert_selected_into_coords(the_other_index)

            # Связанная функция с внутренним кодом для того, чтобы попытаться сходить фигурой
            self.game_mgr.initiate_move(self.chosen_piece, next_move_coords)
            self.game_mgr.promotion_getter(self.show_promotion(), next_move_coords)
            self.linked_rects_dict = {key: IDLE for key in self.linked_rects_dict}
            self.chosen_piece = None


        return

    def approve_selection(self, key):
        coords = self.convert_selected_into_coords(key)
        the_color = self.game_mgr.get_color(self.game_mgr.board, coords)
        if the_color == self.game_mgr.whose_turn_it_is.get_turn():
            return True
        self.game_mgr.illegal_sound.play()
        return False

    def shift_players_clocks(self):

        if self.current_player == COLOR_WHITE:
            self.white_clock.resume()
            self.black_clock.increase_time()
            self.black_clock.pause()
        else:
            self.black_clock.resume()
            self.white_clock.increase_time()
            self.white_clock.pause()

        return

    def get_curr_turn(self):

        """ Проверяет, произошло ли изменение в ходе """
        simple_move_dict = {1: COLOR_WHITE, 2: COLOR_BLACK}
        this_turn = self.game_mgr.whose_turn_it_is.get_turn()
        dict_interpretation_of_current_turn = simple_move_dict[this_turn]

        if dict_interpretation_of_current_turn != self.current_player:
            self.current_player = dict_interpretation_of_current_turn
            # Да, игрок сходил. Возвращает True
            return True

        # Ничего не изменилось. Возвращает False
        return False

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

        color = (COLOR_WHITE, COLOR_BLACK)[self.game_mgr.whose_turn_it_is.get_turn() - 2]

        while self.game_mgr.get_pawn_awaiting_status():

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

        if self.game_mgr.get_checkmate_status():
            ScenePlay.CHECKMATE_STATE = True

        elif self.chosen_piece:
            all_poss_moves = self.game_mgr.get_this_piece_moves(self.chosen_piece)
            self.valid_moves = []
            if self.chosen_piece.__class__.__name__ == 'King':
                additional_moves = self.game_mgr.get_kings_moves(self.chosen_piece)
                for move in additional_moves:
                    pixel_coords = pixel_mapping[move]
                    self.valid_moves.append(pixel_coords)
            for move in all_poss_moves:
                pixel_coords = pixel_mapping[move]
                self.valid_moves.append(pixel_coords)


        if (not ScenePlay.CHECKMATE_STATE and
                not ScenePlay.WIN_STATE in [COLOR_WHITE, COLOR_BLACK]):
            self.check_on_clock()
            self.tossing_girl.update()
            mouse_pos = pygame.mouse.get_pos()
            self.run_through_all_rects(mouse_pos)

            # Обновление хода
            if self.get_curr_turn():
                self.shift_players_clocks()

            if self.black_clock.ended():
                ScenePlay.WIN_STATE = COLOR_WHITE
                self.white_clock.pause()

            elif self.white_clock.ended():
                ScenePlay.WIN_STATE = COLOR_BLACK
                self.black_clock.pause()
            return

        self.tossing_girl.pause()
        ScenePlay.DEVELOPER_TOOL_ACTIVE = False
        return

    def check_on_clock(self):
        self.black_clock.set_color()
        self.white_clock.set_color()
        return

    def show_developer_table(self):
        if ScenePlay.DEVELOPER_TOOL_ACTIVE:
            # message: 4
            pygame.draw.rect(self.window, LIGHT_GRAY, [630, 20, 650, 600])
            selected_info_text = f'Number of'
            selected_img = self.font.render(selected_info_text, True, DARK_GRAY)
            self.window.blit(selected_img, (650, 270))
            selected_info_text = f'selected: {[tile for tile in self.linked_rects_dict.values()].count(SELECTED)}'
            selected_img = self.font.render(selected_info_text, True, DARK_GRAY)
            self.window.blit(selected_img, (650, 300))


            # Message: 1
            whose_turn_in_num = self.game_mgr.whose_turn_it_is.current_move
            text = f'Whose turn:'
            text_img = self.font.render(text, True, DARK_GRAY)
            self.window.blit(text_img, (650, 50))
            text = f' --> {('white', 'black')[whose_turn_in_num - 1]} <--'
            text_img = self.font.render(text, True, DARK_GRAY)
            self.window.blit(text_img, (650, 80))

            # message: 5
            text_img = self.font.render(f'Player: {self.current_player}', True, DARK_GRAY)
            self.window.blit(text_img, (650, 350))

            # Message: 3
            mouse_pos_text = f'Cursor loc:'
            cursor_img = self.font.render(mouse_pos_text, True, DARK_GRAY)
            self.window.blit(cursor_img, (650, 200))
            mouse_pos_text = f'{self.cursor}'
            cursor_img = self.font.render(mouse_pos_text, True, DARK_GRAY)
            self.window.blit(cursor_img, (650, 230))

            # Message: 2.1
            if issubclass(type(self.chosen_piece), self.game_mgr.settings.class_mapping['Piece']):
                class_name = self.chosen_piece.__class__.__name__
                its_loc = self.chosen_piece.loc
                text = f'There is {class_name}.'
                text_img = self.font.render(text, True, DARK_GRAY)
                self.window.blit(text_img, (650, 120))
                text= f'Its loc: {its_loc}'
                text_img = self.font.render(text, True, DARK_GRAY)
                self.window.blit(text_img, (650, 150))

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

        self.black_clock.draw()
        self.white_clock.draw()
        self.timer_display.draw()

        self.show_developer_table()
        self.show_tiles()

        if self.chosen_piece:
            main_rect = pixel_mapping[self.chosen_piece.loc]
            # pygame.draw.rect(self.window, BLACK, main_rect, 3)
            self.window.blit(ScenePlay.CHOSEN_RECT_IMAGE, [main_rect[0]-5, main_rect[1]-5])
            for rect in self.valid_moves:
                rect_center = [rect[0] + 29, rect[1] + 29]
                pygame.draw.circle(self.window, DARK_GRAY, rect_center, 5)

        self.attach_pieces_to_board()

        if ScenePlay.WIN_STATE in [COLOR_WHITE, COLOR_BLACK]:
            pygame.draw.rect(self.window, LIGHT_GRAY, (196, 260, 314, 120), 0)
            pygame.draw.rect(self.window, BLACK, (196, 260, 314, 120), 4)
            self.checkmate_window.setValue('White wins!' if ScenePlay.WIN_STATE == COLOR_WHITE else 'Black wins!')
            self.checkmate_window.draw()


        elif ScenePlay.CHECKMATE_STATE:
            pygame.draw.rect(self.window, LIGHT_GRAY, (196, 260, 314, 120), 0)
            pygame.draw.rect(self.window, BLACK, (196, 260, 314, 120), 4)
            self.checkmate_window.draw()

    def leave(self):
        self.window.fill(BLACK)
        self.choose_time_button.set_default_time()

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
