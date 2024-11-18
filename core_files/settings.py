""" Класс для выполнения посредственных действий:
расставляет шахматные фигуры на начальные позиции,
конвертирует удобно-читаемые позиции в координаты,
с чем уже работает программа и прочее... """

from core_files.pieces import Empty, Color, Piece, Pawn, Rock, Knight, Bishop, Queen, King


class Settings:

    hashed_dict_castling = {
        (0, 2): (0, 0),
        (0, 6): (0, 7),
        (7, 2): (7, 0),
        (7, 6): (7, 7)
    }

    all_rock_appropriate_moves = {
        (0, 0): (0, 3),
        (0, 7): (0, 5),
        (7, 0): (7, 3),
        (7, 7): (7, 5)
    }

    all_king_appropriate_moves = {
        (0, 4): (0, 1),
        (0, 4): (0, 6),
        (7, 4): (7, 1),
        (7, 4): (7, 6)
    }

    class_mapping = {
        'Empty': Empty,
        'Color': Color,
        'Piece': Piece,
        'Pawn': Pawn,
        'Rock': Rock,
        'Knight': Knight,
        'Bishop': Bishop,
        'Queen': Queen,
        'King': King
    }

    def __init__(self, window):
        self.window = window
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
            o_pawn = Pawn(self.window, loc, Color.black, back_or_forth=1)  # o_pawn временная переменная
            self.all_pieces.append(o_pawn)  # Затем присоединяет к списку.
        return None

    def _set_white_pawns(self):
        for coord_x in range(0, 7 + 1):
            loc = (6, coord_x)
            o_pawn = Pawn(self.window, loc, Color.white, back_or_forth=-1)
            self.all_pieces.append(o_pawn)
        return None

    def _set_black_rocks(self):
        loc_list = [(0, 0), (0, 7)]
        o_rock1 = Rock(self.window, loc_list[0], Color.black)
        o_rock2 = Rock(self.window, loc_list[1], Color.black)
        self.all_pieces.extend([o_rock1, o_rock2])
        return None

    def _set_white_rocks(self):
        loc_list = [(7, 0), (7, 7)]
        o_rock1 = Rock(self.window, loc_list[0], Color.white)
        o_rock2 = Rock(self.window, loc_list[1], Color.white)
        self.all_pieces.extend([o_rock1, o_rock2])
        return None

    def _set_black_knights(self):
        loc_list = [(0, 1), (0, 6)]
        o_knight1 = Knight(self.window, loc_list[0], Color.black)
        o_knight2 = Knight(self.window, loc_list[1], Color.black)
        self.all_pieces.extend([o_knight1, o_knight2])
        return None

    def _set_white_knights(self):
        loc_list = [(7, 1), (7, 6)]
        o_knight1 = Knight(self.window, loc_list[0], Color.white)
        o_knight2 = Knight(self.window, loc_list[1], Color.white)
        self.all_pieces.extend([o_knight1, o_knight2])
        return None

    def _set_black_bishops(self):
        loc_list = [(0, 2), (0, 5)]
        o_bishop1 = Bishop(self.window, loc_list[0], Color.black)
        o_bishop2 = Bishop(self.window, loc_list[1], Color.black)
        self.all_pieces.extend([o_bishop1, o_bishop2])
        return None

    def _set_white_bishops(self):
        loc_list = [(7, 2), (7, 5)]
        o_bishop1 = Bishop(self.window, loc_list[0], Color.white)
        o_bishop2 = Bishop(self.window, loc_list[1], Color.white)
        self.all_pieces.extend([o_bishop1, o_bishop2])
        return None

    def _set_queens(self):
        loc_list = [(0, 3), (7, 3)]
        black_queen = Queen(self.window, loc_list[0], Color.black)
        white_queen = Queen(self.window, loc_list[1], Color.white)
        self.all_pieces.extend([black_queen, white_queen])
        return None

    def _set_kings(self):
        loc_list = [(0, 4), (7, 4)]
        black_king = King(self.window, loc_list[0], Color.black)
        white_king = King(self.window, loc_list[1], Color.white)
        self.all_pieces.extend([black_king, white_king])
        return None