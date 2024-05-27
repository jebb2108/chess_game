# from pprint import *
from pprint import pprint

from board import Board


class GamePlay(Board):
    """ Класс самого высокого уровня,
    с чем непосредственно взаимодействует пользователь. """

    def move_pawn(self, from_where, to_where):
        # Метод для перемещения пешки
        # Проверка на правильность введенной команды.
        if self.get_class(from_where) == 'class.Pawn':
            pawn = self.board[from_where[0]][from_where[1]]  # Передаю подконтрольный экземпляр переменной.
            self.change_its_position(pawn, to_where)
            self.auto_print()
        else:
            return 'There was a mistake happened.'

    def move_rock(self, from_where, to_where):
        if self.get_class(from_where) == 'class.Rock':
            rock = self.board[from_where[0]][from_where[1]]
            self.change_its_position(rock, to_where)
            self.auto_print()
        else:
            return 'There was a mistake happened.'

    def move_knight(self, from_where, to_where):
        if self.get_class(from_where) == 'class.Knight':
            knight = self.board[from_where[0]][from_where[1]]
            self.change_its_position(knight, to_where)
            self.auto_print()
        else:
            return 'There was a mistake happened.'

    def move_bishop(self, from_where, to_where):
        if self.get_class(from_where) == 'class.Bishop':
            bishop = self.board[from_where[0]][from_where[1]]
            self.change_its_position(bishop, to_where)
            self.auto_print()
        else:
            return 'There was a mistake happened.'

    def move_queen(self, from_where, to_where):
        if self.get_class(from_where) == 'class.Queen':
            queen = self.board[from_where[0]][from_where[1]]
            self.change_its_position(queen, to_where)
            self.auto_print()
        else:
            return 'There was a mistake happened.'


    @staticmethod
    def auto_print():
        my_game.print_board()


# Приказывает Python не гулять по библиотекам, а принимать этот файл за главный.
if __name__ == '__main__':
    my_game = GamePlay()


my_game.print_board()



# print(my_game.all_moves)

# noinspection PyUnboundLocalVariable
# Действия:

# res = my_game.all_moves
# pprint(res, width=100)
# pprint(my_game.all_moves, width=100)
# #
# pprint(my_game.all_moves, width=150)
# res1 = my_game.all_moves
#
# my_game.move_pawn([6, 1], [4, 1])
# my_game.move_rock([7, 0], [7, 1])
# my_game.move_rock([7, 1], [5, 1])
# my_game.move_rock([5, 1], [5, 7])
# my_game.move_rock([5, 7], [1, 7])
# #
# # pprint(my_game.all_moves)
#
# pprint(my_game.all_moves, width=150)
# res2 = my_game._update_moves_dict()
#
# print(res1 == res2)
#
# pprint(my_game.all_moves, width=150)

# my_game.move_knight([0, 1], [2, 2])
# pprint(my_game.all_moves)
# my_game.move_knight([2, 2], [0, 3])
# my_game.move_knight([2, 2], [4, 3])
# my_game.move_knight([4, 3], [6, 2])
# my_game.move_knight([6, 2], [7, 0])
# my_game.move_knight([7, 0], [7, -1])
# my_game.move_knight([7, 0], [6, 2])
# my_game.move_knight([6, 2], [5, 4])
# my_game.move_knight([5, 4], [7, 3])
# my_game.move_knight([7, 3], [9, 2])