""" Все шахматные фигуры, состояния и их поведение. """
import sys
from sys import exception
from typing import Any


class Color(object):
    """ Цвет, состоящий из трех значений,
    является отдельным классом с двумя цветами """

    empty = 0
    white = 1
    black = 2


class Empty(object):
    """ Класс для пустой клетки """
    color = Color.empty

    def __str__(self):
        return '.'

    @staticmethod
    def _get_all_moves():
        return None


class Piece:
    """ Класс шаблон для шахматной фигуры """
    img = None  # Начальная дефолтная переменная для каждой фигуры.

    def __init__(self, color):  # Каждая фигура должна иметь свой цвет.
        self.color = color  # Программа должна явно указывать Белый или Черный.
        self.enemy_color = 1 if self.color == Color.black else 2
        self.is_not_changed = True
        self.moves = []


    def __str__(self):
        return self.img[0 if self.color == Color.white else 1]  # Каждая фигура имеет свой
        # кортеж белого и черного цвета фигуры.

    @staticmethod
    def raise_exception(error_message):
        default_message = 'Please, report it by clicking the button bellow.'
        print(error_message, default_message, sep='\n')
        return sys.exit()


class Pawn(Piece):
    """ Класс для пешки """
    img = ('\u265F', '\u2659')  # Кортеж из цветов.

    def __init__(self, y, x, color):
        super().__init__(color)  # Унаследование от родителя атрибутов.
        self.y, self.x = y, x  # Каждая фигура имеет свою координату.
        self.back_or_forth = None
        # Список вражеских фигур на съедение.
        self.memory = {}
        self.allowed_moves = 2

    def _get_all_moves(self, board_inst):
        """ Метод, который возвращает все возможные ходы пешки. """
        # Обновляет список переменной экземпляра.
        self.moves.clear()

        # Сохраняет текущую позицию и кол-во ходов в отдельных переменных.
        current_position, current_allowed_moves = (self.y, self.x), self.allowed_moves
        # Возможные ходы пешки и новый, временный список ходов.
        directions, moves = [(1, 0), (1, 1), (1, -1)], []
        for direction in directions:
            # Создает кортеж возможной позиции пешки для проверки условия.
            new_position = (current_position[0] + ((direction[0]) * self.back_or_forth),  # noqa
                            (1 if current_position[1] + direction[1] < 0
                             else current_position[1] + direction[1]))  # noqa

            # Значение позиции НЕ может быть отрицательным.
            # Иначе, клетка будет считаться с конца списка!
            # Тернарным выражением я убедился, что значение всегда положительное.

            # Есть два состояния: пешка ходит вперед и пешка съедает.
            # Под каждое состояние - свои условия.
            if direction == (1, 0):
                if current_allowed_moves == 2:
                    # Эта строка отвечает за направление движения и количество ходов.
                    # Последнее значение кортежа идет из предыдущей строки кода.
                    new_position = (self.y + (self.allowed_moves * self.back_or_forth),
                                    new_position[1])  # noqa
                    if self._is_valid_move(board_inst, new_position):
                        moves.extend([new_position])
                        current_allowed_moves = 1
                if current_allowed_moves == 1:
                    # Тот же смысл, как и в прошлом комментарии.
                    # Только количество ходов изменилось на 1.
                    new_position = (self.y + (direction[0] * self.back_or_forth), self.x + direction[1])
                    if self._is_valid_move(board_inst, new_position):
                        moves.extend([new_position])

            # Когда направление пешки уходит в сторону,
            # проверяет наличие вражеской фигуры в стороне.
            else:
                if self._is_valid_move(board_inst, new_position):
                    moves.extend([new_position])

        # Обрати внимание, что в этом методе программа не меняет глобальные значения переменных пешки,
        # а только выводит список ходов конкретного экземпляра исходя из положения всех фигур на доске.
        self.moves.extend(moves)

        # Передает эти ходы в общую свалку
        # всех ходов класса Board !!!
        return self.moves

    def _is_valid_move(self, board_inst, new_position):
        """ Метод для проверки состояния поля на доске."""
        # Если заданная координата не меняется относительно оси X, значит
        # пешка ходит вперед. Она не может занять вражескую позицию.
        if self.x == new_position[1]:
            if board_inst.get_color(new_position[0], new_position[1]) == Color.empty:
                return True
            return False  # Условие не выполняется.
        # Иначе, она съедает вражескую фигуру.
        else:
            if board_inst.get_color(new_position[0], new_position[1]) == self.enemy_color:
                return True
            return False  # Условие не выполняется.

    def _move_object(self, board_inst: object, to_where: tuple) -> int or None:
        """ Метод приказывает переместить положение пешки. """
        # Создает кортеж с координатами фигуры.
        from_where = (self.y, self.x)

        # В случае того, когда пешка съедает вражескую фигуру
        # сохраняю enemy_piece_id для нее, чтобы вернуть обратно в метод.
        # Указатель вражеской пешке, если первая проходит битое поле.
        enemy_piece_tuple, pawn_dirs = None, []

        # Проверка на заданное движение.
        if not self._check_move(board_inst, from_where, to_where): return False

        # Получает все возможные ходы.
        self._get_all_moves(board_inst)  # Получает все возможные ходы.

        # Воспроизводит память.
        if self.memory:
            new_moves = list([move[1] for move in self.memory.values()])
            self.moves.extend(new_moves)

        # Проверяет, что заданный ход возможен.
        if to_where in self.moves:

            if self.memory:
                # Передаю переменной кортежа вражеской фигуры
                # все значения для удаления из общего словаря фигур.
                enemy_piece = next((enemy_pawn[0] for enemy_pawn in self.memory.values() if enemy_pawn[0].x == to_where[1]), None)
                try:
                    enemy_piece_tuple = [id(enemy_piece), enemy_piece, enemy_piece.moves]
                except AttributeError:
                    error_message = 'Problem emerged related to the internal issue.'
                    self.raise_exception(error_message)

                else:
                    # Удаление вражеской фигуры с поля доски
                    # перед непосредственным передвижением данной фигуры.
                    board_inst.board[enemy_piece.y][enemy_piece.x] = Empty()
                    board_inst.make_msg('Eaten in passing')
                    self.memory.clear()

            # Удаление вражеской фигуры из общего словаря фигур.
            elif board_inst.get_color(to_where[0], to_where[1]) == self.enemy_color:
                enemy_piece = board_inst.board[to_where[0]][to_where[1]]
                enemy_piece_tuple = [id(enemy_piece), enemy_piece, enemy_piece.moves]

            # Манипулирование доской и перемещение пешки.
            temp = board_inst.board[self.y][self.x]
            board_inst.board[to_where[0]][to_where[1]] = temp
            board_inst.board[self.y][self.x] = Empty()

            # Изменение координаты экземпляра.
            self.y, self.x = to_where[0], to_where[1]

            # Изменение динамического атрибута пешки.
            if self.allowed_moves == 2 and from_where[1] == to_where[1]:

                new_position_on_side= (self.y, self.x+1)
                if (self.x+1 >= 0
                        and self._is_valid_move(board_inst, new_position_on_side)
                        and board_inst.get_class(new_position_on_side) == 'class.Pawn'):

                    enemy_pawn = board_inst.board[self.y][self.x+1]
                    res = list([self, enemy_pawn, tuple([self.y - (1 * self.back_or_forth), self.x])])
                    board_inst.pawn_dirs.append(res)


                new_position_on_side = (self.y, self.x-1)
                if (self.x - 1 >= 0
                        and self._is_valid_move(board_inst, new_position_on_side)
                        and board_inst.get_class(new_position_on_side) == 'class.Pawn'):

                    enemy_pawn = board_inst.board[self.y][self.x-1]
                    res = list([self, enemy_pawn, tuple([self.y - (1 * self.back_or_forth), self.x])])
                    board_inst.pawn_dirs.append(res)

                self.allowed_moves = 1



            # Каждый раз проверяет, что пешки
            # находятся на ключевой позиции.
            if self.y in [0, 7]:

                # Вывод сообщения
                response = input('Which piece would you like to have instead? '
                                 '"queen", "rock", "knight", or "bishop": ')

                # Проверка на правильность введенных данных.
                while True:

                    valid_responses = ['queen', 'rock', 'knight', 'bishop']

                    if response in valid_responses:
                        break

                    else:
                        response = input('Wrong input. Please try again: ')

                # Превращение пешки в выбранную фигуру.
                self._turn_into_piece(board_inst, response)

            # Обновление списка возможных ходов.
            self._get_all_moves(board_inst)
            return enemy_piece_tuple

        # board_inst.make_msg('E: You cannot move there')
        return False

        # Возвращает id, если есть, иначе возвращает None.

    def _turn_into_piece(self, board_inst: object, response):
        """ Метод для превращения в выбранную
        фигуру после достижения пешки крайнего поля."""

        # Запоминает цвет фигуры и кладет в переменную.
        if self.color in [Color.white, Color.black]:
            color = Color.white if self.color == 1 else Color.black

            piece_mapping = {
                'queen': Queen,
                'rock': Rock,
                'knight': Knight,
                'bishop': Bishop,
            }

            board_inst.board[self.y][self.x] = piece_mapping[response](self.y, self.x, color)

        return None

    def _check_move(self, board_inst: object, from_where, to_where):
        """ Проверят, если пешка ходит вперед.  """
        if (to_where[0] - from_where[0]) * self.back_or_forth < 0 or from_where[1] != to_where[1]:
            if board_inst.get_color(to_where[0], to_where[1]) != self.enemy_color and not self.memory:
                board_inst.make_msg('E: You cannot move this way')
                return False
        if from_where == to_where:
            board_inst.make_msg('E: You have to make a move')
            return False

        return True


class Rock(Piece):
    img = ('\u265C', '\u2656')

    def __init__(self, y, x, color):
        super().__init__(color)
        self.y, self.x = y, x
        self.enemy_color = Color.white if self.color == 2 else Color.black

    def _get_all_moves(self, board_inst: object) -> list[Any]:
        # Задает переменную с текущим координатами фигуры.
        current_position = (self.y, self.x)
        # Обновляет переменную экземпляра с возможными ходами.
        self.moves.clear()
        # Простой список с направлениями: вниз, вверх, вправо, влево.
        directions, moves = [(1, 0), (-1, 0), (0, 1), (0, -1)], []
        for direction in directions:
            # Каждый раз устанавливает новое положение
            # исходя из текущей, неизменной позиции фигуры.
            new_position = (current_position[0] + direction[0],  # noqa
                            current_position[1] + direction[1])

            # Цикл продолжает работать пока функция возвращает True.
            while self._is_valid_move(board_inst, new_position):
                # Необходимое условие, если координата стала отрицательной в результате прошлого действия,
                # то происходит инвертирования значения в положительное e.g -1 --> 1.
                if direction[0] + direction[1] < 0 and (new_position[0] < 0 or new_position[1] < 0):
                    # Проверяет, чтобы значение координаты не стало отрицательным
                    # тогда проверка списка начинается с конца, а этого нельзя допустить
                    # иначе произойдет бесконечный цикл.
                    break

                # Вражеская фигура должна стать последней в списке возможных ходов.
                elif board_inst.get_color(new_position[0], new_position[1]) == self.enemy_color:
                    moves.extend([new_position])
                    break

                else:
                    moves.extend([new_position])
                    # Шаг завершен. Передаю новое значение этой переменной.
                    new_position = (new_position[0] + direction[0],
                                    new_position[1] + direction[1])

        # Возвращает все возможные ходы в список.
        self.moves.extend(moves)
        return self.moves

    def _is_valid_move(self, board_inst: object, new_position: tuple) -> bool:
        # Только два возможных условия истинности:
        # либо это поле пустое, либо оно вражеское (последнее)
        if (board_inst.get_color(new_position[0], new_position[1])
                in [Color.empty, self.enemy_color]):
            return True  # Возвращает истинное значение, если поле пустое и не произошла ошибка.

        return False

    def _move_object(self, board_inst: object, to_where: tuple) -> int or None:
        # Получает все возможные ходы фигуры.
        self._get_all_moves(board_inst)

        enemy_piece_tuple = None
        # Проверяет, если заданное перемещение присутствует в списке возможных ходов.
        if to_where in self.moves:

            # Удаление вражеской фигуры из общего списка фигур.
            if board_inst.get_color(to_where[0], to_where[1]) == self.enemy_color:
                enemy_piece = board_inst.board[to_where[0]][to_where[1]]
                enemy_piece_tuple = (id(enemy_piece), enemy_piece, enemy_piece.moves)

                # Если да, то происходит перестановка.
            temp = board_inst.board[self.y][self.x]
            board_inst.board[to_where[0]][to_where[1]] = temp
            board_inst.board[self.y][self.x] = Empty()

            # Задает новые координаты переменным экземпляра фигуры.
            self.y, self.x = to_where[0], to_where[1]

            # После сделанного хода, обновляет список возможных ходов.
            self._get_all_moves(board_inst)

            self.is_not_changed = False

            return enemy_piece_tuple

        board_inst.make_msg('E: You cannot move there')
        return False


class Knight(Piece):
    img = ('\u265E', '\u2658')

    def __init__(self, y, x, color):
        super().__init__(color)
        self.y, self.x = y, x

    def _get_all_moves(self, board_inst):
        current_position = (self.y, self.x)
        self.moves.clear()
        directions, moves = [(2, 1), (2, -1), (-2, 1),
                             (-2, -1), (1, -2), (1, 2), (-1, 2), (-1, -2)], []
        for direction in directions:
            new_position = (current_position[0] + direction[0], current_position[1] + direction[1])
            if new_position[0] < 0 or new_position[1] < 0:
                continue
            elif self.is_valid_move(board_inst, new_position):
                moves.extend([new_position])
                continue

        self.moves.extend(moves)
        return moves

    def is_valid_move(self, board_inst, new_position):
        if (board_inst.get_color(new_position[0], new_position[1])
                in [Color.empty, self.enemy_color]):
            return True
        return False

    def _move_object(self, board_inst: object, to_where):
        self._get_all_moves(board_inst)  # noqa

        enemy_piece_tuple = None
        if to_where in self.moves:

            if board_inst.get_color(to_where[0], to_where[1]) == self.enemy_color:
                enemy_piece = board_inst.board[to_where[0]][to_where[1]]
                enemy_piece_tuple = [id(enemy_piece), enemy_piece, enemy_piece.moves]

            temp = board_inst.board[self.y][self.x]
            board_inst.board[to_where[0]][to_where[1]] = temp
            board_inst.board[self.y][self.x] = Empty()

            self.y, self.x = to_where[0], to_where[1]
            self._get_all_moves(board_inst)   # noqa
            return enemy_piece_tuple

        board_inst.make_msg('E: You cannot move there')
        return False


class Bishop(Piece):
    img = ('\u265D', '\u2657')

    def __init__(self, y, x, color):
        super().__init__(color)
        self.y, self.x = y, x

    def _get_all_moves(self, board_inst: object) -> list[Any]:

        current_position = (self.y, self.x)
        self.moves.clear()
        directions, moves = [(1, 1), (-1, 1), (1, -1), (-1, -1)], []

        for direction in directions:

            new_position = (current_position[0] + direction[0],
                            current_position[1] + direction[1])

            if new_position[0] < 0 or new_position[1] < 0:
                continue

            while self._is_valid_move(board_inst, new_position):

                if new_position[0] < 0 or new_position[1] < 0:
                    break

                elif board_inst.get_color(new_position[0], new_position[1]) == self.enemy_color:
                    moves.extend([new_position])
                    break

                elif new_position[0] < 0 or new_position[1] < 0:
                    break

                else:
                    moves.extend([new_position])
                    new_position = (new_position[0] + direction[0],
                                    new_position[1] + direction[1])

        self.moves.extend(moves)
        return self.moves

    def _is_valid_move(self, board_inst: object, new_position: tuple) -> bool:
        if (board_inst.get_color(new_position[0], new_position[1])
                in [Color.empty, self.enemy_color]):
            return True

        return False

    def _move_object(self, board_inst: object, to_where: tuple) -> int or None:

        self._get_all_moves(board_inst)
        enemy_piece_tuple = None

        if to_where in self.moves:

            if board_inst.get_color(to_where[0], to_where[1]) == self.enemy_color:
                enemy_piece = board_inst.board[to_where[0]][to_where[1]]
                enemy_piece_tuple = [id(enemy_piece), enemy_piece, enemy_piece.moves]

            temp = board_inst.board[self.y][self.x]
            board_inst.board[to_where[0]][to_where[1]] = temp
            board_inst.board[self.y][self.x] = Empty()

            self.y, self.x = to_where[0], to_where[1]
            self._get_all_moves(board_inst)

            return enemy_piece_tuple

        board_inst.make_msg('E: You cannot move there')
        return False


class Queen(Piece):
    img = ('\u265B', '\u2655')

    def __init__(self, y, x, color):
        super().__init__(color)
        self.y, self.x = y, x

    def _get_all_moves(self, board_inst: object) -> list[Any]:

        current_position = (self.y, self.x)
        self.moves.clear()
        directions, moves = [(1, 1), (-1, 1), (1, -1),
                             (-1, -1), (1, 0), (-1, 0),
                             (0, 1), (0, -1)], []

        for direction in directions:

            new_position = (current_position[0] + direction[0],  # noqa
                            current_position[1] + direction[1])

            if new_position[0] < 0 or new_position[1] < 0:
                continue

            while self._is_valid_move(board_inst, new_position):
                if direction[0] + direction[1] < 0 and (new_position[0] < 0 or new_position[1] < 0):
                    break

                elif board_inst.get_color(new_position[0], new_position[1]) == self.enemy_color:
                    moves.extend([new_position])
                    break

                elif new_position[0] < 0 or new_position[1] < 0:
                    break

                else:
                    moves.extend([new_position])
                    new_position = (new_position[0] + direction[0],
                                    new_position[1] + direction[1])

        self.moves.extend(moves)
        return self.moves

    def _is_valid_move(self, board_inst: object, new_position: tuple) -> bool:
        if (board_inst.get_color(new_position[0], new_position[1])
                in [Color.empty, self.enemy_color]):
            return True

        return False

    def _move_object(self, board_inst: object, to_where: tuple) -> dict or None:

        self._get_all_moves(board_inst)
        enemy_piece_tuple = None

        if to_where in self.moves:

            if board_inst.get_color(to_where[0], to_where[1]) == self.enemy_color:

                enemy_piece = board_inst.board[to_where[0]][to_where[1]]
                enemy_piece_tuple = [id(enemy_piece), enemy_piece, enemy_piece.moves]



            temp = board_inst.board[self.y][self.x]
            board_inst.board[to_where[0]][to_where[1]] = temp
            board_inst.board[self.y][self.x] = Empty()

            self.y, self.x = to_where[0], to_where[1]
            self._get_all_moves(board_inst)
            return enemy_piece_tuple

        board_inst.make_msg('E: You cannot move there')
        return False


class King(Piece):
    img = ('\u265A', '\u2654')

    def __init__(self, y, x, color):
        super().__init__(color)
        self.y, self.x = y, x
        self.safe_zone = (self.y, self.x)

    def _get_all_moves(self, board_inst):

        self.moves.clear()

        current_position = (self.y, self.x)
        directions, moves = [(1, 0), (-1, 0), (0, 1),
                             (0, -1), (1, 1), (1, -1),
                             (-1, 1), (-1, -1)], []

        for direction in directions:
            new_position = (current_position[0] + direction[0],
                            current_position[1] + direction[1])

            if new_position[0] < 0 or new_position[1] < 0:
                continue

            elif self.is_valid_move(board_inst, new_position):
                moves.extend([new_position])

        self.moves.extend(moves)
        return moves

    def is_valid_move(self, board_inst: object, new_position):

        if (board_inst.get_color(new_position[0], new_position[1])
                in [Color.empty, self.enemy_color]):
            return True

        return False

    def _move_object(self, board_inst, to_where):

        self._get_all_moves(board_inst)
        enemy_piece_tuple = None

        if to_where in self.moves:

            if board_inst.get_color(to_where[0], to_where[1]) == self.enemy_color:
                enemy_piece = board_inst.board[to_where[0]][to_where[1]]
                enemy_piece_tuple = [id(enemy_piece), enemy_piece, enemy_piece.moves]

            temp = board_inst.board[self.y][self.x]
            board_inst.board[to_where[0]][to_where[1]] = temp
            board_inst.board[self.y][self.x] = Empty()

            self.y, self.x = to_where[0], to_where[1]
            self.safe_zone = (self.y, self.x)
            self._get_all_moves(board_inst)

            # Не позволяет королю сделать
            # рокировку после сделанного хода.
            self.is_not_changed = False

            return enemy_piece_tuple

        board_inst.make_msg('E: You cannot move there')
        return False
