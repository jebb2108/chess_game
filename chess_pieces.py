""" Класс для шахматных фигур """


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

    def _check_move(self, *args):
        print('You cannot move an empty space')
        return False


class ChainedArray(object):
    allowed = True  # Будет полезным при дальнейшей работе с королем,

    # когда нужно будет отключать всем эту опцию

    def __init__(self):
        self.root = None
        self.next = None


class Piece:
    """ Класс шаблон для шахматной фигуры """
    img = None  # Начальная дефолтная переменная для каждой фигуры.

    def __init__(self, color):  # Каждая фигура должна иметь свой цвет.
        self.all_moves = []
        self.color = color  # Программа должна явно указывать Белый или Черный.
        self.enemy_color = None
        self.moves = []

    def __str__(self):
        return self.img[0 if self.color == Color.white else 1]  # Каждая фигура имеет свой
        # кортеж белого и черного цвета фигуры.


class Pawn(Piece):
    """ Класс для пешки """
    img = ('\u265F', '\u2659')  # Кортеж из цветов.
    allowed_moves = 2  # Количество ходов для первого хода.

    def __init__(self, y, x, color):
        super().__init__(color)  # Унаследование от родителя атрибутов.
        self.y = y  # Каждая фигура имеет свою координату.
        self.x = x
        self.root = [y, x]

    def _get_all_moves(self):
        pass

    def _move_pawn(self, board, from_where, to_where, direction):
        """ Условия перемещения пешки и последующее отображение ее на доске """
        # Первое условие -- есть цвет (не ноль). Второе, фигура
        # находится на доске. Третье, след-щее не является пустым.
        if self.color and from_where[0] < 7 and board.get_color(from_where[0] + (direction * 1),
                                                                from_where[1]) == Color.empty:

            # Проверяет на сколько далеко пешка
            # может ходить и направление перемещения.
            if self.allowed_moves >= (to_where[0] - from_where[0]) * direction:
                # Если условие выполнено, то происходит перестановка экземпляров.
                # Так же обновляю переменные этого экземпляра.
                temp = board.board[from_where[0]][from_where[1]]
                board.board[from_where[0]][from_where[1]] = Empty()
                board.board[to_where[0]][to_where[1]] = temp
                self.y, self.x = to_where[0], to_where[1]
                self.allowed_moves = 1
                # Последнее условие -- не находится ли пешка на краю доски?
                # В этом случае, запускает инкапсулированный метод превращения.
                if ((self.color == 2 and from_where[0] == 6 and to_where[0] == 7)
                        or (self.color == 1 and from_where[0] == 1 and to_where[0] == 0)):
                    self.__turn_into_piece(board)
                    return board
                return board
            else:
                return print('You cannot move so far')
        else:
            return print('Your pawn is blocked.')

    def _eat_by_pawn(self, board, from_where, to_where, direction):
        """ Метод для поедания вражеской фигуры """

        # Исключительное условие передвижения с выкинутой ошибкой.  ТРЕБУЕТ ДОРАБОТКИ!
        if (to_where[0] - from_where[0]) * direction < 0 or (to_where[1] - from_where[1]) not in [1, -1]:
            return print('You can`t go and eat the enemy piece with this distance')
        else:
            # При выполненном условии, происходит типичная перестановка.
            board.board[to_where[0]][to_where[1]] = board.board[from_where[0]][from_where[1]]
            board.board[from_where[0]][from_where[1]] = Empty()
            return board

    def __turn_into_piece(self, board):
        """ Метод для превращения в выбранную
        фигуру после достижения пешки крайнего поля."""

        # Запоминает цвет фигуры и кладет в переменную.
        color = Color.white if self.color == 1 else Color.black
        if self.color == 1 or 2:
            response = input('Type what piece would you like to have instead? '
                             '"queen", "rock", "knight", or "bishop": ')

            # Сверка ответа.
            if response == 'queen':
                board.board[self.y][self.x] = Empty()
                board.board[self.y][self.x] = Queen(color)
                return board
            elif response == 'rock':
                board.board[self.y][self.x] = Empty()
                board.board[self.y][self.x] = Rock(color)
                return board
            elif response == 'knight':
                board.board[self.y][self.x] = Empty()
                board.board[self.y][self.x] = Knight(color)
                return board
            elif response == 'bishop':
                board.board[self.y][self.x] = Empty()
                board.board[self.y][self.x] = Bishop(color)
                return board

            else:  # При непредусмотренном ответе.
                print('Incorrect input')
                return False

    @staticmethod
    def _check_move(from_where, to_where, direction):
        """ Проверят, если пешка ходит вперед.  """
        if (to_where[0] - from_where[0]) * direction < 0 or from_where[1] != to_where[1]:
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
        self.root = [y, x]
        self.enemy_color = Color.white if self.color == 2 else Color.black

    def _get_rock_moves(self, board: object, current_position: tuple, moves=None) -> list:

        if moves is None:
            moves = []

        # Обновляет переменную экземпляра с возможными ходами.
        self.moves.clear()
        # Простой список с направлениями: вниз, вверх, вправо, влево.
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
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

                    # if enemy_piece:  # Здесь программа понимает, что нужно сделать исключение
                #     #  и добавить это поле, как исключение, чтобы можно было сбить фигуру.
                #     moves.extend([new_position])
                #     enemy_piece = False
                #     break

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

    def _move_rock(self, board: object, from_where: tuple, to_where: tuple) -> object:
        # Получает все возможные ходы фигуры.
        self._get_rock_moves(board, from_where)
        # Проверяет, если заданное перемещение присутствует в списке возможных ходов.
        if to_where in self.moves:
            # Если да, то происходит перестановка.
            temp = board.board[from_where[0]][from_where[1]]
            board.board[from_where[0]][from_where[1]] = Empty()
            board.board[to_where[0]][to_where[1]] = temp

            # Задает новые координаты переменным экземпляра фигуры.
            self.y = to_where[0]
            self.x = to_where[1]

            # После сделанного хода, обновляет список возможных ходов.
            self._get_rock_moves(board, to_where)
            print('You successfully moved your rock')

            # Возвращает измененную доску.
            return board


class Knight(Piece):
    img = ('\u265E', '\u2658')


class Bishop(Piece):
    img = ('\u265D', '\u2657')


class King(Piece):
    img = ('\u265A', '\u2654')


class Queen(Piece):
    img = ('\u265B', '\u2655')
