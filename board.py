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

    def get_moves(self, obj):
        x, y = 0, 0
        coords = []
        pass
