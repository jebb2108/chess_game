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
        elif pawn.color and yx_from[0] < 7 and self.get_color(yx_from[0] + (direction * 1), yx_from[1]) == Color.empty:
            if pawn.allowed_moves >= (yx_to[0] - yx_from[0]) * direction:
                self.board[yx_to[0]][yx_to[1]] = self.board[yx_from[0]][yx_from[1]]
                self.board[yx_from[0]][yx_from[1]] = Empty()
                pawn.y, pawn.x = yx_to[0], yx_to[1]
                pawn.allowed_moves = 1
                if yx_from[0] == 1 and yx_to[0] == 0:
                    self._turn_pawn_into_piece(pawn)
                return 'Successfully moved'
            else:
                return print('Pawn cannot move so far')
        else:
            return print('Your pawn cannot move forward')

    def eat_by_pawn(self, yx_from, yx_to):
        pawn = self.board[yx_from[0]][yx_from[1]]
        direction = 1 if pawn.color == 2 else -1
        if (yx_to[0] - yx_from[0]) * direction < 0 or (yx_to[1] - yx_from[1]) not in [1, -1]:
            return print('You can`t go and eat the enemy piece with this distance')
        else:
            self.board[yx_to[0]][yx_to[1]] = self.board[yx_from[0]][yx_from[1]]
            self.board[yx_from[0]][yx_from[1]] = Empty()

    def _turn_pawn_into_piece(self, pawn):
        if pawn.color == 1:
            new_piece = input('What piece would you like to have instead? "queen": ')
            if new_piece == 'queen':
                self.board[pawn.y][pawn.x] = Empty()
                self.board[pawn.y][pawn.x] = Queen(Color.white)
        else:
            return print('Mistake has happened')


if __name__ == '__main__':
    my_game = GamePlay()

# my_game.print_board()

my_game.move_pawn([6, 2], [4, 2])
my_game.move_pawn([4, 2], [3, 2])
my_game.move_pawn([3, 2], [2, 2])
my_game.print_board()
my_game.eat_by_pawn([2, 2], [1, 1])
my_game.print_board()
my_game.move_pawn([1, 1], [0, 1])
my_game.print_board()
