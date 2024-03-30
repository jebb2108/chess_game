class Board:
    board = [[None] * 8 for _ in range(8)]
    coords = {

        'A1': (7, 0), 'A2': (6, 0), 'A3': (5, 0), 'A4': (4, 0),
        'A5': (3, 0), 'A6': (2, 0), 'A7': (1, 0), 'A8': (0, 0),

        'B1': (7, 1), 'B2': (6, 1), 'B3': (5, 1), 'B4': (4, 1),
        'B5': (3, 1), 'B6': (2, 1), 'B7': (1, 1), 'B8': (0, 1),

        'C1': (7, 2), 'C2': (6, 2), 'C3': (5, 2), 'C4': (4, 2),
        'C5': (3, 2), 'C6': (2, 2), 'C7': (1, 2), 'C8': (0, 2),

        'D1': (7, 3), 'D2': (6, 3), 'D3': (5, 3), 'D4': (4, 3),
        'D5': (3, 3), 'D6': (2, 3), 'D7': (1, 3), 'D8': (0, 3),

        'E1': (7, 4), 'E2': (6, 4), 'E3': (5, 4), 'E4': (4, 4),
        'E5': (3, 4), 'E6': (2, 4), 'E7': (1, 4), 'E8': (0, 4),

        'F1': (7, 5), 'F2': (6, 5), 'F3': (5, 5), 'F4': (4, 5),
        'F5': (3, 5), 'F6': (2, 5), 'F7': (1, 5), 'F8': (0, 5),

        'G1': (7, 6), 'G2': (6, 6), 'G3': (5, 6), 'G4': (4, 6),
        'G5': (3, 6), 'G6': (2, 6), 'G7': (1, 6), 'G8': (0, 6),

        'H1': (7, 7), 'H2': (6, 7), 'H3': (5, 7), 'H4': (4, 7),
        'H5': (3, 7), 'H6': (2, 7), 'H7': (1, 7), 'H8': (0, 7),
    }

    @staticmethod
    def _get_coords(new_pos: str) -> tuple:
        tpl = Board.coords.get(new_pos)
        new_y, new_x = tpl[0], tpl[1]
        return new_y, new_x

    @staticmethod
    def print_board():
        print("\n" + "-" * 90)
        i = 8
        for line in Board.board:
            print(i, "|", end=" ")
            i -= 1
            for figure in line:
                print('{:^10s}'.format(str(figure)), end="|")
            print("\n" + "-" * 90)
        for i in "ABCDEFGH":
            print(" ", end=" ")
            print('    ', '{:^3s}'.format(i), end=" ")


class ChessPieces(Board):

    def __init__(self, name, color, pos_y, pos_x):
        self.name = name
        self.color = color
        self.pos_y = pos_y
        self.pos_x = pos_x
        self.__set_board()

    def __set_board(self):
        Board.board[self.pos_y][self.pos_x] = self.name

    def move_piece(self, new_pos):
        new_y, new_x = Board._get_coords(new_pos)
        Board.board[self.pos_y][self.pos_x] = None
        Board.board[new_y][new_x] = self.name


white_pawn1 = ChessPieces('w_pawn', 'white', 6, 0)
white_pawn2 = ChessPieces('w_pawn', 'white', 6, 1)
white_pawn3 = ChessPieces('w_pawn', 'white', 6, 2)
white_pawn4 = ChessPieces('w_pawn', 'white', 6, 3)
white_pawn5 = ChessPieces('w_pawn', 'white', 6, 4)
white_pawn6 = ChessPieces('w_pawn', 'white', 6, 5)
white_pawn7 = ChessPieces('w_pawn', 'white', 6, 6)
white_pawn8 = ChessPieces('w_pawn', 'white', 6, 7)

black_pawn1 = ChessPieces('b_pawn', 'white', 1, 0)
black_pawn2 = ChessPieces('b_pawn', 'white', 1, 1)
black_pawn3 = ChessPieces('b_pawn', 'white', 1, 2)
black_pawn4 = ChessPieces('b_pawn', 'white', 1, 3)
black_pawn5 = ChessPieces('b_pawn', 'white', 1, 4)
black_pawn6 = ChessPieces('b_pawn', 'white', 1, 5)
black_pawn7 = ChessPieces('b_pawn', 'white', 1, 6)
black_pawn8 = ChessPieces('b_pawn', 'white', 1, 7)

board = Board()

white_pawn5.move_piece('E4')
white_pawn2.move_piece('B3')
board.print_board()
