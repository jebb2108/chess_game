""" Класс для выполнения посредственных действий:
расставляет шахматные фигуры на начальные позиции,
конвертирует удобно-читаемые позиции в координаты,
с чем уже работает программа и прочее... """

from pieces import Color, Pawn, Rock, Knight, Bishop, Queen, King


class Settings:
    pixel_mapping = {
        (0, 0): [65, 65],
        (0, 1): [130, 65],
        (0, 2): [195, 65],
        (0, 3): [260, 65],
        (0, 4): [325, 65],
        (0, 5): [390, 65],
        (0, 6): [455, 65],
        (0, 7): [520, 65],
        (1, 0): [65, 130],
        (1, 1): [130, 130],
        (1, 2): [195, 130],
        (1, 3): [260, 130],
        (1, 4): [325, 130],
        (1, 5): [390, 130],
        (1, 6): [455, 130],
        (1, 7): [520, 130],
        (2, 0): [65, 195],
        (2, 1): [130, 195],
        (2, 2): [195, 195],
        (2, 3): [260, 195],
        (2, 4): [325, 195],
        (2, 5): [390, 195],
        (2, 6): [455, 195],
        (2, 7): [520, 195],
        (3, 0): [65, 260],
        (3, 1): [130, 260],
        (3, 2): [195, 260],
        (3, 3): [260, 260],
        (3, 4): [325, 260],
        (3, 5): [390, 260],
        (3, 6): [455, 260],
        (3, 7): [520, 260],
        (4, 0): [65, 325],
        (4, 1): [130, 325],
        (4, 2): [195, 325],
        (4, 3): [260, 325],
        (4, 4): [325, 325],
        (4, 5): [390, 325],
        (4, 6): [455, 325],
        (4, 7): [520, 325],
        (5, 0): [65, 390],
        (5, 1): [130, 390],
        (5, 2): [195, 390],
        (5, 3): [260, 390],
        (5, 4): [325, 390],
        (5, 5): [390, 390],
        (5, 6): [455, 390],
        (5, 7): [520, 390],
        (6, 0): [65, 455],
        (6, 1): [130, 455],
        (6, 2): [195, 455],
        (6, 3): [260, 455],
        (6, 4): [325, 455],
        (6, 5): [390, 455],
        (6, 6): [455, 455],
        (6, 7): [520, 455],
        (7, 0): [65, 520],
        (7, 1): [130, 520],
        (7, 2): [195, 520],
        (7, 3): [260, 520],
        (7, 4): [325, 520],
        (7, 5): [390, 520],
        (7, 6): [455, 520],
        (7, 7): [520, 520]
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
