""" Класс для выполнения посредственных действий:
расставляет шахматные фигуры на начальные позиции,
конвертирует удобно-читаемые позиции в координаты,
с чем уже работает программа и прочее... """

from chess_pieces import *


class Settings:
    transcripts = {

        'A1': [7, 0], 'A2': [6, 0], 'A3': [5, 0], 'A4': [4, 0],
        'A5': [3, 0], 'A6': [2, 0], 'A7': [1, 0], 'A8': [0, 0],

        'B1': [7, 1], 'B2': [6, 1], 'B3': [5, 1], 'B4': [4, 1],
        'B5': [3, 1], 'B6': [2, 1], 'B7': [1, 1], 'B8': [0, 1],

        'C1': [7, 2], 'C2': [6, 2], 'C3': [5, 2], 'C4': [4, 2],
        'C5': [3, 2], 'C6': [2, 2], 'C7': [1, 2], 'C8': [0, 2],

        'D1': [7, 3], 'D2': [6, 3], 'D3': [5, 3], 'D4': [4, 3],
        'D5': [3, 3], 'D6': [2, 3], 'D7': [1, 3], 'D8': [0, 3],

        'E1': [7, 4], 'E2': [6, 4], 'E3': [5, 4], 'E4': [4, 4],
        'E5': [3, 4], 'E6': [2, 4], 'E7': [1, 4], 'E8': [0, 4],

        'F1': [7, 5], 'F2': [6, 5], 'F3': [5, 5], 'F4': [4, 5],
        'F5': [3, 5], 'F6': [2, 5], 'F7': [1, 5], 'F8': [0, 5],

        'G1': [7, 6], 'G2': [6, 6], 'G3': [5, 6], 'G4': [4, 6],
        'G5': [3, 6], 'G6': [2, 6], 'G7': [1, 6], 'G8': [0, 6],

        'H1': [7, 7], 'H2': [6, 7], 'H3': [5, 7], 'H4': [4, 7],
        'H5': [3, 7], 'H6': [2, 7], 'H7': [1, 7], 'H8': [0, 7],

    }

    def __init__(self):
        # Конструктор, запускающий сборщики фигур.
        self.all_pieces = []  # Список для каждой из них вместе.
        self._set_black_pawns()
        self._set_white_pawns()
        self._set_black_rocks()
        self._set_white_rocks()
        self._set_black_knights()
        self._set_white_knights()
        self._set_black_bishops()
        self._set_white_bishops()
        self._set_queens()
        self._set_kings()

    def _set_black_pawns(self):
        for coord_x in range(0, 7 + 1):
            loc = (1, coord_x)
            o_pawn = Pawn(loc, Color.black, back_or_forth=1)  # o_pawn временная переменная
            self.all_pieces.append(o_pawn)  # Затем присоединяет к списку.
        return None

    def _set_white_pawns(self):
        for coord_x in range(0, 7 + 1):
            loc = (6, coord_x)
            o_pawn = Pawn(loc, Color.white, back_or_forth=-1)
            self.all_pieces.append(o_pawn)
        return None

    def _set_black_rocks(self):
        loc_list = [(0, 0), (0, 7)]
        o_rock1 = Rock(loc_list[0], Color.black)
        o_rock2 = Rock(loc_list[1], Color.black)
        self.all_pieces.extend([o_rock1, o_rock2])
        return None

    def _set_white_rocks(self):
        loc_list = [(7, 0), (7, 7)]
        o_rock1 = Rock(loc_list[0], Color.white)
        o_rock2 = Rock(loc_list[1], Color.white)
        self.all_pieces.extend([o_rock1, o_rock2])
        return None

    def _set_black_knights(self):
        loc_list = [(0, 1), (0, 6)]
        o_knight1 = Knight(loc_list[0], Color.black)
        o_knight2 = Knight(loc_list[1], Color.black)
        self.all_pieces.extend([o_knight1, o_knight2])
        return None

    def _set_white_knights(self):
        loc_list = [(7, 1), (7, 6)]
        o_knight1 = Knight(loc_list[0], Color.white)
        o_knight2 = Knight(loc_list[1], Color.white)
        self.all_pieces.extend([o_knight1, o_knight2])
        return None

    def _set_black_bishops(self):
        loc_list = [(0, 2), (0, 5)]
        o_bishop1 = Bishop(loc_list[0], Color.black)
        o_bishop2 = Bishop(loc_list[1], Color.black)
        self.all_pieces.extend([o_bishop1, o_bishop2])
        return None

    def _set_white_bishops(self):
        loc_list = [(7, 2), (7, 5)]
        o_bishop1 = Bishop(loc_list[0], Color.white)
        o_bishop2 = Bishop(loc_list[1], Color.white)
        self.all_pieces.extend([o_bishop1, o_bishop2])
        return None

    def _set_queens(self):
        loc_list = [(0, 3), (7, 3)]
        black_queen = Queen(loc_list[0], Color.black)
        white_queen = Queen(loc_list[1], Color.white)
        self.all_pieces.extend([black_queen, white_queen])
        return None

    def _set_kings(self):
        loc_list = [(0, 4), (7, 4)]
        black_king = King(loc_list[0], Color.black)
        white_king = King(loc_list[1], Color.white)
        self.all_pieces.extend([black_king, white_king])
        return None

    @staticmethod
    def get_rock_coords(option=None):

        if option is not None:
            all_rock_coords = {
                (0, 2): [0, 0],
                (0, 6): [0, 7],
                (7, 2): [7, 0],
                (7, 6): [7, 7]
            }

            return dict(all_rock_coords)

    @staticmethod
    def get_rock_moves(option=None):

        if option is not None:
            all_rock_possible_moves = {
                (0, 0): [0, 3],
                (0, 7): [0, 5],
                (7, 0): [7, 3],
                (7, 7): [7, 5]
            }

            return dict(all_rock_possible_moves)
