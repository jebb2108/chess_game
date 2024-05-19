""" Класс для создания всех шахматных фигур и придание им всех характеристик """


class Color(object):
    empty = 0
    white = 1
    black = 2


class Empty(object):
    color = Color.empty

    def get_moves(self, x, y):
        raise Exception('Error')

    def __str__(self):
        return '.'


class Piece:
    img = None

    def __init__(self, color):
        self.color = color

    def __str__(self):
        return self.img[0 if self.color == Color.white else 1]


class Pawn(Piece):
    img = ('\u265F', '\u2659')

    def get_moves(self, x, y):
        moves = []
        if self.color and y < 7 and board.get_color(x, y + 1) == Color.empty:
            moves.append([x, y])
        return moves


class Rock(Piece):
    img = ('\u265C', '\u2656')


class Knight(Piece):
    img = ('\u265E', '\u2658')


class Bishop(Piece):
    img = ('\u265D', '\u2657')


class King(Piece):
    img = ('\u265A', '\u2654')


class Queen(Piece):
    img = ('\u265B', '\u2655')


class Board(object):

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


o_board = Board()
print(o_board)
print(o_board.get_moves(2, 1))
#
# print()
# o_pawn = Pawn(0)
# o_rock = Rock(0)
# o_knight = Knight(0)
# o_bishop = Bishop(0)
# o_queen = Queen(0)
# o_king = King(0)
