""" Класс шахматной доски """

from chess_pieces import *
from settings import Settings


class Board:
    """ Класс доски, отвечает за расстановку всех сущностей на доске. """

    def __init__(self, board=None, all_moves=None):
        self.pawn_dirs = []
        self.all_moves = dict()
        if board is None:
            # Если еще доска не создана, то:
            # Создает доску в виде списка из вложенных списков.
            # Отдельным файлом инициализирует экземпляры
            # представляющие собой шахматные фигуры.
            self.board = [[Empty()] * 8 for _ in range(8)]
            self.settings = Settings()
            self._initialize()

        else:
            self.all_moves = all_moves
            self.board = board

    def _initialize(self):
        # Одноразовый метод, принимающий вложенные параметры класса
        # Settings и внедряет его экземпляры в только что созданную доску.
        for obj in self.settings.all_pieces:
            self.board[obj._get_y()][obj._get_x()] = obj
        # В этом методе программа создает
        # идентификаторы со всеми ходами фигуры в одном словаре.
        # Позже мне он понадобится, когда буду работать с королем.
        self._make_moves_dict()

    def _make_moves_dict(self):
        """ Простой метод для создания словарика ходов. """
        board_inst = self
        for item in self.settings.all_pieces:
            id_num = id(item)
            icon = item.img[item.color - 1]
            res = item, item._get_all_moves(board_inst), icon  # noqa
            self.all_moves[id_num] = res

    def _update_moves_dict(self):
        board_inst = self
        for key, value in self.all_moves.items():
            obj = value[0]
            icon = obj.img[obj.color - 1]
            self.all_moves[key] = (obj, obj._get_all_moves(board_inst), icon)  # noqa

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

    def get_class(self, coords: list):
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

    def get_color(self, loc):
        y, x = loc
        # Простой метод для определения цвета
        # фигуры в заданных координатах доски.
        try:
            color = self.board[y][x].color
        except IndexError:  # Индекс выходит за пределы клеток.
            return None

        # Возвращает цвет фигуры.
        return color

    def castle_king(self, obj, to_where):

        # Вытаскиваю из настроек нужные мне значения для рокировки.
        all_rock_coords = self.settings.get_rock_coords(True)
        all_rock_possible_moves = self.settings.get_rock_moves(True)

        to_where = tuple(to_where)  # Словарные ключи могут быть только неизменными кортежами.
        rock_coords = all_rock_coords[to_where]  # Вытаскиваю значение по ключу. Перевожу все в кортежи.

        # Может быть только ладьею на заданной координате.
        if self.get_class(rock_coords) != 'class.Rock':
            return False

        # Создаю переменную для экземпляра.
        rock = self.board[rock_coords[0]][rock_coords[1]]

        # Может быть только один ход для ладьи в рокировке.
        # Вытаскиваю значение по местонахождению.
        rock_possible_move = all_rock_possible_moves[tuple(rock_coords)]

        # Условие, при котором ладья не может быть тронутой.
        if rock.is_not_changed:
            for move in rock.moves:
                # Ладье должна быть доступна клетка перед королем.
                if list(move) in [[0, 3], [0, 5], [7, 3], [7, 5]]:
                    king_from_where, king_to_where = [obj._get_y(), obj._get_x()], to_where

                    # Происходит перестановка фигур и обновление словаря ходов.
                    self.change_its_position(rock, rock_possible_move)
                    self.force_change(obj, king_from_where, king_to_where)
                    self._update_moves_dict()

                    return True

        # Если условия не соблюдены, выводит False.
        return False

    # noinspection PyProtectedMember
    def change_its_position(self, obj: object, to_where: list):
        """ Важный метод, который берет экземпляр доски,
        аргументы уровня выше и опускается на уровень ниже,
        чтобы работать с низко-уровненными условиями фигур. """

        # Кладет экземпляр доски в переменную,
        # чтобы работать с ней на уровень ниже.
        board_inst = self
        # Если возвращает idшник фигуры, значит
        # экземпляр был съеден и его не должно больше быть в общей свалке фигур.

        # Для перехода на нижний уровень я конвертирую все в кортежи.
        to_where = tuple(to_where)

        # Выполняет перемещение фигуры ниже уровнем.
        deleted_item = obj._move_object(board_inst, to_where)

        if self.pawn_dirs:
            for count, item in enumerate(self.pawn_dirs):
                """
                :params:
                0 - данный экземпляр пешки
                1 - вражеская пешка, которая может атаковать
                2 - координаты для возможного контр-нападения
                """
                item[1].memory[count] = (item[0], item[2])
                self.pawn_dirs.clear()



        elif deleted_item is False:
            self._update_moves_dict()
            return False

        # Удаление экземпляра из общего словаря.
        elif deleted_item is not None:
            if deleted_item[0] in self.all_moves:
                del self.all_moves[deleted_item[0]]
                # Обновление всего, чтобы
                # было затронуто перемещением.

            self._update_moves_dict()
            return deleted_item  # Id needed in moves_dict !!!

        else:
            self._update_moves_dict()
            return True


    def force_change(self, obj, to_where, from_where, removed_piece=None):

        if removed_piece is not None or from_where != to_where:
            if removed_piece is not None:
                self.board[from_where[0]][from_where[1]] = obj
                self.board[to_where[0]][to_where[1]] = removed_piece
            else:
                self.board[from_where[0]][from_where[1]] = obj
                self.board[to_where[0]][to_where[1]] = Empty()

            obj._set_loc((from_where[0], from_where[1]))
            self._update_moves_dict()
            if isinstance(obj, King):
                obj.safe_zone = (obj._get_y(), obj._get_x())
            return True

        return False


    @staticmethod
    def change_board(board, obj, from_where, to_where):

        if board.get_color(to_where) == obj.enemy_color:
            enemy_piece = board.board[to_where[0]][to_where[1]]
            # Исправлено.
            gen_id = next((item_id for item_id, item_obj in board.all_moves.items() if
                           id(enemy_piece) == id(item_obj[0])), None)

            del board.all_moves[gen_id]

        board.board[from_where[0]][from_where[1]] = Empty()
        board.board[to_where[0]][to_where[1]] = obj

        obj._set_loc((to_where[0], to_where[1]))

        if isinstance(obj, King):
            obj.safe_zone = (obj._get_y(), obj._get_x())

        return None

    @staticmethod
    def update_enemy_pieces_moves(board, color_indx=None):
        array = sum(board.board, [])
        for item in array:
            if item.color > 0 and item.color == color_indx:

                gen_key = next((key for key, value in board.all_moves.items()
                                if id(item) == id(value[0])), None)

                if gen_key is None:
                    raise Exception("Object not found")

                items_moves = item._get_all_moves(board)
                value = item, items_moves, item.img[item.color - 1]

                board.all_moves[gen_key] = value  # !!!! check it !!!!

        return None
