from board import *
from settings import *


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


class GamePlay:
    """ Класс самого высокого уровня,
    с чем непосредственно взаимодействует пользователь. """

    def __init__(self):
        self.whose_turn_it_is = WhoMoves()
        self.actions = BoardUser()
        self.settings = Settings()
        self.default_message = True
        self.message = 'Press "q" to quit'
        self.current_move_message = 'Turn to play: white'
        self.first_beginning_message = 'What do you want to move: (e.g. "e2") '
        self.second_beginning_message = 'To where do you want to move it: (e.g. "e4") '

        self.object_copies = list()

    def start_game(self):

        self.actions.print_board()

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
                print('options: dictionary for moves "d"; stats for each piece "s"')
                response = input('What would you like to see: ')
                if response == 'd':
                    gen1 = [move[1] for move in self.actions.all_poss_moves.values()]
                    gen2 = [move[2] for move in self.actions.all_poss_moves.values()]
                    for item in zip(gen1, gen2):
                        print(item)
                elif response == 's':
                    for key in self.actions.all_poss_moves.values():
                        print(repr(key[0]))
                        print()

            to_where_input = input('{}'.format(self.second_beginning_message))
            if to_where_input[0].lower() == 'q' or len(to_where_input) < 2:
                print('\nThe session is over')
                break

            from_where_input = from_where_input[0].title() + from_where_input[1]
            to_where_input = to_where_input[0].title() + to_where_input[1]

            # Переводит в числовые координаты 'E2' --> [6, 4]
            # Если координаты некорректные, выдает ошибку.
            try:
                from_where = self.actions.settings.transcripts[from_where_input]
                to_where = self.actions.settings.transcripts[to_where_input]
                from_where, to_where = tuple(from_where), tuple(to_where)

            except KeyError:
                self.make_msg('E: You mistyped. Please try again')
                self.actions.print_board()

            # Маленькая проверка на то, чтобы это была фигуры.
            # Передает в следующую функцию.
            else:
                self.actions.chosen_piece_object = self.actions.pick_piece(from_where)
                self.move_piece(to_where)
                print()

    def is_end_game(self, color_indx):

        checkmate_status = False

        if self.is_checked():
            checkmate_status = True

        while checkmate_status:

            # game_stats = copy.deepcopy(my_game)
            board_copy = copy.deepcopy(self.actions.board)
            game_stats = GamePlay()
            game_stats.actions = BoardUser(board_copy)

            tmp = game_stats.get_moves()

            for piece, moves in tmp:

                curr_pos = list([piece.y, piece.x])

                for new_move in moves:
                    # Функция, которая изменяет доску в новом экземпляре.
                    game_stats.actions.conduct_change(new_move)
                    # Обновляет возможные ходы в словаре после перестановки
                    game_stats.actions.update_enemy_pieces_moves(game_stats, piece.enemy_color)

                    if game_stats.is_checked(color_indx):
                        game_stats.actions.conduct_change(curr_pos)

                    else:
                        checkmate_status = False
                        break

            del game_stats, board_copy

            if checkmate_status is True:
                print('\tCheckmate!')
                return False

        return True

    def move_piece(self, to_where):

        move_mapping = {
            King: self.actions.check_castling_and_move(to_where),
        }

        # Проверяет, если игрок хочет провести рокировку.
        if move_mapping.get(self.actions.chosen_piece_object, False):
            self.whose_turn_it_is.change_turn()
            self.make_msg('Castling your king went successful')
            self.actions.update_all_poss_moves_dict()
            return self.auto_print()

        # Следующее условие. Это не король. Совершает обычный ход
        elif self.check_king(to_where):
            # Требуется убрать проверки т.к они уже сделаны в check_king функциях
            if self.place_piece_on_board(to_where):
                self.whose_turn_it_is.change_turn()
                self.auto_print()
                self.actions.update_all_poss_moves_dict()
                return self.actions.print_board()

        return self.actions.print_board()

    def check_king(self, to_where: list) -> bool:
        """ Важный метод для проверки шаха королю. """
        # Проверяет, кому принадлежит ход.
        if my_game.whose_turn_it_is.current_move != self.actions.chosen_piece_color:
            self.make_msg('This isn`t your turn')
            return False

        # Проверка. Король находится под шахом?
        if self.is_checked():
            if self.king_remains_checked(to_where):
                return True
            else:
                return False

        return True

    def place_piece_on_board(self, to_where):
        # Если шаха не зафиксировано,
        # программа пытается переместить фигуру на доске.
        temp_res = self.actions.attempt_piece_to_move(to_where)

        # Если результат отрицательный,
        # происходит выброс из цикла действий.
        if temp_res is False: return False
        if temp_res not in [True, None]:  # Иначе проверяет, есть ли другое значение от булевых?
            removed_piece_id = temp_res[0]
            removed_piece = temp_res[1]
            # Перемещает экземпляр во временное хранилище - список.
            self.object_copies.extend([removed_piece])

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
                self.actions.all_poss_moves[removed_piece_id] = (removed_piece, [])
                self.actions.conduct_force_change(to_where, self.actions.chosen_piece_object.loc, self.object_copies[-1])
                self.object_copies.clear()
                # Проверка не пройдена. Возвращает False.
                return False

        return True

    def post_check_king(self, to_where):
        """ Проверка на шах уже после сделанного хода. """

        if self.is_checked():
            # Возвращает фигуру на место.
            self.actions.chosen_piece_object.moves.clear()
            self.actions.conduct_force_change(to_where, self.actions.chosen_piece_object.loc,
                                      self.object_copies[-1] if self.object_copies else None)
            self.make_msg(f'{('White', 'Black')[self.actions.chosen_piece_color.color - 1]} king is under attack!')
            # Очищает резервное хранилище.
            self.object_copies.clear()
            return False

        self.object_copies.clear()
        return True

        # Позволяет пройти проверку.

    def king_remains_checked(self, to_where):

        # from_where = self.chosen_piece_object.loc

        res = self.actions.attempt_piece_to_move(to_where)

        if res is False:
            return False

        elif res not in [True, None]:
            # Создает копию съеденной фигуры в резерве
            removed_piece = res[1]
            self.object_copies.append(removed_piece)

        # Король теперь в опасности?
        if self.is_not_checked():  # noqa
            self.make_msg(f'{('White', 'Black')[self.actions.chosen_piece_color - 1]} king is under attack!')
            if self.object_copies:
                self.actions.conduct_force_change(to_where, self.actions.chosen_piece_object.loc, self.object_copies)
                if not isinstance(self.object_copies[-1], object):
                    self.actions.all_poss_moves[res[0]] = (self.object_copies[-1], [])
                    self.object_copies.clear()
                return False

            else:
                self.actions.conduct_force_change(to_where, self.actions.chosen_piece_object.loc)
                return False

        return self.post_check_king(obj, from_where, to_where, color_indx)  # noqa

    def get_moves(self):
        gen_moves = [[move[0], list(move[1])] for move in self.actions.all_poss_moves.values() if
                     move[0].color == self.actions.chosen_piece_color]
        array = list(gen_moves)
        return array

    def make_msg(self, e=''):
        """ Подставляет сообщение об ошибке. """
        self.message = e
        self.default_message = False
        pass

    def auto_print(self):
        """Вспомогательная функция для печати доски и коррекции сообщений."""

        if not self.default_message:
            self.current_move_message = 'Turn to play: {}'.format(
                'white' if self.whose_turn_it_is.current_move == 1 else 'black')
            self.actions.print_board()
            return None


        else:
            self.message = 'Press "q" to press'
            self.current_move_message = 'Turn to play: {}'.format(
                'white' if self.whose_turn_it_is.current_move == 1 else 'black')
            self.actions.print_board()
            return None

    def process_deleted_item(self, item):
        removed_piece_id = item[0]
        removed_piece = item[1]
        # Перемещает экземпляр во временное хранилище - список.
        self.object_copies.extend([removed_piece])
        return removed_piece_id, removed_piece

    def is_checked(self, chessboard_inst=None) -> [True or False]:
        """ Проверка, если король находится в зоне атаки вражеской фигуры. """

        if chessboard_inst is None:
            chessboard_inst = self

        try:
            color = 'white' if chessboard_inst.chosen_piece_color == 1 else 'black'
        except AttributeError:
            return False

        if color == 'black':
            black_king_id = next((key for key, item in chessboard_inst.all_poss_moves.items() if
                                  item[0].color == 2 and isinstance(item[0], King)), None)
            return (chessboard_inst.all_poss_moves[black_king_id][0].safe_zone
                    in set(sum([value[1] if value[0].color == 1 else value[1] for value in
                                chessboard_inst.all_poss_moves.values()], [])))


        elif color == 'white':
            white_king_id = next((key for key, item in chessboard_inst.all_poss_moves.items() if
                                  item[0].color == 1 and isinstance(item[0], King)), None)
            return (chessboard_inst.all_poss_moves[white_king_id][0].safe_zone
                    in set(sum([value[1] if value[0].color == 2 else value[1] for value in
                                chessboard_inst.all_poss_moves.values()], [])))


# Приказывает Python не гулять по библиотекам, а принимать этот файл за главный.
if __name__ == '__main__':
    my_game = GamePlay()
    my_game.start_game()
