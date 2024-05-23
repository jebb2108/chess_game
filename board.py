""" Класс шахматной доски """

from chess_pieces import *
from settings import Settings


class AbortTransaction(Exception):
    pass


class Board:

    def __init__(self):
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

    def print_board(self):
        # Вывод доски на экран.
        res = ''
        for y in range(8):
            res += ''.join(map(str, self.board[y])) + '\n'
        print(res)

    def get_color(self, x, y):
        # Лишний метод для определения цвета
        # фигуры в заданных координатах доски.
        try:
            color = self.board[x][y].color
        except IndexError:
            return None

        return color

    def get_moves(self, obj):
        if isinstance(type(obj), type(Rock)):
            obj.get_all_moves()

    # noinspection PyProtectedMember
    def change_its_position(self, obj, action, from_where, to_where=None, direction=None):
        """ Важный метод, который берет экземпляр доски,
        аргументы уровня выше и опускается на уровень ниже,
        чтобы работать с низко-уровненными условиями фигур. """

        # Кладет экземпляр доски в переменную,
        # чтобы работать с ней на уровень ниже.
        board = self

        # Сверяет экземпляр с наименованием класса фигуры.
        # Выполняет перемещения фигуры в зависимости от ее характеристик.
        if isinstance(obj, Pawn):
            # Указывает основные действия указанные выше уровнем.
            if action == 'move':
                obj._check_move(from_where, to_where, direction)
                obj._move_pawn(board, from_where, to_where, direction)

            if action == 'eat':
                obj._eat_by_pawn(board, from_where, to_where, direction)

            # Возвращает True для последующего взаимодействия программы.
            return True
        if isinstance(obj, Rock):
            if action == 'check':
                obj._get_rock_moves(board, (obj.y, obj.x))

        # В случае проблем выводит это сообщение.
        return print('Nothing changed')
