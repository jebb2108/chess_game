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
        self._set_all_rocks()

    def _set_black_pawns(self):
        # X представляет горизонтальную позицию.
        x = 0
        for b_pawn in range(7 + 1):
            o_pawn = Pawn(1, x, Color.black)  # o_pawn временная переменная
                                                 # для каждого экземпляра.
            self.all_pieces.append(o_pawn)       # Затем присоединяет к списку.
            x += 1
        return self.all_pieces

    def _set_white_pawns(self):
        x = 0
        for w_pawn in range(7 + 1):
            o_pawn = Pawn(6, x, Color.white)
            self.all_pieces.append(o_pawn)
            x += 1
        return self.all_pieces

    def _set_all_rocks(self):
        xy1, xy2, xy3, xy4 = (0, 0), (0, 7), (7, 0), (7, 7)
        o_rock = Rock(xy1[0], xy1[1], Color.black)
        self.all_pieces.append(o_rock)
        o_rock = Rock(xy2[0], xy2[1], Color.black)
        self.all_pieces.append(o_rock)
        o_rock = Rock(xy3[0], xy3[1], Color.white)
        self.all_pieces.append(o_rock)
        o_rock = Rock(xy4[0], xy4[1], Color.white)
        self.all_pieces.append(o_rock)
        return self.all_pieces
