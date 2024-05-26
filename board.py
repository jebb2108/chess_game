""" Класс шахматной доски """

from chess_pieces import *
from settings import Settings


class AbortTransaction(Exception):
    pass


class Board:

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
        # В этой переменной программе хранит уникальные
        # идентификаторы со всеми ходами фигуры в одном словаре.
        for item in self.settings.all_pieces:
            res = self.get_moves(item)
            id_num = id(item)
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
        # Лишний метод для определения цвета
        # фигуры в заданных координатах доски.
        try:
            color = self.board[y][x].color
        except IndexError:
            return None

        return color

    def get_moves(self, item):
        board = self
        res = item._get_all_moves(board)
        return res

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

        # Сверяет экземпляр с наименованием класса фигуры.
        # Выполняет перемещения фигуры в зависимости от ее характеристик.
        if isinstance(obj, Pawn):
            # Указывает основные действия указанные выше уровнем.
            obj._move_pawn(board, to_where)
            # Возвращает True для последующего взаимодействия программы.
            return True
        if isinstance(obj, Rock):
            obj._move_rock(board, to_where)

        # В случае проблем выводит это сообщение.
        return True
