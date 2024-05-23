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


class Piece:
    """ Класс шаблон для шахматной фигуры """
    img = None  # Начальная дефолтная переменная для каждой фигуры.

    def __init__(self, color):  # Каждая фигура должна иметь свой цвет.
        self.color = color  # Программа должна явно указывать Белый или Черный.

    def __str__(self):
        return self.img[0 if self.color == Color.white else 1]  # Каждая фигура имеет свой
        # кортеж белого и черного цвета фигуры.


class Pawn(Piece):
    """ Класс для пешки """
    img = ('\u265F', '\u2659')  # Кортеж из цветов.
    allowed_moves = 2  # Количество ходов для первого хода.

    def __init__(self, x, y, color):
        super().__init__(color)  # Унаследование от родителя атрибутов.
        self.x = x  # Каждая фигура имеет свою координату.
        self.y = y

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

    def __init__(self, x, y, color):
        super().__init__(color)
        self.x = x
        self.y = y


class Knight(Piece):
    img = ('\u265E', '\u2658')


class Bishop(Piece):
    img = ('\u265D', '\u2657')


class King(Piece):
    img = ('\u265A', '\u2654')


class Queen(Piece):
    img = ('\u265B', '\u2655')