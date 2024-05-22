""" Класс шахматной доски """

from chess_pieces import *
from settings import Settings


class Board:

    def __init__(self):
        self.board = [[Empty()] * 8 for y in range(8)]
        self.settings = Settings()
        self._initialize()

    def _initialize(self):
        for obj in self.settings.all_pieces:
            self.board[obj.y][obj.x] = obj

    def print_board(self):
        res = ''
        for y in range(8):
            res += ''.join(map(str, self.board[y])) + '\n'
        print(res)

    def get_color(self, x, y):
        return self.board[x][y].color

    # noinspection PyProtectedMember
    def change_its_position(self, obj, action, from_where, to_where, direction=None):
        board = self
        if isinstance(type(obj), type(Pawn)):
            if action == 'move':
                obj._check_move(from_where, to_where, direction)
                obj._move_pawn(board, from_where, to_where, direction)

            if action == 'eat':
                obj._eat_by_pawn(board, from_where, to_where, direction)

            return True

        return print('Nothing changed')
