

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
        self.current_move_message = 'Turn to play: white'
        self.first_beginning_message = 'What do you want to move: (e.g. "e2") '
        self.second_beginning_message = 'To where do you want to move it: (e.g. "e4") '

    def start_game(self):

        self.print_board()


        while True:

            print(self.message)
            print('***', str(self.current_move_message), '***')
            from_where_input = input('{}'.format(self.first_beginning_message))
            if from_where_input[0].lower() == 'q' or len(from_where_input) < 2:
                print('\nThe session is over')
                break

            elif from_where_input == 'h+':
                # gen0 = [(move[0].y, move[0].x) for move in self.all_moves.values()]
                gen1 = [move[1] for move in self.all_moves.values()]
                gen2 = [move[2] for move in self.all_moves.values()]
                for item in zip(gen1, gen2):
                    print(item)

            from_where_input = from_where_input[0].title() + from_where_input[1]

            to_where_input = input('{}'.format(self.second_beginning_message))
            if to_where_input[0].lower() == 'q' or len(to_where_input) < 2:
                print('\nThe session is over')
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
                self.move_piece(res, from_where, to_where)
                print()



    def move_piece(self, res, from_where, to_where):

        if res == 'Empty':
            self.make_msg('Wrong input')
            return self.print_board()

        piece = self.board[from_where[0]][from_where[1]]

        if self._check_king(piece, from_where, to_where):
            print('level 1')
            if self.post_check_king(piece, from_where, to_where):
                print('level 2', kings.object_copies)
                self.whose_turn_it_is.change_turn()
                self.auto_print()
                return None


        print('level 0. Operation went wrong.')
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
        if self.is_under_attack('black'):

            # Да. Значит изменяет положение фигуры в копии.
            removed_piece = self.change_its_position(obj, to_where)
            kings.object_copies.append(removed_piece if type(removed_piece) is not None else())
            print('Check. Level 1')

            # Белый король теперь в опасности?
            if self.is_under_attack('black'):  # noqa

                self.make_msg('White king is under attack!')

                print('Check. Level 2. False')

                self.force_change(obj, to_where, from_where,
                                  kings.object_copies)

                if kings.object_copies:
                    self.all_moves[removed_piece[0]] = (kings.object_copies[-1], [])
                    kings.object_copies.clear()

                return False


            else:


                # Иначе, проверка пройдена.
                # Переходит к следующему этапу.
                return True


        # То же самое для белого короля.
        elif self.is_under_attack('white'):

            res = self.change_its_position(obj, to_where)
            if res not in [False, None]:
                removed_piece = res[1]
                kings.object_copies.extend(removed_piece)

            print(kings.object_copies)
            print('Check. Level 1')

            # Белый король теперь в опасности?
            if self.is_under_attack('white'):  # noqa

                self.make_msg('White king is under attack!')

                print('Check. Level 2. False', kings.object_copies)

                self.force_change(obj, to_where, from_where, kings.object_copies if kings.object_copies != [] else None)

                if kings.object_copies:
                    if not isinstance(kings.object_copies[-1], object):
                        self.all_moves[res[0]] = (kings.object_copies[-1], [])
                        kings.object_copies.clear()

                return False



        else:

                # Иначе, проверка пройдена.
                # Переходит к следующему этапу.
                return True


        # Сохраняю возвращенный элемент в переменную класса King.
        temp_res = self.change_its_position(obj, to_where)
        kings.object_copies.append(temp_res[1]) if type(temp_res) is not bool else None

        # После первоначальной проверки, делаю ход
        # и если ход позволяет, делаю ход изменяя доску.
        if temp_res:

                # Последняя проверка.
                return True

        # При отрицательном результате
        # останавливается и выводит False.
        return False


    def post_check_king(self, obj, from_where, to_where):

        if self.is_under_attack('black') and obj.color == 2:

            # Ничего не вышло.
            # Обновляю список ходов.
            # Возвращаю ход
            obj.moves.clear()
            self.force_change(obj, to_where, from_where, kings.object_copies[-1] if kings.object_copies else None)
            self.make_msg('Black king is under attack!')

            # Обновляет.
            kings.object_copies.clear()

            # Останавливает.
            return False

        if self.is_under_attack('white') and obj.color == 1:

            # Те же проверки, но теперь с белым королем.
            obj.moves.clear()
            self.force_change(obj, to_where, from_where, kings.object_copies[-1] if kings.object_copies else None)
            self.make_msg('White king is under attack!')

            # Обновляет.
            kings.object_copies.clear()

            # Останавливает.
            return False

        # Очищает 'кэш' фигур.
        if self.change_its_position(obj, to_where):
            print('Done.')
            return True

    def is_under_attack(self, color):

        if color == 'black':

            return (self.all_moves[kings.black_king][0].safe_zone
                    in set(sum([value[1] if value[0].color == 1 else value[1] for value in self.all_moves.values()], [])))

        elif color == 'white':

            return (self.all_moves[kings.white_king][0].safe_zone
                    in set(sum([value[1] if value[0].color == 2 else value[1] for value in self.all_moves.values()], [])))


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
