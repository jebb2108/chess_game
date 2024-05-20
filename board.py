""" Класс шахматной доски """
from chess_pieces import *


class Board:

    def __init__(self):
        self.board = [[Empty()] * 8 for y in range(8)]
        self.board[1][1] = Pawn(Color.black)
        self.board[0][4] = King(Color.black)

    def __str__(self):
        res = ''
        for y in range(8):
            res += ''.join(map(str, self.board[y])) + '\n'
        return res

    def get_color(self, x, y):
        return self.board[x][y].color

    def get_moves(self, x, y):
        return self.board[y][x].get_moves(self, x, y)

    def move(self, xy_from, xy_to):
        self.board[xy_to[1]][xy_to[0]] = self.board[xy_from[1]][xy_from[0]]
        self.board[xy_from[1]][xy_from[0]] = Empty()

o_board = Board()
print(o_board)
m = o_board.get_moves(2, 1)
o_board.move([2, 2], m[0])
