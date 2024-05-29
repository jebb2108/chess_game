# from pprint import *
import copy
from pprint import pprint

from copy import *
from board import Board


class WhoMoves(object):

    def __init__(self):
        self.turn = 1
        self.current_move = 1

    def change_turn(self):
        self.turn *= -1
        self.current_move = 1 if self.turn == 1 else 2


class King(Board):

    def __init__(self):
        super().__init__()
        self.black_king = id(my_game.board[0][4])
        self.white_king = id(my_game.board[7][4])


class GamePlay(Board):
    """ Класс самого высокого уровня,
    с чем непосредственно взаимодействует пользователь. """

    def __init__(self):
        super().__init__()
        self.whose_turn_it_is = WhoMoves()

    def move_pawn(self, from_where, to_where, color=None):
        # Метод для перемещения пешки
        # Проверка на правильность введенной команды.
        if self.get_class(from_where) == 'class.Pawn':
            # Передаю подконтрольный экземпляр переменной.
            pawn = self.board[from_where[0]][from_where[1]]
            if self._check_king(pawn, from_where, to_where):
                self.whose_turn_it_is.change_turn()
                self.auto_print()
                return None
            else:
                print('There was a mistake happened.')
                return None
        return None

    def move_rock(self, from_where, to_where, color=None):
        if self.get_class(from_where) == 'class.Rock':
            rock = self.board[from_where[0]][from_where[1]]
            if self._check_king(rock, from_where, to_where):
                self.whose_turn_it_is.change_turn()
                self.auto_print()
                return None
            else:
                return 'There was a mistake happened.'
        print(f'You have to move your {color} king')
        return None

    def move_knight(self, from_where, to_where):
        if self.get_class(from_where) == 'class.Knight':
            knight = self.board[from_where[0]][from_where[1]]
            if self._check_king(knight, from_where, to_where):
                self.whose_turn_it_is.change_turn()
                self.auto_print()
                return None
            else:
                return 'There was a mistake happened.'

    def move_bishop(self, from_where, to_where):
        if self.get_class(from_where) == 'class.Bishop':
            bishop = self.board[from_where[0]][from_where[1]]
            if self._check_king(bishop, from_where, to_where):
                self.whose_turn_it_is.change_turn()
                self.auto_print()
                return None
            else:
                return 'There was a mistake happened.'

    def move_queen(self, from_where, to_where):
        if self.get_class(from_where) == 'class.Queen':
            queen = self.board[from_where[0]][from_where[1]]
            if self._check_king(queen, from_where, to_where):
                self.whose_turn_it_is.change_turn()
                self.auto_print()
                return None
            else:
                return 'There was a mistake happened.'

    def move_king(self, from_where, to_where):
        if self.get_class(from_where) == 'class.King':
            king = self.board[from_where[0]][from_where[1]]
            if self._check_king(king, from_where, to_where):
                self.whose_turn_it_is.change_turn()
                self.auto_print()
            return None
        else:
            return 'There was a mistake happened.'

    def _check_king(self, obj, from_where, to_where):
        piece_touched = my_game.get_color(from_where[0], from_where[1])

        if my_game.whose_turn_it_is.current_move != piece_touched:
            print('This isn`t your turn. ')
            return False

        all_attack_moves = list()
        for value in my_game.all_moves.values():
            attack_move = value[1]
            all_attack_moves.extend(attack_move)
        set(all_attack_moves)

        b_king_safe_zone = my_game.all_moves[kings.black_king][0].safe_zone
        w_king_safe_zone = my_game.all_moves[kings.white_king][0].safe_zone

        if b_king_safe_zone in all_attack_moves:
            alternative_board = self
            alternative_board.change_its_position(obj, to_where)
            if b_king_safe_zone in sum([value[1] for value in alternative_board.all_moves.values()], []):
                print('Black king is under attack!')
                return False if my_game.whose_turn_it_is.current_move == 2 else True
            else:
                self.all_moves = alternative_board.all_moves
                self.board = alternative_board.board
                return True

        if w_king_safe_zone in all_attack_moves:
            alternative_board = self
            alternative_board.change_its_position(obj, to_where)
            if w_king_safe_zone in sum([value[1] for value in alternative_board.all_moves.values()], []):
                print('White king is under attack!')
                return False if my_game.whose_turn_it_is.current_move == 1 else True
            else:
                self.all_moves = alternative_board.all_moves
                self.board = alternative_board.board
                return True

        self.change_its_position(obj, to_where)
        return True


    @staticmethod
    def auto_print():
        my_game.print_board()


# Приказывает Python не гулять по библиотекам, а принимать этот файл за главный.
if __name__ == '__main__':
    my_game = GamePlay()
    kings = King()

# print(my_game.all_moves)

# noinspection PyUnboundLocalVariable
# Действия:
#
my_game.move_pawn([6, 4], [4, 4])
my_game.move_pawn([1, 3], [3, 3])
my_game.move_pawn([4, 4], [3, 3])
my_game.move_knight([0, 6], [1, 4])
my_game.move_king([7, 4], [6, 4])
my_game.move_bishop([0, 2], [4, 6])
my_game.move_pawn([6, 1], [5, 1])
# my_game.move_king([6, 4], [7, 4])
