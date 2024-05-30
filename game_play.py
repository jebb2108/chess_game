import copy

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
        self.message = 'Turn to play: '

    def start_game(self):
        while True:
            self.auto_print()
            print()
            print('Press "q" to quit')
            print(self.message, 'white' if self.whose_turn_it_is.current_move == 1 else 'black')
            from_where_input = input('What do you want to move: ')
            if from_where_input[0].lower() == 'q':
                break
            from_where_input = from_where_input[0].title() + from_where_input[1]

            to_where_input = input('To where do you want to move it: ')
            if to_where_input[0].lower() == 'q':
                break
            to_where_input = to_where_input[0].title() + to_where_input[1]

            try:
                from_where = self.settings.transcripts[from_where_input]
                to_where = self.settings.transcripts[to_where_input]
            except KeyError:
                print('You mistyped. Please try again.')

            else:
                res = self.get_class(from_where)
                self.choose_action(res, from_where, to_where)
                print()

    def choose_action(self, res, from_where, to_where):
        if res == 'class.Pawn':
            self.move_pawn(from_where, to_where)
        if res == 'class.Rock':
            self.move_rock(from_where, to_where)
        if res == 'class.Knight':
            self.move_knight(from_where, to_where)
        if res == 'class.Bishop':
            self.move_bishop(from_where, to_where)
        if res == 'class.Queen':
            self.move_queen(from_where, to_where)
        if res == 'class.King':
            self.move_king(from_where, to_where)
        else:
            return False

    def move_pawn(self, from_where: list, to_where: list):
        # Каждый этот метод по сути проверяет,
        # выбрал ли пользователь правильную команду.
        # Передаю подконтрольный экземпляр переменной.
        pawn = self.board[from_where[0]][from_where[1]]
        # Следующие методы проверяет, находится ли король под шахом.
        # Если нет или это не ход игрока с битым королем, то
        # позволяет передвинуть фигуру ниже уровнем,
        # затем ход передается другому и печатает доску.
        if self._check_king(pawn, from_where, to_where):
            if self.change_its_position(pawn, to_where):
                self.whose_turn_it_is.change_turn()
                self.auto_print()
                print('here...')
                return None

        return print('Something went wrong processing your input.')

    def move_rock(self, from_where, to_where):
        rock = self.board[from_where[0]][from_where[1]]
        if self._check_king(rock, from_where, to_where):
            if self.change_its_position(rock, to_where):
                self.whose_turn_it_is.change_turn()
                self.auto_print()

        return print('Something went wrong processing your input.')

    def move_knight(self, from_where, to_where):
        if self.get_class(from_where) == 'class.Knight':
            knight = self.board[from_where[0]][from_where[1]]
            if self._check_king(knight, from_where, to_where):
                self.change_its_position(knight, to_where)
                self.whose_turn_it_is.change_turn()
                self.auto_print()

        return print('Something went wrong processing your input.')

    def move_bishop(self, from_where, to_where):
        bishop = self.board[from_where[0]][from_where[1]]
        if self._check_king(bishop, from_where, to_where):
            if self.change_its_position(bishop, to_where):
                self.whose_turn_it_is.change_turn()
                self.auto_print()

        return print('Something went wrong processing your input.')

    def move_queen(self, from_where, to_where):
        queen = self.board[from_where[0]][from_where[1]]
        if self._check_king(queen, from_where, to_where):
            if self.change_its_position(queen, to_where):
                self.whose_turn_it_is.change_turn()
                self.auto_print()

        return print('Something went wrong processing your input.')

    def move_king(self, from_where, to_where):
        king = self.board[from_where[0]][from_where[1]]
        if self._check_king(king, from_where, to_where):
            if self.change_its_position(king, to_where) is not False:
                self.whose_turn_it_is.change_turn()
                self.auto_print()

        return print('Something went wrong processing your input.')

    def _check_king(self, obj: object, from_where: list, to_where: list) -> bool:
        """ Важный метод для проверки шаха королю. """
        # Выявляет цвет затронутой фигуры.
        piece_touched = my_game.get_color(from_where[0], from_where[1])
        # Проверяет, кому принадлежит ход.
        if my_game.whose_turn_it_is.current_move != piece_touched:
            print('This isn`t your turn. ')
            return False



        # Если нужно что-то проверить, то
        # программа никогда не будет работать с реальными данными,
        # поэтому она создает копию доски для всех проверок.
        alternative_board = self.copy_object(self)

        # Создаю множество всех ходов
        all_attack_moves = set(sum([value[1] for value in alternative_board.all_moves.values()], []))

        # Текущие положения королей
        b_king = next((value[0] for value in alternative_board.all_moves.values()
                                  if alternative_board.get_class([value[0].y, value[0].x]) == 'class.King' and value[0].color == 2), None)  # noqa
        b_king_safe_zone = (b_king.y, b_king.x)

        w_king = next((value[0] for value in alternative_board.all_moves.values()
                                  if alternative_board.get_class([value[0].y, value[0].x]) == 'class.King' and value[0].color == 1), None)  # noqa
        w_king_safe_zone = (w_king.y, w_king.x)

        # Проверка. Король уже находится под шахом?
        if b_king_safe_zone in all_attack_moves:
            # Да. Значит изменяет положение фигуры в копии.
            alternative_board.change_its_position(obj, to_where)
            # Теперь король находится под шахом?
            if b_king_safe_zone in set(sum([value[1] for value
                                            in alternative_board.all_moves.values()], [])):
                print('Black king is under attack!')
                # Да. Сообщение игроку.
                # Не дает сделать ход возвращая False
                del alternative_board
                return False

            else:
                # Иначе, если король ушел из-под шаха,
                # возвращает True и игрок делает свой ход.
                del alternative_board
                return True

        # То же самое для белого короля.
        if w_king_safe_zone in all_attack_moves:
            alternative_board.change_its_position(obj, to_where)
            if w_king_safe_zone in set(sum([value[1] for value in
                                            alternative_board.all_moves.values()], [])):
                print('White king is under attack!')
                del alternative_board
                return False

            else:
                del alternative_board
                return True

        # Не отработав ни одно
        # условие - все хорошо и можно делать ход.
        # if [w_king_safe_zone, b_king_safe_zone] not in all_attack_moves:
        #     return True
        # else:
        #     return False
        del alternative_board
        return True

    @staticmethod
    def copy_object(obj):
        copied = copy.deepcopy(obj)
        return copied

    @staticmethod
    def auto_print():
        my_game.print_board()


# Приказывает Python не гулять по библиотекам, а принимать этот файл за главный.
if __name__ == '__main__':
    my_game = GamePlay()
    kings = King()
    my_game.start_game()
