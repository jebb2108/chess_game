""" Класс шахматной доски """


class Board():

    def __init__(self):
        self.board = [[None] * 8 for _ in range(8)]

    def show_board(self):
        print(self.board)


o_board = Board()
o_board.show_board()
