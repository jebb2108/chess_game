""" Класс самого высокого уровня,
с чем непосредственно взаимодействует пользователь. """
from pprint import *

from board import Board


# from settings import Settings


class GamePlay(Board):

    # Пока не используемый конструктор.

    # def __init__(self):
    #     super().__init__()
    #     self.settings = Settings()

    def move_pawn(self, yx_from, to_where):
        # Метод для перемещения пешки
        pawn = self.board[yx_from[0]][yx_from[1]]  # Передаю подконтрольный экземпляр переменной.

        self.change_its_position(pawn, to_where)

        return 'Operation went completely'

    def move_rock(self, yx_from, to_where):
        if self.get_class(yx_from) == 'class.Rock':
            rock = self.board[yx_from[0]][yx_from[1]]
            self.change_its_position(rock, to_where)
        else:
            return print('Mistake brrooo!')


# Приказывает Python не гулять по библиотекам, а считать этот файл за главный.
if __name__ == '__main__':
    my_game = GamePlay()

# Действия:

res = my_game.all_moves
pprint(res, width=100)