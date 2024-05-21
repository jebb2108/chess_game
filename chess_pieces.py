""" Класс для всех шахматных фигур """


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
    allowed_moves = 2

    def __init__(self, x, y, color):
        super().__init__(color)
        self.x = x
        self.y = y


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
