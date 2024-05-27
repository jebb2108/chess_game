""" Все шахматные фигуры, состояния и их поведение. """
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

    @staticmethod
    def _check_move():
        print('You cannot move an empty space')
        return False


class Piece:
    """ Класс шаблон для шахматной фигуры """
    img = None  # Начальная дефолтная переменная для каждой фигуры.

    def __init__(self, color):  # Каждая фигура должна иметь свой цвет.
        self.color = color  # Программа должна явно указывать Белый или Черный.
        self.enemy_color = None
        self.moves = []

    def __str__(self):
        return self.img[0 if self.color == Color.white else 1]  # Каждая фигура имеет свой
        # кортеж белого и черного цвета фигуры.


class Pawn(Piece):
    """ Класс для пешки """
    img = ('\u265F', '\u2659')  # Кортеж из цветов.

    def __init__(self, y, x, color):
        super().__init__(color)  # Унаследование от родителя атрибутов.
        self.y = y  # Каждая фигура имеет свою координату.
        self.x = x
        self.back_or_forth = None

        self.allowed_moves = 2

    def _get_all_moves(self, board):
        """ Метод, который возвращает все возможные ходы пешки. """
        # Обновляет список переменной экземпляра.
        self.moves.clear()

        # Сохраняет текущую позицию и кол-во ходов в отдельных переменных.
        current_position, current_allowed_moves = (self.y, self.x), self.allowed_moves
        # Возможные ходы пешки и новый, временный список ходов.
        directions, moves = [(1, 0), (1, 1), (1, -1)], []
        for direction in directions:
            # Создает кортеж возможной позиции пешки для проверки условия.
            new_position = (current_position[0] + ((direction[0]) * self.back_or_forth),
                            (1 if current_position[1] + direction[1] < 0 else current_position[1] + direction[1]))  # noqa
            # Значение позиции НЕ может быть отрицательным.
            # Иначе, клетка будет считаться с конца списка!
            # Тернарным выражением я убедился, что значение всегда положительное.

            # Есть два состояния: пешка ходит вперед и пешка съедает.
            # Под каждое состояние - свои условия.
            if direction == (1, 0):
                if current_allowed_moves == 2:
                    # Эта строка отвечает за направление движения и количество ходов.
                    # Последнее значение кортежа идет из предыдущей строки кода.
                    new_position = (self.y + (self.allowed_moves * self.back_or_forth), new_position[1])
                    if self._is_valid_move(board, new_position):
                        moves.extend([new_position])
                        current_allowed_moves = 1
                if current_allowed_moves == 1:
                    # Тот же смысл, как и в прошлом комментарии.
                    # Только количество ходов изменилось на 1.
                    new_position = (self.y + (direction[0] * self.back_or_forth), self.x + direction[1])
                    if self._is_valid_move(board, new_position):
                        moves.extend([new_position])

            # Когда направление пешки уходит в сторону,
            # проверяет наличие вражеской фигуры в стороне.
            else:
                if self._is_valid_move(board, new_position):
                    moves.extend([new_position])

        # Обрати внимание, что в этом методе программа не меняет глобальные значения переменных пешки,
        # а только выводит список ходов конкретного экземпляра исходя из положения всех фигур на доске.
        self.moves.extend(moves)

        # Передает эти ходы в общую свалку
        # всех ходов класса Board !!!
        return self.moves

    def _is_valid_move(self, board, new_position):
        """ Метод для проверки состояния поля на доске."""
        # Если заданная координата не меняется относительно оси X, значит
        # пешка ходит вперед. Она не может занять вражескую позицию.
        if self.x == new_position[1]:
            if board.get_color(new_position[0], new_position[1]) == Color.empty:
                return True
            return False  # Условие не выполняется.
        # Иначе, она съедает вражескую фигуру.
        else:
            if board.get_color(new_position[0], new_position[1]) == self.enemy_color:
                return True
            return False  # Условие не выполняется.

    def _move_pawn(self, board: object, to_where: tuple) -> int or None:
        """ Метод приказывает переместить положение пешки. """

        # Создает кортеж с координатами фигуры.
        from_where = (self.y, self.x)

        # В случае того, когда пешка съедает вражескую фигуру
        # сохраняю enemy_piece_id для нее, чтобы вернуть обратно в метод.
        enemy_piece_id = None

        # Выполняет проверки.
        self._check_move(from_where, to_where)  # Проверка на заданное движение.
        self._get_all_moves(board)  # Получает все возможные ходы.

        # Проверяет, что заданный ход возможен.
        if to_where in self.moves:

            # Изменение динамического атрибута пешки.
            if self.allowed_moves == 2:
                self.allowed_moves = 1

            # Удаление вражеской фигуры из общего списка фигур.
            if board.get_color(to_where[0], to_where[1]) == self.enemy_color:
                enemy_piece_id = id(board.board[to_where[0]][to_where[1]])

            # Манипулирование доской и перемещение пешки.
            temp = board.board[self.y][self.x]
            board.board[to_where[0]][to_where[1]] = temp
            board.board[self.y][self.x] = Empty()

            # Изменение координаты экземпляра.
            self.y, self.x = to_where[0], to_where[1]

            # Обновление списка возможных ходов.
            self._get_all_moves(board)
            return enemy_piece_id

        # Каждый раз проверяет, что пешки
        # находятся на ключевой позиции.
        elif self.y in [0, 7]:
            # Превращение пешки в выбранную фигуру.
            self.__turn_into_piece(board)

        # Возвращать ничего не нужно, т.к. в данном случае
        # переменная доски это просто ссылка на экземпляр.
        return None

    def __turn_into_piece(self, board):
        """ Метод для превращения в выбранную
        фигуру после достижения пешки крайнего поля."""

        # Запоминает цвет фигуры и кладет в переменную.
        if self.color == 1 or 2:
            response = input('Type what piece would you like to have instead? '
                             '"queen", "rock", "knight", or "bishop": ')

            color = Color.white if self.color == 1 else Color.black

            # Сверка ответа.
            if response == 'queen':
                board.board[self.y][self.x] = Empty()
                board.board[self.y][self.x] = Queen(color)
                return board
            if response == 'rock':
                board.board[self.y][self.x] = Empty()
                board.board[self.y][self.x] = Rock(color)  # noqa
                return board
            if response == 'knight':
                board.board[self.y][self.x] = Empty()
                board.board[self.y][self.x] = Knight(color)
                return board
            if response == 'bishop':
                board.board[self.y][self.x] = Empty()
                board.board[self.y][self.x] = Bishop(color)
                return board

            else:  # При непредусмотренном ответе.
                print('Incorrect input')
                return False

        return None

    def _check_move(self, from_where, to_where):
        """ Проверят, если пешка ходит вперед.  """
        if (to_where[0] - from_where[0]) * self.back_or_forth < 0 or from_where[1] != to_where[1]:
            print('You cannot move it backward')
            return False
        if from_where == to_where:
            print('Inappropriate command')
            return False

        return True


class Rock(Piece):
    img = ('\u265C', '\u2656')

    def __init__(self, y, x, color):
        super().__init__(color)
        self.y = y
        self.x = x
        self.enemy_color = Color.white if self.color == 2 else Color.black

    def _get_all_moves(self, board: object) -> list[Any]:
        # Задает переменную с текущим координатами фигуры.
        current_position = (self.y, self.x)
        # Обновляет переменную экземпляра с возможными ходами.
        self.moves.clear()
        # Простой список с направлениями: вниз, вверх, вправо, влево.
        directions, moves = [(1, 0), (-1, 0), (0, 1), (0, -1)], []
        for direction in directions:
            # Каждый раз устанавливает новое положение
            # исходя из текущей, неизменной позиции фигуры.
            new_position = (current_position[0] + direction[0],
                            current_position[1] + direction[1])

            # Цикл продолжает работать пока функция возвращает True.
            while self._is_valid_move(board, new_position):
                # Необходимое условие, если координата стала отрицательной в результате прошлого действия,
                # то происходит инвертирования значения в положительное e.g -1 --> 1.
                if direction[0] + direction[1] < 0 and (new_position[0] < 0 or new_position[1] < 0):
                    # Проверяет, чтобы значение координаты не стало отрицательным
                    # тогда проверка списка начинается с конца, а этого нельзя допустить
                    # иначе произойдет бесконечный цикл.
                    break

                # Вражеская фигура должна стать последней в списке возможных ходов.
                elif board.get_color(new_position[0], new_position[1]) == self.enemy_color:
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

    def _is_valid_move(self, board: object, new_position: tuple) -> bool:
        # Только два возможных условия истинности:
        # либо это поле пустое, либо оно вражеское (последнее)
        if ((board.get_color(new_position[0], new_position[1]) == Color.empty or
             board.get_color(new_position[0], new_position[1]) == self.enemy_color)):
            return True  # Возвращает истинное значение, если поле пустое и не произошла ошибка.

        return False

    def _move_rock(self, board: object, to_where: tuple) -> int or None:
        # Получает все возможные ходы фигуры.
        self._get_all_moves(board)

        enemy_piece_id = None
        # Проверяет, если заданное перемещение присутствует в списке возможных ходов.
        if to_where in self.moves:

            # Удаление вражеской фигуры из общего списка фигур.
            if board.get_color(to_where[0], to_where[1]) == self.enemy_color:
                enemy_piece_id = id(board.board[to_where[0]][to_where[1]])

            # Если да, то происходит перестановка.
            temp = board.board[self.y][self.x]
            board.board[to_where[0]][to_where[1]] = temp
            board.board[self.y][self.x] = Empty()

            # Задает новые координаты переменным экземпляра фигуры.
            self.y, self.x = to_where[0], to_where[1]

            # После сделанного хода, обновляет список возможных ходов.
            self._get_all_moves(board)
            return enemy_piece_id


class Knight(Piece):
    img = ('\u265E', '\u2658')


class Bishop(Piece):
    img = ('\u265D', '\u2657')

    def __init__(self, y, x, color):
        super().__init__(color)
        self.y = y
        self.x = x
        self.enemy_color = Color.white if self.color == 2 else Color.black

    def _get_all_moves(self, board: object) -> list[Any]:
        # Задает переменную с текущим координатами фигуры.
        current_position = (self.y, self.x)
        # Обновляет переменную экземпляра с возможными ходами.
        self.moves.clear()
        # Простой список с направлениями: вниз, вверх, вправо, влево.
        directions, moves = [(1, 1), (-1, 1), (1, -1), (-1, -1)], []
        for direction in directions:
            # Каждый раз устанавливает новое положение
            # исходя из текущей, неизменной позиции фигуры.
            new_position = (current_position[0] + direction[0],
                            current_position[1] + direction[1])


            # Цикл продолжает работать пока функция возвращает True.
            while self._is_valid_move(board, new_position):
                # Необходимое условие, если координата стала отрицательной в результате прошлого действия,
                # то происходит инвертирования значения в положительное e.g -1 --> 1.
                if direction[0] + direction[1] < 0 and (new_position[0] < 0 or new_position[1] < 0):
                    # Проверяет, чтобы значение координаты не стало отрицательным
                    # тогда проверка списка начинается с конца, а этого нельзя допустить
                    # иначе произойдет бесконечный цикл.
                    break

                # Вражеская фигура должна стать последней в списке возможных ходов.
                elif board.get_color(new_position[0], new_position[1]) == self.enemy_color:
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

    def _is_valid_move(self, board: object, new_position: tuple) -> bool:
        # Только два возможных условия истинности:
        # либо это поле пустое, либо оно вражеское (последнее)
        if ((board.get_color(new_position[0], new_position[1]) == Color.empty or
             board.get_color(new_position[0], new_position[1]) == self.enemy_color)):
            return True  # Возвращает истинное значение, если поле пустое и не произошла ошибка.

        return False

    def _move_bishop(self, board: object, to_where: tuple) -> int or None:
        # Получает все возможные ходы фигуры.
        self._get_all_moves(board)

        enemy_piece_id = None
        # Проверяет, если заданное перемещение присутствует в списке возможных ходов.
        if to_where in self.moves:

            # Удаление вражеской фигуры из общего списка фигур.
            if board.get_color(to_where[0], to_where[1]) == self.enemy_color:
                enemy_piece_id = id(board.board[to_where[0]][to_where[1]])

            # Если да, то происходит перестановка.
            temp = board.board[self.y][self.x]
            board.board[to_where[0]][to_where[1]] = temp
            board.board[self.y][self.x] = Empty()

            # Задает новые координаты переменным экземпляра фигуры.
            self.y, self.x = to_where[0], to_where[1]

            # После сделанного хода, обновляет список возможных ходов.
            self._get_all_moves(board)
            return enemy_piece_id


class King(Piece):
    img = ('\u265A', '\u2654')


class Queen(Piece):
    img = ('\u265B', '\u2655')

    def __init__(self, y, x, color):
        super().__init__(color)
        self.y = y
        self.x = x
        self.enemy_color = Color.white if self.color == 2 else Color.black

    def _get_all_moves(self, board: object) -> list[Any]:
        # Задает переменную с текущим координатами фигуры.
        current_position = (self.y, self.x)
        # Обновляет переменную экземпляра с возможными ходами.
        self.moves.clear()
        # Простой список с направлениями: вниз, вверх, вправо, влево.
        directions, moves = [(1, 1), (-1, 1), (1, -1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)], []
        for direction in directions:
            # Каждый раз устанавливает новое положение
            # исходя из текущей, неизменной позиции фигуры.
            new_position = (current_position[0] + direction[0],
                            current_position[1] + direction[1])


            # Цикл продолжает работать пока функция возвращает True.
            while self._is_valid_move(board, new_position):
                # Необходимое условие, если координата стала отрицательной в результате прошлого действия,
                # то происходит инвертирования значения в положительное e.g -1 --> 1.
                if direction[0] + direction[1] < 0 and (new_position[0] < 0 or new_position[1] < 0):
                    # Проверяет, чтобы значение координаты не стало отрицательным
                    # тогда проверка списка начинается с конца, а этого нельзя допустить
                    # иначе произойдет бесконечный цикл.
                    break

                # Вражеская фигура должна стать последней в списке возможных ходов.
                elif board.get_color(new_position[0], new_position[1]) == self.enemy_color:
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

    def _is_valid_move(self, board: object, new_position: tuple) -> bool:
        # Только два возможных условия истинности:
        # либо это поле пустое, либо оно вражеское (последнее)
        if ((board.get_color(new_position[0], new_position[1]) == Color.empty or
             board.get_color(new_position[0], new_position[1]) == self.enemy_color)):
            return True  # Возвращает истинное значение, если поле пустое и не произошла ошибка.

        return False

    def _move_queen(self, board: object, to_where: tuple) -> int or None:
        # Получает все возможные ходы фигуры.
        self._get_all_moves(board)

        enemy_piece_id = None
        # Проверяет, если заданное перемещение присутствует в списке возможных ходов.
        if to_where in self.moves:

            # Удаление вражеской фигуры из общего списка фигур.
            if board.get_color(to_where[0], to_where[1]) == self.enemy_color:
                enemy_piece_id = id(board.board[to_where[0]][to_where[1]])

            # Если да, то происходит перестановка.
            temp = board.board[self.y][self.x]
            board.board[to_where[0]][to_where[1]] = temp
            board.board[self.y][self.x] = Empty()

            # Задает новые координаты переменным экземпляра фигуры.
            self.y, self.x = to_where[0], to_where[1]

            # После сделанного хода, обновляет список возможных ходов.
            self._get_all_moves(board)
            return enemy_piece_id
