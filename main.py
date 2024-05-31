import copy
from pprint import pprint

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
        self.message = 'Press "q" to quit'
        self.current_move_message = 'Turn to play: white'
        self.first_beginning_message = 'What do you want to move: (e.g. "e2") '
        self.second_beginning_message = 'To where do you want to move it: (e.g. "e4") '


    def start_game(self):

        self.print_board()

        while True:

            print(self.message)
            print('***', str(self.current_move_message), '***')
            from_where_input = input('{}'.format(self.first_beginning_message))
            if from_where_input[0].lower() == 'q':
                break

            elif from_where_input == 'h+':
                # gen0 = [(move[0].y, move[0].x) for move in self.all_moves.values()]
                gen1 = [move[1] for move in self.all_moves.values()]
                gen2 = [move[2] for move in self.all_moves.values()]
                for item in zip(gen1, gen2):
                    print(item)

            from_where_input = from_where_input[0].title() + from_where_input[1]

            to_where_input = input('{}'.format(self.second_beginning_message))
            if to_where_input[0].lower() == 'q':
                break
            to_where_input = to_where_input[0].title() + to_where_input[1]

            try:
                from_where = self.settings.transcripts[from_where_input]
                to_where = self.settings.transcripts[to_where_input]
            except KeyError:
                self.make_msg('E: You mistyped. Please try again')
                self.print_board()

            else:
                res = self.get_class(from_where)
                self.choose_action(res, from_where, to_where)
                print()

    def choose_action(self, res, from_where, to_where):

        if res == 'class.Pawn':
            self.move_pawn(from_where, to_where)
        elif res == 'class.Rock':
            self.move_rock(from_where, to_where)
        elif res == 'class.Knight':
            self.move_knight(from_where, to_where)
        elif res == 'class.Bishop':
            self.move_bishop(from_where, to_where)
        elif res == 'class.Queen':
            self.move_queen(from_where, to_where)
        elif res == 'class.King':
            self.move_king(from_where, to_where)
        else:
            self.make_msg('Wrong input')
            return self.print_board()

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
                return None

        return self.print_board()

    def move_rock(self, from_where, to_where):
        rock = self.board[from_where[0]][from_where[1]]
        if self._check_king(rock, from_where, to_where):
            if self.change_its_position(rock, to_where):
                self.whose_turn_it_is.change_turn()
                self.auto_print()
                return None

        return self.print_board()

    def move_knight(self, from_where, to_where):
        knight = self.board[from_where[0]][from_where[1]]
        if self._check_king(knight, from_where, to_where):
            if self.change_its_position(knight, to_where):
                self.whose_turn_it_is.change_turn()
                self.auto_print()
                return None

        return self.print_board()

    def move_bishop(self, from_where, to_where):
        bishop = self.board[from_where[0]][from_where[1]]
        if self._check_king(bishop, from_where, to_where):
            if self.change_its_position(bishop, to_where):
                self.whose_turn_it_is.change_turn()
                self.auto_print()
                return None

        return self.print_board()

    def move_queen(self, from_where, to_where):
        queen = self.board[from_where[0]][from_where[1]]
        if self._check_king(queen, from_where, to_where):
            if self.change_its_position(queen, to_where):
                self.whose_turn_it_is.change_turn()
                self.auto_print()
                return None

        return self.print_board()

    def move_king(self, from_where, to_where):
        king = self.board[from_where[0]][from_where[1]]
        if self._check_king(king, from_where, to_where):
            if self.change_its_position(king, to_where):
                self.whose_turn_it_is.change_turn()
                self.auto_print()
                return None

        return self.print_board()

    def _check_king(self, obj: object, from_where: list, to_where: list) -> bool:
        """ Важный метод для проверки шаха королю. """
        # Выявляет цвет затронутой фигуры.
        piece_touched = my_game.get_color(from_where[0], from_where[1])
        # Проверяет, кому принадлежит ход.
        if my_game.whose_turn_it_is.current_move != piece_touched:
            self.make_msg('This isn`t your turn')
            return False

        # Проверка. Черный король находится под шахом?
        # Создаю множество ходов всех белых фигур.
        if self.all_moves[kings.black_king][0].safe_zone in set(sum([value[1] if value[0].color == 1
                                                                     else value[1] for value in
                                                                     self.all_moves.values()], [])):
            # Да. Значит изменяет положение фигуры в копии.
            if_deleted = self.change_its_position(obj, to_where)
            all_attack_moves = set(sum([value[1] for value in self.all_moves.values()], []))
            # Теперь король находится под шахом?
            if self.all_moves[kings.black_king][0].safe_zone in set(sum([value[1] if value[0].color == 1
                                                                         else value[1] for value in
                                                                         self.all_moves.values()], [])):
                # Да. Сообщение игроку.
                # Не дает сделать ход возвращая False
                self.make_msg('Black king is under attack!')

                if if_deleted is True:
                    if_deleted = None

                self.force_change(obj, to_where, from_where, if_deleted)

                return False

            else:
                # Иначе, если король ушел из-под шаха,
                # возвращает True и игрок делает свой ход.
                return True

        # То же самое для белого короля.
        # Создаю множество ходов всех черных фигур.
        if self.all_moves[kings.white_king][0].safe_zone in set(sum([value[1] if value[0].color == 2
                                                                     else value[1] for value in
                                                                     self.all_moves.values()], [])):  # noqa
            if_deleted = self.change_its_position(obj, to_where)

            # Белый король теперь в опасности?
            if self.all_moves[kings.white_king][0].safe_zone in set(sum([value[1] if value[0].color == 2
                                                                         else value[1] for value in
                                                                         self.all_moves.values()], [])):  # noqa

                self.make_msg('White king is under attack!')

                if if_deleted is True:
                    if_deleted = None

                self.force_change(obj, to_where, from_where, if_deleted)

                return False

            else:
                return True

        # Не отработав ни одно
        # условие - все хорошо и можно делать ход.
        return True

    def make_msg(self, e):
        self.message = e

    def auto_print(self):

        self.message = 'Press "q" to quit'

        self.current_move_message = 'Turn to play: {}'.format(
            'white' if self.whose_turn_it_is.current_move == 1 else 'black')

        self.print_board()

        self.first_beginning_message = self.first_beginning_message[:26]
        self.second_beginning_message = self.second_beginning_message[:33]


# Приказывает Python не гулять по библиотекам, а принимать этот файл за главный.
if __name__ == '__main__':
    my_game = GamePlay()
    kings = King()
    my_game.start_game()
