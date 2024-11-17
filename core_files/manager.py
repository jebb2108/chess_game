import copy
import sys

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
        self.object_copies = list()

        if not Manager.sounds_loaded:
            Manager.game_start_sound = pygame.mixer.Sound('sounds/game-start.mp3')
            Manager.game_end_sound = pygame.mixer.Sound('sounds/game-end.mp3')
            Manager.move_check_sound = pygame.mixer.Sound('sounds/move-check.mp3')
            Manager.sounds_loaded = True

        super().__init__(window, board_ls)

        self.playing = True


    def initiate_move(self, piece, to_where):

        self.chosen_piece_object = piece
        # Проверяет, если это король и запрашивается рокировка.
        if self.chosen_piece_class == 'class.King':
            if self.check_castling_and_move(to_where):
                self.whose_turn_it_is.change_turn()
                # self.make_msg('Castling your king went successful')
                self.update_all_poss_moves_dict(self.all_poss_moves)
                return self.is_end_game()
            else:
                # self.make_msg('Castling your king went unsuccessful')
                self.update_all_poss_moves_dict()
                return self.is_end_game()

        # Следующее условие. Это не король. Совершает обычный ход
        elif self.identify_whether_move_is_legal(to_where):
            # Требуется убрать проверки т.к они уже сделаны в check_king функциях
            self.whose_turn_it_is.change_turn()
            self.update_all_poss_moves_dict()
            self.chosen_piece_object.move_sound.play()
            return self.is_end_game()

        else:
            return self.chosen_piece_object.illegal_sound.play()

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
            current_state = copy.deepcopy(self.board)

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

                    if self.is_checked():
                        self.conduct_force_change(new_move, curr_pos, eaten_piece)

                    else:
                        self.conduct_force_change(new_move, curr_pos, eaten_piece)
                        self.update_all_poss_moves_dict()
                        Manager.move_check_sound.play()
                        checkmate_status = False


            self.board = current_state
            if checkmate_status is True:
                Manager.game_end_sound.play()
                self.playing = False
                break

    def identify_whether_move_is_legal(self, to_where: list) -> bool:
        """ Важный метод для проверки шаха королю. """
        # Проверяет, кому принадлежит ход.
        if self.whose_turn_it_is.current_move != self.chosen_piece_color:
            # self.make_msg('This isn`t your turn')
            return False

        """ Должно выполняться два этапа проверки: 
        1 - проверяет, может ли фигура пойти в настоящий момент времени,
        2 - проверяет, если сделанный ход привел к шаху ИЛИ ушел из под него."""

        # 1 - Проверяет, может ли фигура пойти в
        # настоящий момент времени.
        if not self.is_checked():

            # Фигура может переместиться и обновиться словарик ходов.
            if (self.place_piece_on_board(to_where)
                    and self.post_check_king(to_where)):

                # success!
                return True
            else:
                # self.play_not_allowed_sound()
                return False

        # 2 - Проверяет, если сделанный ход привел
        # к шаху ИЛИ ушел из под него.
        elif self.remains_checked(to_where):
            # self.play_not_allowed_sound()
            return False

        # success!
        return True

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

        # Если результат отрицательный,
        # происходит выброс из цикла действий.
        if eaten_piece is False: return False

        if type(eaten_piece) is not bool:
            # Иначе проверяет, есть ли другое значение от булевых?
            # removed_piece = eaten_piece
            # Перемещает экземпляр во временное хранилище - список.
            self.object_copies.append(eaten_piece)

        return True

    def remains_checked(self, to_where):

        """ Этот метод задает такое условие:
        Хорошо, шах королю объявлен, но является
        ли предложенный ход избавлением от него? """

        if (self.place_piece_on_board(to_where)
                and self.post_check_king(to_where)):
            return True

        return False

    def post_check_king(self, to_where):

        """ Метод является логическим завершением
            проверки на шах королю и возможности
            оставить фигуру на ее новом месте. """

        if self.is_checked():
            # Проверка провалена.
            # Возвращает фигуру на прежнее место.
            self.chosen_piece_object.moves.clear()
            self.conduct_force_change(to_where, self.chosen_piece_object.loc,
                                      self.object_copies[-1] if self.object_copies else None)

            # Очищает резервное хранилище.
            self.object_copies.clear()
            return False

        self.object_copies.clear()
        return True

        # Позволяет пройти проверку.

