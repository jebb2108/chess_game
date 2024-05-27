""" Класс шахматной доски """

from chess_pieces import *
from settings import Settings


class AbortTransaction(Exception):
    pass


class Board:
    """ Класс доски, отвечает за расстановку всех сущностей на доске. """
    def __init__(self):
        self.all_moves = dict()
        # Создает доску в виде списка из вложенных списков.
        # Отдельным файлом инициализирует экземпляры
        # представляющие собой шахматные фигуры.
        self.board = [[Empty()] * 8 for y in range(8)]
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
        self.make_moves_dict()

    def make_moves_dict(self):
        """ Простой метод для создания словарика ходов. """
        board = self
        for item in self.settings.all_pieces:
            id_num = id(item)
            icon = item.img[item.color - 1]
            res = item._get_all_moves(board), icon
            self.all_moves[id_num] = res

    def print_board(self):
        # Вывод доски на экран.
        res = ''
        for y in range(8):
            res += ''.join(map(str, self.board[y])) + '\n'
        print(res)

    def get_class(self, coords: list):
        # Из-за того, что не могу спуститься ниже,
        # программу делает проверку на класс на этом уровне.
        obj = self.board[coords[0]][coords[1]]
        if isinstance(obj, Pawn): return 'class.Pawn'
        if isinstance(obj, Rock): return 'class.Rock'
        if isinstance(obj, Knight): return 'class.Knight'
        if isinstance(obj, Bishop): return 'class.Bishop'
        if isinstance(obj, Queen): return 'class.Queen'
        if isinstance(obj, King): return 'class.King'
        return 'Unknown type.'

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
    def change_its_position(self, obj, to_where, back_or_forth=None):
        """ Важный метод, который берет экземпляр доски,
        аргументы уровня выше и опускается на уровень ниже,
        чтобы работать с низко-уровненными условиями фигур. """

        # Кладет экземпляр доски в переменную,
        # чтобы работать с ней на уровень ниже.
        board = self

        # Для перехода на нижний уровень я конвертирую все в кортежи.
        to_where = tuple(to_where)

        # Сверяет экземпляр с нужным классом фигуры.
        # Выполняет перемещение фигуры в зависимости от ее условий.
        if isinstance(obj, Pawn):
            # Выполняет основные действия ниже уровнем.
            obj._move_pawn(board, to_where)

        if isinstance(obj, Rock):
            obj._move_rock(board, to_where)

        self.make_moves_dict()
        return None
