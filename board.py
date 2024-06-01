""" Класс шахматной доски """
import copy

from chess_pieces import *
from settings import Settings


class Board:
    """ Класс доски, отвечает за расстановку всех сущностей на доске. """

    def __init__(self):
        self.all_moves = dict()
        # Создает доску в виде списка из вложенных списков.
        # Отдельным файлом инициализирует экземпляры
        # представляющие собой шахматные фигуры.
        self.board = [[Empty()] * 8 for _ in range(8)]
        self.settings = Settings()
        self._initialize()

    def _initialize(self):
        # Одноразовый метод, принимающий вложенные параметры класса
        # Settings и внедряет его экземпляры в только что созданную доску.
        for obj in self.settings.all_pieces:
            self.board[obj.y][obj.x] = obj
        # В этом методе программа создает
        # идентификаторы со всеми ходами фигуры в одном словаре.
        # Позже мне он понадобится, когда буду работать с королем.
        self._make_moves_dict()

    def _make_moves_dict(self):
        """ Простой метод для создания словарика ходов. """
        board = self
        for item in self.settings.all_pieces:
            id_num = id(item)
            icon = item.img[item.color - 1]
            res = item, item._get_all_moves(board), icon  # noqa
            self.all_moves[id_num] = res

    def _update_moves_dict(self):
        board = self
        for key, value in self.all_moves.items():
            obj = value[0]
            icon = obj.img[obj.color - 1]
            self.all_moves[key] = (obj, obj._get_all_moves(board), icon)  # noqa

    def print_board(self):
        # Вывод доски на экран.
        res = '\n     A B C D E F G H\n   |=================|\n'
        count = 9
        for y in range(8):
            res += ' {} | '.format(count-1)
            res += ' '.join(map(str, self.board[y])) + f' | {count-1}\n'
            count -= 1
        res += '   |=================|\n     A B C D E F G H\n'
        print(res)

    def get_class(self, coords: list):
        # Из-за того, что не могу спуститься ниже,
        # программу делает проверку на класс на этом уровне.
        obj = self.board[coords[0]][coords[1]]
        if isinstance(obj, Pawn): return 'class.Pawn'
        elif isinstance(obj, Rock): return 'class.Rock'
        elif isinstance(obj, Knight): return 'class.Knight'
        elif isinstance(obj, Bishop): return 'class.Bishop'
        elif isinstance(obj, Queen): return 'class.Queen'
        elif isinstance(obj, King): return 'class.King'
        elif isinstance(obj, Empty): return 'Empty'

    def get_color(self, y, x):
        # Простой метод для определения цвета
        # фигуры в заданных координатах доски.
        try:
            color = self.board[y][x].color
        except IndexError:  # Индекс выходит за пределы клеток.
            return None

        # Возвращает цвет фигуры.
        return color

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
        deleted_item = None
        # Сверяет экземпляр с нужным классом фигуры.
        # Выполняет перемещение фигуры в зависимости от ее условий.
        if isinstance(obj, Pawn):
            # Выполняет основные действия ниже уровнем.
            deleted_item = obj._move_pawn(board_inst, to_where)
        elif isinstance(obj, Rock):
            deleted_item = obj._move_rock(board_inst, to_where)
        elif isinstance(obj, Knight):
            deleted_item = obj._move_knight(board_inst, to_where)
        elif isinstance(obj, Bishop):
            deleted_item = obj._move_bishop(board_inst, to_where)
        elif isinstance(obj, Queen):
            deleted_item = obj._move_queen(board_inst, to_where)
        elif isinstance(obj, King):
            deleted_item = obj._move_king(board_inst, to_where)


        if deleted_item is False:
            self._update_moves_dict()
            return False

        # Удаление экземпляра из общего словаря.
        print('deleted:', deleted_item)
        if deleted_item is not None:
            print('Success???')
            try:
                print('key', deleted_item[0])
                del self.all_moves[deleted_item[0]]
                # Обновление всего, чтобы
                # было затронуто перемещением.
            except KeyError:
                print('Not really ...')
                pass


            print('Kinda success')
            self._update_moves_dict()
            return deleted_item  # Id needed in moves_dict !!!

        else:
            print('Is it true? ')
            self._update_moves_dict()
            return True


    def force_change(self, obj, to_where, from_where, removed_piece=None):
        print('state1', obj.y, obj.x)
        if type(removed_piece) is not bool:

            self.board[from_where[0]][from_where[1]] = obj
            self.board[to_where[0]][to_where[1]] = removed_piece
            obj.y, obj.x = from_where[0],  from_where[1]
            print('state1', obj.y, obj.x)
            return True


        else:

            if from_where != to_where:

                self.board[from_where[0]][from_where[1]] = obj
                self.board[to_where[0]][to_where[1]] = Empty()
                obj.y, obj.x = from_where[0], from_where[1]

                return True

            return False


