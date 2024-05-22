from board import Board
from settings import Settings


class GamePlay(Board):

    def __init__(self):
        super().__init__()
        self.settings = Settings()

    def move_pawn(self, yx_from, yx_to):
        action = 'move'
        pawn = self.board[yx_from[0]][yx_from[1]]  # leave it here
        direction = 1 if pawn.color == 2 else -1  # leave it here

        self.change_its_position(pawn, action, yx_from, yx_to, direction)
        return 'Operation went completely'

    def eat_by_pawn(self, yx_from, yx_to):
        action = 'eat'
        pawn = self.board[yx_from[0]][yx_from[1]]
        direction = 1 if pawn.color == 2 else -1
        self.change_its_position(pawn, action, yx_from, yx_to, direction)
        return 'Operation went completely'


if __name__ == '__main__':
    my_game = GamePlay()

# noinspection PyUnboundLocalVariable
my_game.print_board()
my_game.move_pawn([1, 1], [2, 1])
my_game.move_pawn([2, 1], [3, 1])
my_game.move_pawn([3, 1], [4, 1])
my_game.move_pawn([4, 1], [3, 1])
my_game.print_board()
