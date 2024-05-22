""" Класс самого высокого уровня,
с чем непосредственно взаимодействует пользователь. """

from board import Board
# from settings import Settings


class GamePlay(Board):

    # Пока не используемый конструктор.

    # def __init__(self):
    #     super().__init__()
    #     self.settings = Settings()

    def move_pawn(self, yx_from, yx_to):
        # Метод для перемещения пешки
        action = 'move'  # Устанавливаю флажки на каждое действие.
        pawn = self.board[yx_from[0]][yx_from[1]]  # Передаю подконтрольный экземпляр переменной.
        direction = 1 if pawn.color == 2 else -1  # Устанавливаю направление в зависимости от цвета.

        # С новыми переменными перехожу на уровень ниже
        # для манипулирования низко-уровненными данными.
        self.change_its_position(pawn, action, yx_from, yx_to, direction)
        return 'Operation went completely'

    def eat_by_pawn(self, yx_from, yx_to):
        # Метод для поедания вражеской фигуры пешкой.
        action = 'eat'
        pawn = self.board[yx_from[0]][yx_from[1]]
        direction = 1 if pawn.color == 2 else -1
        self.change_its_position(pawn, action, yx_from, yx_to, direction)
        return 'Operation went completely'


# Приказывает Python не гулять по библиотекам, а считать этот файл за главный.
if __name__ == '__main__':
    my_game = GamePlay()


# Действия:

# noinspection PyUnboundLocalVariable
my_game.print_board()
my_game.move_pawn([1, 1], [2, 1])
my_game.move_pawn([2, 1], [3, 1])
my_game.move_pawn([3, 1], [4, 1])
my_game.move_pawn([4, 1], [3, 1])
my_game.print_board()
