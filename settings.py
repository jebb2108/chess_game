""" Класс для выполнения посредственных действий:
расставляет шахматные фигуры на начальные позиции,
конвертирует удобно-читаемые позиции в координаты,
с чем уже работает программа и прочее... """

from chess_pieces import *


class Settings:

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
        # X представляет горизонтальную позицию.
        x = 0
        for b_pawn in range(7 + 1):
            o_pawn = Pawn(1, x, Color.black)  # o_pawn временная переменная
            o_pawn.back_or_forth = 1  # для каждого экземпляра.
            self.all_pieces.append(o_pawn)  # Затем присоединяет к списку.
            x += 1
        return None

    def _set_white_pawns(self):
        x = 0
        for w_pawn in range(7 + 1):
            o_pawn = Pawn(6, x, Color.white)
            o_pawn.back_or_forth = -1
            self.all_pieces.append(o_pawn)
            x += 1
        return None

    def _set_black_rocks(self):
        o_rock1 = Rock(0, 0, Color.black)
        o_rock2 = Rock(0, 7, Color.black)
        self.all_pieces.extend([o_rock1, o_rock2])
        return None

    def _set_white_rocks(self):
        o_rock1 = Rock(7, 0, Color.white)
        o_rock2 = Rock(7, 7, Color.white)
        self.all_pieces.extend([o_rock1, o_rock2])
        return None

    def _set_black_knights(self):
        o_knight1 = Knight(0, 1, Color.black)
        o_knight2 = Knight(0, 6, Color.black)
        self.all_pieces.extend([o_knight1, o_knight2])
        return None

    def _set_white_knights(self):
        o_knight1 = Knight(7, 1, Color.white)
        o_knight2 = Knight(7, 6, Color.white)
        self.all_pieces.extend([o_knight1, o_knight2])
        return None

    def _set_black_bishops(self):
        o_bishop1 = Bishop(0, 2, Color.black)
        o_bishop2 = Bishop(0, 5, Color.black)
        self.all_pieces.extend([o_bishop1, o_bishop2])
        return None

    def _set_white_bishops(self):
        o_bishop1 = Bishop(7, 2, Color.white)
        o_bishop2 = Bishop(7, 5, Color.white)
        self.all_pieces.extend([o_bishop1, o_bishop2])
        return None

    def _set_queens(self):
        black_queen = Queen(0, 3, Color.black)
        white_queen = Queen(7, 3, Color.white)
        self.all_pieces.extend([black_queen, white_queen])
        return None

    def _set_kings(self):
        black_king = King(0, 4, Color.black)
        white_king = King(7, 4, Color.white)
        self.all_pieces.extend([black_king, white_king])
        return None
