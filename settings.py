from chess_pieces import *


class Settings:

    def __init__(self):
        self.all_pieces = []
        self._set_black_pawns()
        self._set_white_pawns()

    def _set_black_pawns(self):
        x = 0
        for b_pawn in range(7 + 1):
            o_pawn = Pawn(x, 1, Color.black)
            self.all_pieces.append(o_pawn)
            x += 1
        return self.all_pieces

    def _set_white_pawns(self):
        x = 0
        for w_pawn in range(7 + 1):
            o_pawn = Pawn(x, 6, Color.white)
            self.all_pieces.append(o_pawn)
            x += 1
        return self.all_pieces
