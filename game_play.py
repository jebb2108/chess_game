# from pprint import *
from pprint import pprint

from board import Board


class GamePlay(Board):
    """ Класс самого высокого уровня,
    с чем непосредственно взаимодействует пользователь. """

    def move_pawn(self, from_where, to_where):
        self._check_king()
        # Метод для перемещения пешки
        # Проверка на правильность введенной команды.
        if self.get_class(from_where) == 'class.Pawn':
            pawn = self.board[from_where[0]][from_where[1]]  # Передаю подконтрольный экземпляр переменной.
            self.change_its_position(pawn, to_where)
            self.auto_print()
        else:
            return 'There was a mistake happened.'

    def move_rock(self, from_where, to_where):
        self._check_king()
        if self.get_class(from_where) == 'class.Rock':
            rock = self.board[from_where[0]][from_where[1]]
            self.change_its_position(rock, to_where)
            self.auto_print()
        else:
            return 'There was a mistake happened.'

    def move_knight(self, from_where, to_where):
        self._check_king()
        if self.get_class(from_where) == 'class.Knight':
            knight = self.board[from_where[0]][from_where[1]]
            self.change_its_position(knight, to_where)
            self.auto_print()
        else:
            return 'There was a mistake happened.'

    def move_bishop(self, from_where, to_where):
        self._check_king()
        if self.get_class(from_where) == 'class.Bishop':
            bishop = self.board[from_where[0]][from_where[1]]
            self.change_its_position(bishop, to_where)
            self.auto_print()
        else:
            return 'There was a mistake happened.'

    def move_queen(self, from_where, to_where):
        self._check_king()
        if self.get_class(from_where) == 'class.Queen':
            queen = self.board[from_where[0]][from_where[1]]
            self.change_its_position(queen, to_where)
            self.auto_print()
        else:
            return 'There was a mistake happened.'

    def move_king(self, from_where, to_where):
        if self.get_class(from_where) == 'class.King':
            king = self.board[from_where[0]][from_where[1]]
            self.change_its_position(king, to_where)
            self.auto_print()
        else:
            return 'There was a mistake happened.'

    @staticmethod
    def _check_king():
        all_attack_moves, kings = list(), list()
        for value in my_game.all_moves.values():
            attack_move = value[1]
            all_attack_moves.extend(attack_move)

        set(all_attack_moves)

        kings.extend([ king for king in my_game.settings.all_pieces if my_game.get_class([king.y, king.x]) == 'class.King'])
        for king in kings:
            if king.safe_zone in all_attack_moves:
                # print('You have to move your king!')
                return False
            return True



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

my_game.move_pawn([6, 4], [4, 4])
my_game.move_pawn([1, 3], [3, 3])
my_game.move_pawn([4, 4], [3, 3])
# my_game.move_king([7, 4], [6, 4])
# pprint(my_game.all_moves)