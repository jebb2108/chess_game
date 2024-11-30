import copy
import pygame
from core_files.board import BoardUser

class WhoMoves(object):
    """ Класс, который следит за очередностью ходов белых и черных. """

    def __init__(self):
        # 1 олицетворяет белые фигуры, а -1 черные.
        self.turn = 1
        # Текущий ход.
        self.current_move = 1

    def change_turn(self):
        self.turn *= -1
        # Отдельный атрибут 'current_move' помогает выводить два значения 1 и 2,
        # где в изначальном виде интерпретируются цвета фигуры, что помогает в дальнейших
        # условиях сравнений.
        self.current_move = 1 if self.turn == 1 else 2

class Manager(BoardUser):
    """ Класс самого высокого уровня,
    с чем непосредственно взаимодействует пользователь. """

    sounds_loaded = False

    game_start_sound = None
    game_end_sound = None
    move_check_sound = None

    def __init__(self, window, board_ls=None):
        self.window = window
        self.whose_turn_it_is = WhoMoves()
        self.default_message = None
        self.object_copies = list()

        if not Manager.sounds_loaded:
            Manager.game_start_sound = pygame.mixer.Sound('sounds/game-start.mp3')
            Manager.game_end_sound = pygame.mixer.Sound('sounds/game-end.mp3')
            Manager.move_check_sound = pygame.mixer.Sound('sounds/move-check.mp3')
            Manager.sounds_loaded = True


        super().__init__(window, board_ls)

        self.game_start_sound_state = True
        self.pawn_awaiting = False
        self.checkmate = False

    def promotion_getter(self, piece, dest: tuple):
        if self.pawn_awaiting:
            its_y, its_x = dest
            color = 1 if its_y == 0 else 2
            self.board[its_y][its_x] = self.settings.class_mapping['Empty']()
            new_piece = piece(self.window, dest, color)
            self.board[its_y][its_x] = new_piece

            self.all_poss_moves[new_piece] = new_piece._get_all_moves(self.board)
            self.pawn_awaiting = False

        return

    def initiate_move(self, piece: object, to_where: tuple):

        if self.checkmate: return

        # Три важных действия
        self.update_sound_states()
        self.chosen_piece_object = piece
        # current_board = self.copy_board()

        # Проверяет, если это король и запрашивается рокировка.
        # if self.chosen_piece_class == 'class.King':
        if self.check_castling_and_move(to_where):

            # if not self.is_end_game():
            #     self.play_sound(False)

            self.whose_turn_it_is.change_turn()
            self.update_all_poss_moves_dict()
            self.castling_sound_state = True

            return

        # Следующее условие. Это не король. Совершает обычный ход
        elif self.identify_whether_move_is_legal(to_where):
            if self.chosen_piece_class == 'class.Pawn' and self.check_pawn_at_edge(to_where):
                del self.all_poss_moves[self.chosen_piece_object]
                self.pawn_awaiting = True

            # if not self.is_end_game():
            #     self.play_sound(False)

            self.whose_turn_it_is.change_turn()
            self.update_all_poss_moves_dict()

            return

        self.update_all_poss_moves_dict()
        self.chosen_piece_object = None
        return self.play_sound(True)

    def is_end_game(self):

        """ Метод, который активируется в случае шаха собственному королю,
            сделанному оппонентом на предыдущем ходе """

        checkmate_status = False
        if self.is_checked(True):
            checkmate_status = True

        # выполнит всевозможные ходы для проверки,
        # если поставлен мат и это конец игры
        while checkmate_status:

            # Тут мне нужно сохранить состояние доски
            # res = self.copy_board()

            enemy_color_index = self.chosen_piece_object.enemy_color
            enemy_moves_n_pieces = [(key, key.access_all_moves()) for key
                                    in self.all_poss_moves if key.get_color() == enemy_color_index]

            for piece, moves in enemy_moves_n_pieces:

                # Координаты выбранной фигуры до перестановки
                curr_pos = tuple([piece.get_y(), piece.get_x()])

                for new_move in moves:
                    # Функция, которая изменяет доску в новом экземпляре.
                    eaten_piece = self.conduct_change(new_move, curr_pos)
                    # Обновляет возможные ходы в словаре после перестановки
                    self.update_all_poss_moves_dict()

                    res = self.print_board()
                    print(res)

                    if self.is_checked():
                        self.conduct_force_change(new_move, curr_pos, eaten_piece)
                        self.update_all_poss_moves_dict()

                    else:
                        self.conduct_force_change(new_move, curr_pos, eaten_piece)
                        self.update_all_poss_moves_dict()
                        Manager.move_check_sound.play()
                        checkmate_status = False
                        break

                if checkmate_status is False:
                    break


            if checkmate_status is True:
                self.checkmate = True
                Manager.game_end_sound.play()
                return True

            return False

    def identify_whether_move_is_legal(self, to_where) -> bool:
        """ Важный метод для проверки легитимности хода. """
        # Проверяет, кому принадлежит ход.
        if self.whose_turn_it_is.current_move != self.chosen_piece_color:
            return False

        curr_loc = copy.copy(self.chosen_piece_object.loc)

        # 1 - Проверяет, если фигура находится под шахом.
        if self.is_checked():
            if self.place_piece_on_board(to_where):
                # Если так, то проверяет,
                # если сделанный ход вывел короля из под него.
                if self.is_checked():
                    # Возврат доски в исходное состояние
                    self.conduct_force_change(to_where, curr_loc)
                    self.update_all_poss_moves_dict()
                    return False
                self.update_all_poss_moves_dict()
                return True
            # Ход сделать невозможно по другой причине
            self.update_all_poss_moves_dict()
            return False

        # 2 - Проверяет, если сделанный ход привел к шаху.
        elif self.place_piece_on_board(to_where):
            if self.is_checked():
                # Возврат доски в исходное состояние
                self.conduct_force_change(to_where, curr_loc)
                self.update_all_poss_moves_dict()
                return False
            self.update_all_poss_moves_dict()
            return True

        raise Exception("Something went wrong")

    def is_checked(self, enemy_check=False) -> [True or False]:
        """ Проверка, если король находится в зоне атаки вражеской фигуры. """

        color_indx = self.chosen_piece_color
        enemy_color = self.chosen_piece_object.enemy_color


        if enemy_check:
            color_indx = self.chosen_piece_object.enemy_color
            enemy_color = self.chosen_piece_color


        # Функция определяет сначала цвет выбранной фигуры,
        # а потом вражеский цвет.
        # Таким образом подбираются значения для каждого действия
        # и может определить находится ли этот король в зоне атаки
        # вражеской фигуры.
        either_king = next((key for key in self.all_poss_moves if key.color == color_indx and isinstance(key, self.settings.class_mapping['King'])), None)

        # Возвращает True или False в зависимости от того,
        # находится ли король в зоне атаки.
        return either_king.safe_zone in set(sum([value for key, value in self.all_poss_moves.items() if key.color == enemy_color], []))

    def place_piece_on_board(self, to_where):

        """ Предпоследнее действие - пробное совершение хода.
            Эта функция так же является проверочной. """

        # создает переменную со съеденной фигурой, чтобы была
        # возомжность ее вернуть с функцией conduct_force_change
        eaten_piece = self.attempt_piece_to_move(to_where)
        self.move_sound_state = True

        # Если результат отрицательный,
        # происходит выброс из цикла действий.
        if eaten_piece is False: return False

        if type(eaten_piece) is not bool:
            # Иначе проверяет, есть ли другое значение от булевых?
            # removed_piece = eaten_piece
            # Перемещает экземпляр во временное хранилище - список.
            self.object_copies.append(eaten_piece)
            self.capture_sound_state = True

        return True

    def play_sound(self, flag: bool):

        if flag:
            piece_class = self.settings.class_mapping['Piece']
            piece_class.illegal_sound.play()
            return self.update_sound_states()


        elif self.end_game_sound_state:
            Manager.game_end_sound.play()
            self.update_sound_states()

        elif self.castling_sound_state and not self.move_sound_state:
            self.chosen_piece_object.castling_sound.play()

        elif self.move_sound_state and not self.capture_sound_state:
            self.chosen_piece_object.move_sound.play()

        elif self.capture_sound_state and not self.illegal_sound_state:
            self.chosen_piece_object.capture_sound.play()

        elif self.illegal_sound_state:
            piece_class = self.settings.class_mapping['Piece']
            piece_class.illegal_sound.play()

        return self.update_sound_states()

    def update_sound_states(self):
        self.illegal_sound_state = False
        self.move_sound_state = False
        self.capture_sound_state = False
        self.castling_sound_state = False
        self.check_move_sound_state = False
        self.end_game_sound_state = False
        return

    def make_msg(self, msg):
        self.default_message = msg

    def copy_board(self):
        current_state = copy.copy(self.board)
        return current_state