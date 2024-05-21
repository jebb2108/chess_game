from board import Board
from settings import Settings
from chess_pieces import *


class GamePlay(Board):

    def __init__(self):
        super().__init__()
        self.settings = Settings()

    def move_pawn(self, yx_from, yx_to):
        pawn = self.board[yx_from[0]][yx_from[1]]
        direction = 1 if pawn.color == 2 else -1
        if (yx_to[0] - yx_from[0]) * direction < 0 or yx_from[1] != yx_to[1]:
            return print('Incorrect input')
        elif pawn.color and yx_from[0] < 7 and self.get_color(yx_from[0] + 1, yx_from[1]) == Color.empty:
            if pawn.allowed_moves >= (yx_to[0] - yx_from[0]) * direction:
                self.board[yx_to[0]][yx_to[1]] = self.board[yx_from[0]][yx_from[1]]
                self.board[yx_from[0]][yx_from[1]] = Empty()
                pawn.allowed_moves = 1
                return 'Successfully moved'
            else:
                return print('Pawn cannot move so far')


if __name__ == '__main__':
    my_game = GamePlay()

my_game.print_board()
# my_game.move_pawn([1, 1], [3, 2])
# my_game.print_board()
my_game.move_pawn([6, 1],[4, 1])
my_game.print_board()
