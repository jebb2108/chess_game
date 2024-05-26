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

    def _set_black_pawns(self):
        # X представляет горизонтальную позицию.
        x = 0
        for b_pawn in range(7 + 1):
            o_pawn = Pawn(1, x, Color.black)  # o_pawn временная переменная
            o_pawn.back_or_forth = 1  # для каждого экземпляра.
            o_pawn.enemy_color = Color.white
            self.all_pieces.append(o_pawn)  # Затем присоединяет к списку.
            x += 1
        return None

    def _set_white_pawns(self):
        x = 0
        for w_pawn in range(7 + 1):
            o_pawn = Pawn(6, x, Color.white)
            o_pawn.back_or_forth = -1
            o_pawn.enemy_color = Color.black
            self.all_pieces.append(o_pawn)
            x += 1
        return None

    def _set_black_rocks(self):
        o_rock1 = Rock(0, 0, Color.black)
        o_rock1.enemy_color = Color.white
        o_rock2 = Rock(0, 7, Color.black)
        o_rock2.enemy_color = Color.white
        self.all_pieces.extend([o_rock1, o_rock2])
        return None

    def _set_white_rocks(self):
        o_rock1 = Rock(7, 0, Color.white)
        o_rock1.enemy_color = Color.black
        o_rock2 = Rock(7, 7, Color.white)
        o_rock2.enemy_color = Color.black
        self.all_pieces.extend([o_rock1, o_rock2])
        return None
