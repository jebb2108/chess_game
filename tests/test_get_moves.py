import pytest

from ..main import GamePlay
from ..board import Board
from ..chess_pieces import Pawn, Color

new_board = Board()
new_pawn = Pawn(1, 0, Color.black)

new_board.all_moves = {
        12345: [new_pawn, [(2, 0), (3, 0)], new_pawn.img[new_pawn.color - 1]]
    }


# noinspection PyTypeChecker
def test_get_moves():
    res = GamePlay.get_moves(GamePlay, new_board, 2)
    expected_result = [(new_pawn, [(2, 0), (3, 0)])]
    assert res == expected_result