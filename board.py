""" Класс шахматной доски """

from chess_pieces import *


class Board:

    def __init__(self):
        self.board = [[Empty()] * 8 for y in range(8)]
        self.board[1][1] = Pawn(Color.black)
        self.board[6][1] = Pawn(Color.white)
        self.board[0][4] = King(Color.black)

    def print_board(self):
        res = ''
        for y in range(8):
            res += ''.join(map(str, self.board[y])) + '\n'
        print(res)

    def get_color(self, x, y):
        return self.board[x][y].color

    def get_moves(self, x, y):
        color = []
        obj = self.board[x][y]
        if obj != '.':
            color.append(obj.color)
        return color


