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
        pawn = self.board[yx_from[0]][yx_from[1]]  # Передаю подконтрольный экземпляр переменной.
        direction = 1 if pawn.color == 2 else -1  # Устанавливаю направление в зависимости от цвета.

        # Проверка на действие
        if yx_from[1] == yx_to[1]:
            action = 'move'  # Устанавливаю флажки на каждое действие.
            self.change_its_position(pawn, action, yx_from, yx_to, direction)
        # С новыми переменными перехожу на уровень ниже
        # для манипулирования низко-уровненными данными.
        else:
            action = 'eat'
            self.change_its_position(pawn, action, yx_from, yx_to, direction)

        return 'Operation went completely'

    def move_rock(self, yx_from, yx_to):
        action = 'move'
        if self.get_class(yx_from) == 'class.Rock':
            rock = self.board[yx_from[0]][yx_from[1]]
            self.change_its_position(rock, action, yx_from, yx_to)
        else:
            return print('Mistake brrooo!')


# Приказывает Python не гулять по библиотекам, а считать этот файл за главный.
if __name__ == '__main__':
    my_game = GamePlay()

# Действия:

# noinspection PyUnboundLocalVariable
my_game.print_board()

my_game.move_rock([0, 0], [0, 3])
my_game.print_board()

