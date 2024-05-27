from pprint import *
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
            self.__auto_print()
        else:
            return 'There was a mistake happened.'

    def move_rock(self, from_where, to_where):
        if self.get_class(from_where) == 'class.Rock':
            rock = self.board[from_where[0]][from_where[1]]
            self.change_its_position(rock, to_where)
            self.__auto_print()
        else:
            return 'There was a mistake happened.'

    def __auto_print(self):
        my_game.print_board()


# Приказывает Python не гулять по библиотекам, а принимать этот файл за главный.
if __name__ == '__main__':
    my_game = GamePlay()

# noinspection PyUnboundLocalVariable
# Действия:

# res = my_game.all_moves
# pprint(res, width=100)
# pprint(my_game.all_moves, width=100)
# #
# my_game.move_pawn([6, 1], [4, 1])
# my_game.move_rock([7, 0], [7, 1])
# my_game.move_rock([7, 1], [5, 1])
# my_game.move_rock([5, 1], [5, 7])
# my_game.move_rock([5, 7], [1, 7])
#
# pprint(my_game.all_moves)