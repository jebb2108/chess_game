from board import Board


class WhoMoves(object):
    """ Класс, который следит за очередностью ходов белых и черных. """
    def __init__(self):
        # 1 олицетворяет белые фигуры, а -1 черные.
        self.turn = 1
        # Текущий ход.
        self.current_move = 1

    def change_turn(self):
        self.turn *= -1
        # Отдельный атрибут 'current_move' помогает выводить два значения 1 и 2,
        # где в изначальном виде интерпретируются цвета фигуры, что помогает в дальнейших
        # условиях сравнений.
        self.current_move = 1 if self.turn == 1 else 2


class King(Board):
    """ Простой класс, назначающий идентификаторы королям на протяжении всей игры. """
    # С этим могут возникнуть проблемы в будущем из-за вновь созданного экземпляра доске!!!!
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

    def move_pawn(self, from_where: list, to_where: list):
        # Каждый этот метод по сути проверяет,
        # выбрал ли пользователь правильную команду.
        if self.get_class(from_where) == 'class.Pawn':
            # Передаю подконтрольный экземпляр переменной.
            pawn = self.board[from_where[0]][from_where[1]]
            # Следующие методы проверяет, находится ли король под шахом.
            # Если нет или это не ход игрока с битым королем, то
            # позволяет передвинуть фигуру ниже уровнем,
            # затем ход передается другому и печатает доску.
            if self._check_king(pawn, from_where, to_where):
                self.change_its_position(pawn, to_where)
                self.whose_turn_it_is.change_turn()
                self.auto_print()
                return None

        return None

    def move_rock(self, from_where, to_where):
        if self.get_class(from_where) == 'class.Rock':
            rock = self.board[from_where[0]][from_where[1]]
            if self._check_king(rock, from_where, to_where):
                self.change_its_position(rock, to_where)
                self.whose_turn_it_is.change_turn()
                self.auto_print()
                return None

        return None

    def move_knight(self, from_where, to_where):
        if self.get_class(from_where) == 'class.Knight':
            knight = self.board[from_where[0]][from_where[1]]
            if self._check_king(knight, from_where, to_where):
                self.change_its_position(knight, to_where)
                self.whose_turn_it_is.change_turn()
                self.auto_print()
                return None

        return None

    def move_bishop(self, from_where, to_where):
        if self.get_class(from_where) == 'class.Bishop':
            bishop = self.board[from_where[0]][from_where[1]]
            if self._check_king(bishop, from_where, to_where):
                self.change_its_position(bishop, to_where)
                self.whose_turn_it_is.change_turn()
                self.auto_print()
                return None

        return None

    def move_queen(self, from_where, to_where):
        if self.get_class(from_where) == 'class.Queen':
            queen = self.board[from_where[0]][from_where[1]]
            if self._check_king(queen, from_where, to_where):
                self.change_its_position(queen, to_where)
                self.whose_turn_it_is.change_turn()
                self.auto_print()
                return None

        return None

    def move_king(self, from_where, to_where):
        if self.get_class(from_where) == 'class.King':
            king = self.board[from_where[0]][from_where[1]]
            if self._check_king(king, from_where, to_where):
                self.change_its_position(king, to_where)
                self.whose_turn_it_is.change_turn()
                self.auto_print()
            return None

        return None

    def _check_king(self, obj: object, from_where: list, to_where: list) -> bool:
        """ Важный метод для проверки шаха королю. """
        # Выявляет цвет затронутой фигуры.
        piece_touched = my_game.get_color(from_where[0], from_where[1])
        # Проверяет, кому принадлежит ход.
        if my_game.whose_turn_it_is.current_move != piece_touched:
            print('This isn`t your turn. ')
            return False

        # Создаю множество всех ходов
        all_attack_moves = set(sum([value[1] for value in my_game.all_moves.values()], []))

        # Текущие положения королей
        b_king_safe_zone = my_game.all_moves[kings.black_king][0].safe_zone
        w_king_safe_zone = my_game.all_moves[kings.white_king][0].safe_zone

        # Если нужно что-то проверить, то
        # программа никогда не будет работать с реальными данными,
        # поэтому она создает копию доски для всех проверок.
        alternative_board = self

        # Проверка. Король уже находится под шахом?
        if b_king_safe_zone in all_attack_moves:
            # Да. Значит изменяет положение фигуры в копии.
            alternative_board.change_its_position(obj, to_where)
            # Теперь король находится под шахом?
            if b_king_safe_zone in sum([value[1] for value
                                        in alternative_board.all_moves.values()], []):
                print('Black king is under attack!')
                # Да. Сообщение игроку.
                # Не дает сделать ход возвращая False
                return False

            else:
                # Иначе, если король ушел из-под шаха,
                # возвращает True и игрок делает свой ход.
                return True

        # То же самое для белого короля.
        if w_king_safe_zone in all_attack_moves:
            alternative_board.change_its_position(obj, to_where)
            if w_king_safe_zone in sum([value[1] for value in
                                        alternative_board.all_moves.values()], []):
                print('White king is under attack!')
                return False

            else:
                return True

        # Не отработав ни одно
        # условие - все хорошо и можно делать ход.
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
# white_king= my_game.all_moves[kings.white_king][0]
# print(white_king.under_attack)

my_game.move_pawn([6, 4], [4, 4])  # white
my_game.move_pawn([1, 3], [3, 3])  # black
my_game.move_pawn([4, 4], [3, 3])  # white
my_game.move_knight([0, 1], [2, 0]) # black
my_game.move_king([7, 4], [6, 4])  # white

# print(white_king.under_attack)
#
my_game.move_bishop([0, 2], [4, 6])  # black
# print(white_king.under_attack)
#
# my_game.print_board()
# print(white_king.under_attack)
my_game.move_pawn([6, 5], [5, 5])  # white
# my_game.print_board()

my_game.move_queen([7, 3], [7, 4])

# print(white_king.under_attack)

# gen = sum([value[1] for value in my_game.all_moves.values()], [])
# print(white_king.safe_zone in gen )

# my_game.print_board()
# my_game.print_board()
# my_game.move_pawn([6, 1], [5, 1])
# my_game.move_king([6, 4], [7, 4])
#
# print(my_game.board[7][3].moves)
