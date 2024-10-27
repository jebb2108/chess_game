""" Класс шахматной доски """
import copy

from chess_pieces import *
from settings import Settings

class Accessor(BoardManipulator, ABC):
    def remove_piece_from_board(self, board, coords, id_num):
        pass

class Board:
    def __init__(self, board=None):
        self.board = [[Empty()] * 8 for _ in range(8)]
        if board is not None:  # оставленная возможность
                               # замены для копирования доски
            self.board.clear()
            self.board = board

        self.all_poss_moves = dict()
        self.settings = Settings()
        self.initialize()


    def initialize(self):
        for obj in self.settings.all_pieces:
            obj_y, obj_x = obj.loc
            self.board[obj_y][obj_x] = obj

        return self.make_all_poss_moves_dict()

    def make_all_poss_moves_dict(self):
        all_pieces = self.settings.all_pieces
        for piece in all_pieces:
            id_num = id(piece)
            res = list([ piece, piece.access_all_moves() ])
            self.all_poss_moves[id_num] = res

    def update_all_poss_moves_dict(self):
        board_inst = self
        for key, value in self.all_poss_moves.items():
            o_piece = value[0]
            self.all_poss_moves[key] = list([ o_piece, o_piece.access_all_moves() ])

        return None

    def print_board(self):
        # Вывод доски на экран.
        res = '\n     A B C D E F G H\n   |=================|\n'
        count = 9
        for y in range(8):
            res += ' {} | '.format(count - 1)
            res += ' '.join(map(str, self.board[y])) + f' | {count - 1}\n'
            count -= 1
        res += '   |=================|\n     A B C D E F G H\n'
        print(res)

        return None

    @staticmethod
    def update_enemy_pieces_moves(board, color_indx=None):
        array = sum(board.board, [])
        for obj in array:
            if obj.color > 0 and obj.color == color_indx:

                gen_key = next((key for key, value in board.all_moves.items()
                                if id(obj) == id(value[0])), None)

                if gen_key is None:
                    raise Exception("Object not found")

                items_moves = obj(board)
                value = obj, items_moves

                board.all_moves[gen_key] = value  # !!!! check it !!!!

        return None




class BoardUser(Board):
    def __init__(self, board=None, chosen_piece_object=Empty):
        super().__init__(board)
        self.chosen_piece_object = chosen_piece_object  # переменная сохраняет экземпляр фигуры,
                                           # над которой программа работает в текущий
                                           # момент для автоматизации процесса


    def pick_piece(self, its_loc_on_board: tuple) -> object:
        coord_y, coord_x = its_loc_on_board
        the_piece = self.board[coord_y][coord_x]
        print(type(the_piece))
        return the_piece


    @property
    def chosen_piece_object(self):
        return self.__chosen_piece_object

    @chosen_piece_object.setter
    def chosen_piece_object(self, chosen_piece_object):
        if issubclass(type(chosen_piece_object), Piece):
            # Новые обязательные динамические атрибуты классу BoardTools
            self.chosen_piece_class = self.get_class(chosen_piece_object)
            self.chosen_piece_color = self.get_color(chosen_piece_object)
            # Выролняет назначение основному атрибуту
            self.__chosen_piece_object = chosen_piece_object

        else:
            self.chosen_piece_class = Empty
            self.chosen_piece_color = None
            self.__chosen_piece_object = None

    def get_class(self, o_piece):
        coords = o_piece.loc
        # Из-за того, что не могу спуститься ниже,
        # программу делает проверку на класс на этом уровне.
        class_mapping = {
            Pawn: 'class.Pawn',
            Rock: 'class.Rock',
            Knight: 'class.Knight',
            Bishop: 'class.Bishop',
            Queen: 'class.Queen',
            King: 'class.King'
        }
        obj = self.board[coords[0]][coords[1]]
        return class_mapping.get(type(obj), 'Empty')

    def get_color(self, data) -> int or None:
        """ Простой метод для определения цвета
          фигуры в заданных координатах доски. """

        if type(data) is tuple:
            coord_y, coord_x = data
        else:
            coord_y, coord_x = data.loc

        try:
            color = self.board[coord_y][coord_x].color
        except IndexError:  # Индекс выходит за пределы клеток.
            return None

        # Возвращает цвет фигуры.
        return color

    def attempt_piece_to_move(self, dest_coords: list) -> [True or False]:
        """ Проверяет, если по правилам шахмат возможно совершить ход с данными координатами """
        deleted_item = self.chosen_piece_object._move_object(dest_coords, board_list=self.board)   # noqa

        if deleted_item is False:
            self.update_all_poss_moves_dict()
            return False

        # Удаление экземпляра из общего словаря.
        elif deleted_item is not None:
            if deleted_item[0] in self.all_poss_moves:
                del self.all_poss_moves[deleted_item[0]]
                # Обновление всего, чтобы
                # было затронуто перемещением.
            self.update_all_poss_moves_dict()
            return deleted_item  # Id needed in moves_dict !!!

        else:
            self.update_all_poss_moves_dict()
            return True

    def conduct_change(self, to_where):
        """ Метод изменяет доску совершая ход после сделанной проверки """
        if self.get_color(to_where) == self.chosen_piece_object.enemy_color:
            enemy_piece = self.pick_piece(to_where)

            # Нахожу искомый id вражеской фигуры, который находит нужную фигуру со всеми ходами
            # из списка всех ходов активных фигур.
            gen_id = next((item_id for item_id, item_obj in self.all_poss_moves.items() if
                           id(enemy_piece) == id(item_obj[0])), None)
            # удаление фигуры из общего списка
            del self.all_poss_moves[gen_id]

        orig_y, orig_x = self.chosen_piece_object.loc

        self.board[orig_y][orig_x] = Empty()
        self.board[to_where[0]][to_where[1]] = self.chosen_piece_object

        self.chosen_piece_object._set_loc(tuple(to_where))  # noqa

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
            self.update_all_poss_moves_dict()

            if self.chosen_piece_class == 'class.King':
                self.chosen_piece_object.safe_zone = self.chosen_piece_object.loc

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
                        self.update_all_poss_moves_dict()
                        return True
                    else:
                        return False

        return True