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

    def _set_black_pawns(self):
        # X представляет горизонтальную позицию.
        x = 0
        for b_pawn in range(7 + 1):
            o_pawn = Pawn(x, 1, Color.black)  # o_pawn временная переменная
                                                 # для каждого экземпляра.
            self.all_pieces.append(o_pawn)       # Затем присоединяет к списку.
            x += 1
        return self.all_pieces

    def _set_white_pawns(self):
        x = 0
        for w_pawn in range(7 + 1):
            o_pawn = Pawn(x, 6, Color.white)
            self.all_pieces.append(o_pawn)
            x += 1
        return self.all_pieces
