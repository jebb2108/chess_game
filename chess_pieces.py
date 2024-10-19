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

    def __init__(self, loc: tuple[int, int], color: object):  # Каждая фигура должна иметь свой цвет.
        self.loc = loc
        self.color = color  # Программа должна явно указывать Белый или Черный.
        self.enemy_color = 1 if self.color == Color.black else 2
        self.is_not_changed = True
        self.enemy_to_delete = None
        self.moves = list()

    @property
    def loc(self):
        return self.__loc

    @loc.setter
    def loc(self, loc):
        if loc[0] < 0 or loc[0] > 7 or loc[1] < 0 or loc[1] > 7:
            raise Exception('Wrong location!')

        self.__loc = loc

    def _get_y(self):
        return self.__loc[0]

    def _get_x(self):
        return self.__loc[1]

    def _set_loc(self, loc):
        self.__loc = loc

    def _generate_linear_moves(self, board_inst: object, array_dirs):
        curr_pos, moves = self.loc, list()
        for dir in array_dirs:
            # Каждый раз устанавливает новое положение
            # исходя из текущей, неизменной позиции фигуры.
            new_pos = (curr_pos[0] + dir[0],  # noqa
                            curr_pos[1] + dir[1])

            # Цикл продолжает работать пока функция возвращает True.
            while self.__is_valid_move(board_inst, new_pos):
                # Необходимое условие, если координата стала отрицательной в результате прошлого действия,
                # то происходит инвертирования значения в положительное e.g -1 --> 1.
                if dir[0] + dir[1] < 0 and (new_pos[0] < 0 or new_pos[1] < 0):
                    # Проверяет, чтобы значение координаты не стало отрицательным
                    # тогда проверка списка начинается с конца, а этого нельзя допустить
                    # иначе произойдет бесконечный цикл.
                    break

                # Вражеская фигура должна стать последней в списке возможных ходов.
                elif board_inst.get_color(new_pos[0], new_pos[1]) == self.enemy_color:
                    moves.extend([new_pos])
                    break

                else:
                    moves.extend([new_pos])
                    # Шаг завершен. Передаю новое значение этой переменной.
                    new_pos = (new_pos[0] + dir[0],
                                    new_pos[1] + dir[1])

        return moves

    def _finish_move(self, board_inst: object, to_where: tuple):
        self.__check_enemy_for_removal(board_inst, to_where)
        self.__put_piece_on_board_into_loc(board_inst, to_where)
        self._set_loc((to_where[0], to_where[1]))
        return None

    def __put_piece_on_board_into_loc(self, board_inst: object, to_where: tuple):
        """ Перемещает фигуру на доску по переданным координатам. """
        temp = board_inst.board[self._get_y()][self._get_x()]
        board_inst.board[to_where[0]][to_where[1]] = temp
        board_inst.board[self._get_y()][self._get_x()] = Empty()

    def __check_enemy_for_removal(self, board_inst: object, to_where: tuple):
        """ Проверяет на наличие вражеской фигуры по заданной координате. """
        if board_inst.get_color(to_where[0], to_where[1]) == self.enemy_color:
            enemy_piece = board_inst.board[to_where[0]][to_where[1]]
            self.enemy_to_delete = (id(enemy_piece), enemy_piece, enemy_piece.moves)
            return self.enemy_to_delete

        self.enemy_to_delete = None
        return None

    def __is_valid_move(self, board_inst: object, new_position: tuple) -> bool:
        # Только два возможных условия истинности:
        # либо это поле пустое, либо оно вражеское (последнее)
        if (board_inst.get_color(new_position[0], new_position[1])
                in [Color.empty, self.enemy_color]):
            return True  # Возвращает истинное значение, если поле пустое
                         # и не произошла ошибка.
        return False



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

    def __init__(self, loc, color, back_or_forth=None):
        self.allowed_moves = 2
        self.ways_to_go = [(1, 0), (1, 1), (1, -1)]
        self.back_or_forth = back_or_forth
        # Список вражеских фигур на съедение.
        self.memory = {}

        super().__init__(loc, color)  # Унаследование от родителя атрибутов.

    def _get_all_moves(self, board_inst):
        """ Метод, который возвращает все возможные ходы пешки. """
        # Обновляет список переменной экземпляра.
        self.moves.clear()

        # Сохраняет текущую позицию и кол-во ходов в отдельных переменных.
        curr_pos, curr_allowed_moves = self.loc, self.allowed_moves
        # Возможные ходы пешки и новый, временный список ходов.
        moves = []
        for dir in self.ways_to_go:
            # Создает кортеж возможной позиции пешки для проверки условия.
            new_pos = (curr_pos[0] + ((dir[0]) * self.back_or_forth),  # noqa
                            (1 if curr_pos[1] + dir[1] < 0
                             else curr_pos[1] + dir[1]))  # noqa

            # Значение позиции НЕ может быть отрицательным.
            # Иначе, клетка будет считаться с конца списка!
            # Тернарным выражением я убедился, что значение всегда положительное.

            # Есть два состояния: пешка ходит вперед и пешка съедает.
            # Под каждое состояние - свои условия.
            if dir == (1, 0):
                if curr_allowed_moves == 2:
                    # Эта строка отвечает за направление движения и количество ходов.
                    # Последнее значение кортежа идет из предыдущей строки кода.
                    new_pos = (self._get_y() + (self.allowed_moves * self.back_or_forth),
                                    new_pos[1])  # noqa
                    if self._is_valid_move(board_inst, new_pos):
                        moves.extend([new_pos])
                        curr_allowed_moves = 1

                if curr_allowed_moves == 1:
                    # Тот же смысл, как и в прошлом комментарии.
                    # Только количество ходов изменилось на 1.
                    new_pos = (self._get_y() + (dir[0] * self.back_or_forth),
                                    self._get_x() + dir[1])
                    if self._is_valid_move(board_inst, new_pos):
                        moves.extend([new_pos])

            # Когда направление пешки уходит в сторону,
            # проверяет наличие вражеской фигуры в стороне.
            else:
                if self._is_valid_move(board_inst, new_pos):
                    moves.extend([new_pos])

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
        if self._get_x() == new_position[1]:
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
        from_where = self.loc
        # В случае того, когда пешка съедает вражескую фигуру
        # сохраняю enemy_piece_id для нее, чтобы вернуть обратно в метод.
        # Указатель вражеской пешке, если первая проходит битое поле.
        pawn_dirs = []

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
                enemy_piece = next((enemy_pawn[0] for enemy_pawn in self.memory.values() if enemy_pawn[0]._get_x() == to_where[1]), None)
                try:
                    self.enemy_to_delete = [id(enemy_piece), enemy_piece, enemy_piece.moves]
                except AttributeError:
                    error_message = 'Problem emerged related to the internal issue.'
                    self.raise_exception(error_message)

                else:
                    # Удаление вражеской фигуры с поля доски
                    # перед непосредственным передвижением данной фигуры.
                    board_inst.board[enemy_piece._get_y()][enemy_piece._get_x()] = Empty()
                    board_inst.make_msg('Eaten in passing')
                    self.memory.clear()

            # Изменение динамического атрибута пешки.
            self._check_by_passing_enemy_pawns(board_inst, from_where, to_where)
            self._is_at_the_edge(board_inst)
            self._finish_move(board_inst, to_where)
            # Обновление списка возможных ходов.
            self._get_all_moves(board_inst)
            return self.enemy_to_delete

        # board_inst.make_msg('E: You cannot move there')
        return False

    def _check_by_passing_enemy_pawns(self, board_inst: object, from_where: tuple, to_where: tuple):
        if self.allowed_moves == 2 and (from_where[1] == to_where[1]):

            new_position_on_side = (self._get_y(), self._get_x() + 1)
            if (self._get_x() + 1 >= 0
                    and self._is_valid_move(board_inst, new_position_on_side)
                    and board_inst.get_class(new_position_on_side) == 'class.Pawn'):
                enemy_pawn = board_inst.board[self._get_y()][self._get_x() + 1]
                res = list([self, enemy_pawn, tuple([self._get_y() - (1 * self.back_or_forth),
                                                     self._get_x()])])
                board_inst.pawn_dirs.append(res)

            new_position_on_side = (self._get_y(), self._get_x() - 1)
            if (self._get_x() - 1 >= 0
                    and self._is_valid_move(board_inst, new_position_on_side)
                    and board_inst.get_class(new_position_on_side) == 'class.Pawn'):
                enemy_pawn = board_inst.board[self._get_y()][self._get_x() - 1]
                res = list([self, enemy_pawn, tuple([self._get_y() - (1 * self.back_or_forth),
                                                     self._get_x()])])
                board_inst.pawn_dirs.append(res)

            self.allowed_moves = 1
            return board_inst

        return None

    def _is_at_the_edge(self, board_inst: object):
        # Каждый раз проверяет, что пешки
        # находятся на ключевой позиции.
        if self._get_y() in [0, 7]:
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
            return self.__turn_into_piece(board_inst, response)

        return None


    def __turn_into_piece(self, board_inst: object, response):
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

            board_inst.board[self._get_y()][self._get_x()] = (
                piece_mapping[response](self._get_y(), self._get_x(), color))

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

    def __init__(self, loc, color):
        self.ways_to_go = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        super().__init__(loc, color)

    def _get_all_moves(self, board_inst: object) -> list[Any]:
        # Задает переменную с текущим координатами фигуры.
        current_position = self.loc
        # Обновляет переменную экземпляра с возможными ходами.
        self.moves.clear()
        # Простой список с направлениями: вниз, вверх, вправо, влево.
        resulted_moves = self._generate_linear_moves(board_inst, self.ways_to_go)

        # Возвращает все возможные ходы в список.
        self.moves.extend(resulted_moves)
        return self.moves

    def _move_object(self, board_inst: object, to_where: tuple) -> int or None:
        # Получает все возможные ходы фигуры.
        self._get_all_moves(board_inst)
        # Проверяет, если заданное перемещение присутствует в списке возможных ходов.
        if to_where in self.moves:

            # Удаление вражеской фигуры из общего списка фигур.
            self._finish_move(board_inst, to_where)
            self._get_all_moves(board_inst)
            return self.enemy_to_delete

        board_inst.make_msg('E: You cannot move there')
        return False


class Knight(Piece):
    img = ('\u265E', '\u2658')

    def __init__(self, loc, color):
        self.ways_to_go = [(2, 1), (2, -1), (-2, 1),
                             (-2, -1), (1, -2), (1, 2), (-1, 2), (-1, -2)]
        super().__init__(loc, color)

    def _get_all_moves(self, board_inst):
        self.moves.clear()
        curr_pos,temp_moves = self.loc, list()
        for dir in self.ways_to_go:
            new_pos = (curr_pos[0] + dir[0], curr_pos[1] + dir[1])
            if new_pos[0] < 0 or new_pos[1] < 0:
                continue
            elif self.__is_valid_move(board_inst, new_pos):
                temp_moves.extend([new_pos])
                continue

        self.moves.extend(temp_moves)
        return self.moves

    def _move_object(self, board_inst: object, to_where):
        self._get_all_moves(board_inst)  # noqa
        if to_where in self.moves:
            self._finish_move(board_inst, to_where)
            self._get_all_moves(board_inst)   # noqa
            return self.enemy_to_delete

        board_inst.make_msg('E: You cannot move there')
        return False


class Bishop(Piece):
    img = ('\u265D', '\u2657')

    def __init__(self, loc, color):
        self.ways_to_go = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        super().__init__(loc, color)

    def _get_all_moves(self, board_inst: object) -> list[Any]:
        self.moves.clear()
        resulted_moves = self._generate_linear_moves(board_inst, self.ways_to_go)
        self.moves.extend(resulted_moves)
        return self.moves

    def _move_object(self, board_inst: object, to_where: tuple) -> int or None:
        self._get_all_moves(board_inst)
        if to_where in self.moves:
            self._finish_move(board_inst, to_where)
            self._get_all_moves(board_inst)
            return self.enemy_to_delete

        board_inst.make_msg('E: You cannot move there')
        return False


class Queen(Piece):
    img = ('\u265B', '\u2655')

    def __init__(self, loc, color):
        self.ways_to_go = [(1, 1), (-1, 1), (1, -1),
                             (-1, -1), (1, 0), (-1, 0),
                             (0, 1), (0, -1)]
        super().__init__(loc, color)

    def _get_all_moves(self, board_inst: object) -> list[Any]:
        self.moves.clear()
        resulted_moves = self._generate_linear_moves(board_inst, self.ways_to_go)
        self.moves.extend(resulted_moves)

        return self.moves

    def _move_object(self, board_inst: object, to_where: tuple) -> dict or None:

        self._get_all_moves(board_inst)

        if to_where in self.moves:
            self._finish_move(board_inst, to_where)
            self._get_all_moves(board_inst)
            return self.enemy_to_delete

        board_inst.make_msg('E: You cannot move there')
        return False


class King(Piece):
    img = ('\u265A', '\u2654')

    def __init__(self, loc, color):
        self.ways_to_go = [(1, 0), (-1, 0), (0, 1),
                             (0, -1), (1, 1), (1, -1),
                             (-1, 1), (-1, -1)]
        super().__init__(loc, color)
        self.safe_zone = self.loc

    def _get_all_moves(self, board_inst):
        self.moves.clear()
        curr_pos, temp_moves = self.loc, list()
        for dir in self.ways_to_go:
            new_pos = (curr_pos[0] + dir[0],
                            curr_pos[1] + dir[1])

            if new_pos[0] < 0 or new_pos[1] < 0:
                continue

            elif self.__is_valid_move(board_inst, new_pos):
                temp_moves.extend([new_pos])

        self.moves.extend(temp_moves)
        return temp_moves

    def _move_object(self, board_inst, to_where):
        self._get_all_moves(board_inst)
        if to_where in self.moves:
            self._finish_move(board_inst, to_where)
            self._get_all_moves(board_inst)
            self.safe_zone = self.loc
            # Не позволяет королю сделать
            # рокировку после сделанного хода.
            self.is_not_changed = False
            return self.enemy_to_delete

        board_inst.make_msg('E: You cannot move there')
        return False
