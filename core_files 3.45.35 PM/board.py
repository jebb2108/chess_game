""" Класс шахматной доски """
from abc import ABC

from interface.core_files.settings import Settings
from interface.core_files.pieces import BoardManipulator, Empty, Piece, King, Rock


class Board(BoardManipulator, ABC):
    def __init__(self, window, board=None):
        self.board = [[Empty()] * 8 for _ in range(8)]
        if board is not None:  # оставленная возможность
            # замены для копирования доски
            self.board.clear()
            self.board = board

        self.all_poss_moves = dict()
        self.settings = Settings(window)
        self.initialize()

    def initialize(self):
        container = self.settings.all_pieces
        for piece in container:
            self.board[piece.get_y()][piece.get_x()] = piece

        self.update_all_poss_moves_dict(container)

    def update_all_poss_moves_dict(self, container):
        self.all_poss_moves = { key: [key._get_all_moves(self.board)]
                                for  key in container }

        return

    @staticmethod
    def update_enemy_pieces_moves(board_inst, color_indx=None):

        if color_indx is None:
            color_indx = None

        array = sum(board_inst.board, [])
        for obj in array:
            if obj.color > 0 and obj.color == color_indx:

                gen_key = next(( key for key in board_inst.all_poss_moves
                                if obj.id == key.id), None)

                if gen_key is None:
                    raise Exception("Object not found")

                items_moves = obj(board_inst)
                value = items_moves

                board_inst.all_poss_moves[gen_key] = value  # !!!! check it !!!!

        return None


class BoardUser(Board):
    def __init__(self, board_list=None, chosen_piece_object=Empty):

        self.chosen_piece_object = chosen_piece_object
        self.chosen_piece_class = None
        self.chosen_piece_color = None

        super().__init__(board_list)

    def pick_piece(self, its_loc_on_board: tuple) -> object:
        coord_y, coord_x = its_loc_on_board
        the_piece = self.board[coord_y][coord_x]
        return the_piece

    @property
    def chosen_piece_object(self):
        return self.__chosen_piece_object

    @chosen_piece_object.setter
    def chosen_piece_object(self, chosen_piece_object=None):
        if chosen_piece_object is not None:
            if issubclass(type(chosen_piece_object), Piece):
                # Новые обязательные динамические атрибуты классу BoardTools
                self.chosen_piece_class = self.get_class(self.board, chosen_piece_object.loc)
                self.chosen_piece_color = self.get_color(self.board, chosen_piece_object.loc)
                # Выролняет назначение основному атрибуту
                self.__chosen_piece_object = chosen_piece_object

        else:
            self.__chosen_piece_object = Empty()
            self.chosen_piece_class = None
            self.chosen_piece_color = None


    def attempt_piece_to_move(self, dest_coords: list) -> [True or False]:
        """ Проверяет, если по правилам шахмат возможно совершить ход с данными координатами """
        if self.chosen_piece_object._move_object(dest_coords, board_list=self.board):  # noqa

            if isinstance(self.chosen_piece_object.alien_id, int):
                eaten_piece = next((key for key in self.all_poss_moves
                                    if key.id == self.chosen_piece_object.alien_id), None)
                self.chosen_piece_object.alien_id = None
                del self.all_poss_moves[eaten_piece]
                # Обновление всего, чтобы было затронуто перемещением.
                self.update_all_poss_moves_dict(self.all_poss_moves)
                return eaten_piece

            self.update_all_poss_moves_dict(self.all_poss_moves)
            return True

    def conduct_change(self, to_where):
        """ Метод изменяет доску совершая ход после сделанной проверки """
        if self.get_color(self.board.board, to_where) == self.chosen_piece_object.enemy_color:
            enemy_piece = self.pick_piece(to_where)

            # Нахожу искомый id вражеской фигуры, который находит нужную фигуру со всеми ходами
            # из списка всех ходов активных фигур.
            gen_id = next((obj for obj, item_moves in self.all_poss_moves.items() if
                           enemy_piece.id == obj.id), None)
            # удаление фигуры из общего списка
            del self.all_poss_moves[gen_id]

        orig_y, orig_x = self.chosen_piece_object.loc

        self.board[orig_y][orig_x] = Empty()

        # self.board[to_where[0]][to_where[1]] = self.chosen_piece_object
        # self.chosen_piece_object._set_loc(tuple(to_where))  # noqa

        if self.chosen_piece_class == 'class.King':
            self.chosen_piece_object.safe_zone = self.chosen_piece_object.loc

        return None

    def conduct_force_change(self, to_where: list, from_where: list, removed_piece=None) -> [True or False]:
        """
        :param to_where: Текущее положение, которые было изначально.
        :param from_where: Предыдущее положение, которое нужно вернуть.
        :param removed_piece: Возвращает съеденную фигуру на ее прошлое место.
        :return: Возвращает правду или ложь о проделанном действии.
        """
        # Метод возвращает доску к изначальному
        # состоянию до попытки игроком сходить.
        if removed_piece is not None or from_where != to_where:
            if removed_piece is not None:
                self.board[from_where[0]][from_where[1]] = self.chosen_piece_object
                self.board[to_where[0]][to_where[1]] = removed_piece
            else:
                self.board[from_where[0]][from_where[1]] = self.chosen_piece_object
                self.board[to_where[0]][to_where[1]] = Empty()

            self.chosen_piece_object._set_loc(tuple(from_where))  # noqa
            self.update_all_poss_moves_dict(self.all_poss_moves)

            if self.chosen_piece_class == 'class.King':
                self.chosen_piece_object.safe_zone = self.chosen_piece_object.loc

            # self.update_all_poss_moves_dict()
            return True

        return False

    def check_castling_and_move(self, to_where: list) -> [True or False]:

        if isinstance(self.chosen_piece_object, King):

            # Вытаскиваю из настроек нужные мне значения для рокировки.
            all_rock_coords = self.settings.get_rock_coords(True)
            all_rock_possible_moves = self.settings.get_rock_moves(True)

            to_where = tuple(to_where)  # Словарные ключи могут быть только неизменными кортежами.
            rock_coords = all_rock_coords[to_where]  # Вытаскиваю значение по ключу. Перевожу все в кортежи.
            # Может быть только один ход для ладьи в рокировке.
            # Вытаскиваю значение по местонахождению.5
            rock_possible_move = all_rock_possible_moves[tuple(rock_coords)]

            # Может быть только ладьею на заданной координате.
            rock = self.pick_piece(rock_coords)
            if not isinstance(rock, Rock):
                return False

            # Условие, при котором ладья не может быть тронутой.
            if rock.is_not_changed and self.chosen_piece_object.is_not_changed:
                for move in rock.moves:  # noqa
                    # Ладье должна быть доступна клетка перед королем.
                    if list(move) in [[0, 3], [0, 5], [7, 3], [7, 5]]:
                        king_from_where, king_to_where = king.loc, to_where  # noqa
                        # Происходит перестановка фигур и обновление словаря ходов.
                        self.conduct_change(rock_possible_move)
                        self.conduct_force_change(king_from_where, king_to_where)  # noqa
                        self.update_all_poss_moves_dict(self.all_poss_moves)
                        return True
                    else:
                        return False

        return True
