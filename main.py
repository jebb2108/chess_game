import copy
from pprint import *
from typing import Any

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

        # Временная переменная для всех значений возвращаемых фигур.
        self.object_copies = list()


class GamePlay(Board):
    """ Класс самого высокого уровня,
    с чем непосредственно взаимодействует пользователь. """

    def __init__(self):
        super().__init__()
        self.whose_turn_it_is = WhoMoves()
        self.message = 'Press "q" to quit'
        self.default_message = True
        self.current_move_message = 'Turn to play: white'
        self.first_beginning_message = 'What do you want to move: (e.g. "e2") '
        self.second_beginning_message = 'To where do you want to move it: (e.g. "e4") '

    def start_game(self):

        self.print_board()

        while True:

            if not self.is_end_game(self.whose_turn_it_is.current_move): break

            print(self.message)
            if not self.default_message:
                self.default_message = True

            print('***', str(self.current_move_message), '***')
            from_where_input = input('{}'.format(self.first_beginning_message))
            if from_where_input[0].lower() == 'q' or len(from_where_input) < 2:
                print('\nWhite wins!' if self.whose_turn_it_is.current_move == 2 else '\nBlack wins!')
                break

            # Команда разработчика.
            elif from_where_input == 'h+':
                # gen0 = [(move[0].y, move[0].x) for move in self.all_moves.values()]
                gen1 = [move[1] for move in self.all_moves.values()]
                gen2 = [move[2] for move in self.all_moves.values()]
                for item in zip(gen1, gen2):
                    print(item)

            to_where_input = input('{}'.format(self.second_beginning_message))
            if to_where_input[0].lower() == 'q' or len(to_where_input) < 2:
                print('\nThe session is over')
                break

            elif from_where_input == 'attack' or to_where_input == 'attack':
                self.get_attacker()
                self.print_board()
                continue

            from_where_input = from_where_input[0].title() + from_where_input[1]
            to_where_input = to_where_input[0].title() + to_where_input[1]

            # Переводит в числовые координаты 'E2' --> [6, 4]
            # Если координаты некорректные, выдает ошибку.
            try:
                from_where = self.settings.transcripts[from_where_input]
                to_where = self.settings.transcripts[to_where_input]

            except KeyError:
                self.make_msg('E: You mistyped. Please try again')
                self.print_board()

            # Маленькая проверка на то, чтобы это была фигуры.
            # Передает в следующую функцию.
            else:
                cls = self.get_class(from_where)
                self.move_piece(cls, from_where, to_where)
                print()

    def get_attacker(self):
        for piece in self.all_moves.values():
            if self.all_moves[kings.white_king][0].safe_zone in piece[1] if piece[0].color != 1 else ():
                return self.make_msg(f'The white king is under attack by {piece[0]}')
            if self.all_moves[kings.black_king][0].safe_zone in piece[1] if piece[0].color != 2 else ():
                return self.make_msg(f'The black king is under attack by {piece[0]}')

        return self.make_msg('No one threatens the king')

    def is_end_game(self, color_indx):

        checkmate_status = False

        if self.is_checked(self, color_indx):
            checkmate_status = True


        while checkmate_status:

            game_stats = copy.deepcopy(my_game)
            board_copy = copy.copy(game_stats.board)
            movies_copy = copy.copy(game_stats.all_moves)
            new_board = Board(board_copy, movies_copy)

            tmp = game_stats.get_moves(new_board, color_indx)


            for piece, moves in tmp:

                curr_pos = list([piece.y, piece.x])

                for move in moves:
                    # Функция, которая изменяет доску в новом экземпляре.
                    new_board.change_board(new_board, piece, curr_pos, move)
                    # Обновляет возможные ходы в словаре после перестановки
                    new_board.update_enemy_pieces_moves(new_board, piece.enemy_color)

                    if game_stats.is_checked(new_board, color_indx):
                        new_board.change_board(new_board, piece, move, curr_pos)

                    else:

                        checkmate_status = False

            if checkmate_status is True:
                print('\tCheckmate!')
                return False


        return True

    def move_piece(self, cls, from_where, to_where):

        if cls == 'Empty':
            self.make_msg('E: You cannot move an empty space')
            return self.print_board()

        piece = self.board[from_where[0]][from_where[1]]  # object

        # Проверяет, если игрок хочет провести рокировку.
        if self.check_castle(piece, from_where, to_where):
            # Переходит на уровень ниже и пытается совершить ее.
            if self.castle_king(piece, to_where):
                # В случае успеха, производит обновление терминала.
                self.whose_turn_it_is.change_turn()
                self.auto_print('Castling your king went successful')
                self._update_moves_dict()
                return None

            else:

                # Иначе, выводит сообщение об ошибке.
                self.make_msg('Impossible to castle your king')
                return self.print_board()

        # Следующее условие -- совершает обычный ход
        elif self.check_king(piece, from_where, to_where, piece.color):
            self.whose_turn_it_is.change_turn()
            self.auto_print()
            self._update_moves_dict()
            return None

        return self.print_board()

    def check_castle(self, piece, from_where, to_where):
        """ Простейшая проверка на возможную рокировку. """
        if self.get_class(from_where) == 'class.King':
            if from_where[0] == to_where[0] and to_where[1] in [2, 6]:
                if piece.is_not_changed:
                    return True

        return False

    def check_king(self, obj: object, from_where: list, to_where: list, color_indx: int) -> bool:
        """ Важный метод для проверки шаха королю. """

        # Выявляет цвет затронутой фигуры.
        piece_touched = my_game.get_color(from_where[0], from_where[1])
        # Проверяет, кому принадлежит ход.

        if my_game.whose_turn_it_is.current_move != piece_touched:
            self.make_msg('This isn`t your turn')
            return False

        # Проверка. Черный король находится под шахом?
        # Создаю множество ходов всех белых фигур.
        if self.is_checked(self, color_indx):
            if self.remains_checked(obj, from_where, to_where, color_indx):
                return True
            else:
                return False

        # Если шаха не зафиксировано,
        # программа пытается переместить фигуру на доске.
        temp_res = self.change_its_position(obj, to_where)

        # Если результат отрицательный,
        # происходит выброс из цикла действий.
        if temp_res is False: return False
        if temp_res not in [True, None]:  # Иначе проверяет, есть ли другое значение от булевых?
            removed_piece_id = temp_res[0]
            removed_piece = temp_res[1]
            # Перемещает экземпляр во временное хранилище - список.
            kings.object_copies.extend([removed_piece])

            # Так как изменения на доске уже произошли,
            # проверяет, есть ли шах королю сейчас?
            if self.post_check_king(obj, from_where, to_where, color_indx):  # noqa

                # Проверка выполнена.
                # Фигура остается в той же позиции
                # и съеденная вражеская фигура удаляется.
                return True

            else:
                # Король остается под шахом.
                # Возвращает фигуру на место.
                # Удаленная фигура возвращается
                # в хранилище из резервного списка.
                self.all_moves[removed_piece_id] = (removed_piece, [])
                self.force_change(obj, to_where, from_where, kings.object_copies[-1])
                kings.object_copies.clear()
                # Проверка не пройдена. Возвращает False.
                return False

        # Это поле служит на случай,
        # если res вернулось булево значение:
        # True или (редко) None
        else:

            # Два возможных исхода после последней проверки.
            # Помните, что передвижение уже выполнено.
            if self.post_check_king(obj, from_where, to_where, color_indx):  # noqa
                return True

            else:
                # Обратите внимание, что программа
                # не возвращает ничего в аргумент removed_piece.
                self.force_change(obj, to_where, from_where)
                return False

    def post_check_king(self, obj, from_where, to_where, color_indx):
        """ Проверка на шах уже после сделанного хода. """

        if self.is_checked(self, color_indx):

            # Ничего не вышло.
            # Обновляю список ходов.
            # Возвращаю ход
            obj.moves.clear()
            self.force_change(obj, to_where, from_where, kings.object_copies[-1] if kings.object_copies else None)
            self.make_msg(f'{('White', 'Black')[obj.color-1]} king is under attack!')

            # Обновляет.
            kings.object_copies.clear()

            # Останавливает.
            return False

        kings.object_copies.clear()
        return True

        # Позволяет пройти проверку.

    def remains_checked(self, obj, from_where, to_where, color_indx):
        # Король в опасности?
        # if self.is_under_attack(color_indx):

        res = self.change_its_position(obj, to_where)

        if res is False:
            return False

        elif res not in [True, None]:
            removed_piece = res[1]
            kings.object_copies.extend([removed_piece])

        # Король теперь в опасности?
        if self.is_checked(self, color_indx):  # noqa

            self.make_msg(f'{('White', 'Black')[obj.color-1]} king is under attack!')

            if kings.object_copies:
                self.force_change(obj, to_where, from_where, kings.object_copies)

                if not isinstance(kings.object_copies[-1], object):
                    self.all_moves[res[0]] = (kings.object_copies[-1], [])
                    kings.object_copies.clear()

                return False

            else:
                self.force_change(obj, to_where, from_where)
                return False

        return self.post_check_king(obj, from_where, to_where, color_indx)  # noqa


    def get_moves(self, obj, color_indx):
        gen_moves = [[move[0], list(move[1])] for move in obj.all_moves.values() if move[0].color == color_indx]
        array = list(gen_moves)
        return array


    def make_msg(self, e):
        """ Подставляет сообщение об ошибке. """
        self.message = e
        self.default_message = False

    def auto_print(self, given_message=None):
        """Вспомогательная функция для печати доски и коррекции сообщений."""

        if not self.default_message:

            if given_message:
                self.message = given_message
                self.current_move_message = 'Turn to play: {}'.format(
                    'white' if self.whose_turn_it_is.current_move == 1 else 'black')
                self.print_board()
                return None

            else:
                self.current_move_message = 'Turn to play: {}'.format(
                    'white' if self.whose_turn_it_is.current_move == 1 else 'black')
                self.print_board()
                return None


        else:
            self.message = 'Press "q" to press'
            self.current_move_message = 'Turn to play: {}'.format(
                'white' if self.whose_turn_it_is.current_move == 1 else 'black')
            self.print_board()
            return None

    @staticmethod
    def is_checked(chessboard_inst, color_indx: int) -> [True or False]:
        """ Проверка, если король находится в зоне атаки вражеской фигуры. """

        color = 'white' if color_indx == 1 else 'black'

        if color == 'black':
            return (chessboard_inst.all_moves[kings.black_king][0].safe_zone
                    in set(sum([value[1] if value[0].color == 1 else value[1] for value in chessboard_inst.all_moves.values()], [])))

        elif color == 'white':
            return (chessboard_inst.all_moves[kings.white_king][0].safe_zone
                    in set(sum([value[1] if value[0].color == 2 else value[1] for value in chessboard_inst.all_moves.values()], [])))



# Приказывает Python не гулять по библиотекам, а принимать этот файл за главный.
if __name__ == '__main__':
    my_game = GamePlay()
    kings = King()
    my_game.start_game()
