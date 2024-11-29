import pygame
from abc import ABC, abstractmethod

from core_files.pixels import pixel_mapping

""" Все шахматные фигуры, состояния и их поведение. """

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

class BoardManipulator(ABC):

    @staticmethod
    def get_class(board, coords):
        coord_y, coord_x = coords
        class_mapping = {
            Pawn: 'class.Pawn',
            Rock: 'class.Rock',
            Knight: 'class.Knight',
            Bishop: 'class.Bishop',
            Queen: 'class.Queen',
            King: 'class.King'
        }
        piece = board[coord_y][coord_x]
        return class_mapping.get(type(piece), 'Empty')

    @staticmethod
    def get_color(board, coords):
        coord_y, coord_x = coords
        try:
            color = board[coord_y][coord_x].color
        except IndexError:
            return None
        return color

    @staticmethod
    def update_board_list(board_list: list, curr_pos, new_pos: tuple, color: int):
        this_enemy = BoardManipulator.__check_enemy_for_removal(board_list, new_pos, color)
        BoardManipulator.__put_piece_on_board_into_loc(board_list, curr_pos, new_pos)
        return this_enemy

    @staticmethod
    def __put_piece_on_board_into_loc(board_list: list, curr_pos: tuple, new_pos: tuple):
        """ Перемещает фигуру на доску по переданным координатам. """
        curr_y, curr_x = curr_pos
        new_y, new_x = new_pos
        temp = board_list[curr_y][curr_x]
        board_list[new_y][new_x] = temp
        board_list[curr_y][curr_x] = Empty()
        return None

    @staticmethod
    def __check_enemy_for_removal(board_list: list, new_pos: tuple, color: int):
        """ Проверяет на наличие вражеской фигуры по заданной координате. """
        new_y, nex_x = new_pos
        if BoardManipulator.get_color(board_list, new_pos) == color:
            enemy = board_list[new_y][nex_x]
            return enemy

        return False

class Piece(ABC):
    """ Класс шаблон для шахматной фигуры """
    sounds_loaded = False
    capture_sound = None
    illegal_sound = None
    move_sound = None
    castling_sound = None

    # Каждая фигура должна иметь свой цвет.
    def __init__(self, window, loc: tuple[int, int], color: object):
        self.window = window
        self.loc = loc
        self.color = color  # Программа должна явно указывать Белый или Черный.
        self.id = self.__hash__()
        self.alien_id = None

        if not Piece.sounds_loaded:
            Piece.capture_sound = pygame.mixer.Sound('sounds/capture.mp3')
            Piece.move_sound = pygame.mixer.Sound('sounds/move-self.mp3')
            Piece.illegal_sound = pygame.mixer.Sound('sounds/illegal.mp3')
            Piece.castling_sound = pygame.mixer.Sound('sounds/castle.mp3')
            Piece.sounds_loaded = True

        self.enemy_color = 1 if self.color == Color.black else 2
        path = (('white', 'black')[self.color-1]  # noqa
                     + '_' + self.__class__.__name__ + '.png')
        self.image = pygame.image.load('images/' + path)
        self.is_not_changed = True
        self.moves = list()


    @property
    def loc(self):
        return self.__loc

    @loc.setter
    def loc(self, loc):
        if loc[0] < 0 or loc[0] > 7 or loc[1] < 0 or loc[1] > 7:
            raise Exception('Wrong location!')

        self.__loc = loc

    def get_color(self):
        return self.color

    def get_id(self):
        return self.id

    def get_y(self):
        return self.__loc[0]

    def get_x(self):
        return self.__loc[1]

    def set_loc(self, loc: tuple):
        self.__loc = loc


    def clicked_inside(self, mouse_pos):
        first_x, first_y = pixel_mapping[self.loc]
        this_rect = pygame.rect.Rect(first_x, first_y, 55, 55)
        clicked = this_rect.collidepoint(mouse_pos)
        if clicked:
            # self.clicked_sound.play()
            return True
        else:
            return False


    @abstractmethod
    def _get_all_moves(self, board_list: object):
        return NotImplementedError

    @abstractmethod
    def _move_object(self, to_where: list, board_list: list):
        return NotImplementedError


    def _prep_moves(self, board_list: list, array_dirs):
        curr_pos, moves = self.loc, list()
        for d1r in array_dirs:
            # Каждый раз устанавливает новое положение
            # исходя из текущей, неизменной позиции фигуры.
            new_pos = (curr_pos[0] + d1r[0],  # noqa
                            curr_pos[1] + d1r[1])

            if (new_pos[0] < 0 or new_pos[1] < 0) or \
                    (new_pos[0] > 7 or new_pos[1]) > 7:

                continue

            # Цикл продолжает работать пока функция возвращает True.
            while self._is_valid_move(board_list, new_pos):

                # Вражеская фигура должна стать последней в списке возможных ходов.
                if BoardManipulator.get_color(board_list, new_pos) == self.enemy_color:
                    moves.append(new_pos)
                    break

                else:
                    moves.append(new_pos)
                    # Шаг завершен. Передаю новое значение этой переменной.
                    new_pos = (new_pos[0] + d1r[0],
                                    new_pos[1] + d1r[1])

        return moves


    def _is_valid_move(self, board_list: list, new_pos: tuple) -> bool:
        # Только два возможных условия истинности:
        # либо это поле пустое, либо оно вражеское (последнее)
        if BoardManipulator.get_color(board_list, new_pos) in [Color.empty, self.enemy_color]:
            return True  # Возвращает истинное значение, если поле пустое
                         # и не произошла ошибка.
        return False


    def access_all_moves(self):
        return list(self.moves)


    def _finish_move(self, board_list: list, new_pos: tuple):
        BoardManipulator.update_board_list(board_list, self.loc, new_pos, self.enemy_color)
        self.set_loc(new_pos)
        # self.move_sound.play()
        self.is_not_changed = False
        return


    def draw(self):
        screen_loc = pixel_mapping[self.loc]
        self.window.blit(self.image, screen_loc)

class Pawn(Piece, ABC):
    """ Класс пешки """
    def __init__(self, window, loc, color, back_or_forth):
        self.allowed_moves = 2
        self.ways_to_go = [(1, 0), (1, 1), (1, -1)]
        self.back_or_forth = back_or_forth
        # Список вражеских фигур на съедение.
        self.memory = {}

        super().__init__(window, loc, color)  # Унаследование от родителя атрибутов.


    def _prep_moves(self, board_list: list, array_dirs):
        curr_pos, temp_moves = self.loc, list()
        for d1r in array_dirs:
            ternary_for_below_zero = (1 if curr_pos[1] + d1r[1] < 0
                             else curr_pos[1]+d1r[1] )
            # Создает кортеж возможной позиции пешки для проверки условия.
            new_pos = tuple([ curr_pos[0] + ((d1r[0]) * self.back_or_forth),  # noqa
                            ternary_for_below_zero ])  # noqa


            # Есть два состояния: пешка ходит вперед и пешка съедает.
            # Под каждое состояние - свои условия.
            if d1r == (1, 0):
                if self.allowed_moves == 2:
                    # Эта строка отвечает за направление движения и количество ходов.
                    new_pos = (self.get_y()+(1*self.back_or_forth), new_pos[1])

                    if self._is_valid_move(board_list, new_pos):

                        temp_moves.append(new_pos)
                        new_pos = (new_pos[0]+(1*self.back_or_forth), new_pos[1])

                        if self._is_valid_move(board_list, new_pos):
                            temp_moves.append(new_pos)
                            continue

                if self.allowed_moves == 1:
                    # Тот же смысл, как и в прошлом комментарии.
                    # Только количество ходов изменилось на 1.
                    new_pos = (self.get_y() + (d1r[0] * self.back_or_forth),
                                    self.get_x() + d1r[1])
                    if self._is_valid_move(board_list, new_pos):
                        temp_moves.append(new_pos)

            # Когда направление пешки уходит в сторону,
            # проверяет наличие вражеской фигуры в стороне.
            else:
                # это не собственная фигура
                if BoardManipulator.get_color(board_list, new_pos) == self.enemy_color:
                    temp_moves.append(new_pos)

                if self.memory.get(new_pos, False):
                    temp_moves.append(new_pos)




        return temp_moves

    def _get_all_moves(self, board_inst):
        """ Метод, который возвращает все возможные ходы пешки. """
        # Обновляет список переменной экземпляра.
        self.moves.clear()
        resulted_moves = self._prep_moves(board_inst, self.ways_to_go)
        # Обрати внимание, что в этом методе программа не меняет глобальные значения переменных пешки,
        # а только выводит список ходов конкретного экземпляра исходя из положения всех фигур на доске.
        self.moves.extend(resulted_moves)
        # Передает эти ходы в общую свалку
        # всех ходов класса Board !!!
        return self.moves


    def _move_object(self, to_where: tuple, board_list: list,) -> int or None:
        """ Метод приказывает переместить положение пешки. """
        # Создает кортеж с координатами фигуры.
        from_where = self.loc
        # В случае того, когда пешка съедает вражескую фигуру
        # сохраняю enemy_piece_id для нее, чтобы вернуть обратно в метод.
        # Указатель вражеской пешке, если первая проходит битое поле.

        # Проверка на заданное движение.
        if not self._check_move(board_list, from_where, to_where): return False

        # Получает все возможные ходы.
        self._get_all_moves(board_list)  # Получает все возможные ходы.

        # Проверяет, что заданный ход возможен.
        if to_where in self.moves:

            """ Три возможных условия перемещения пешки: 
                  1 - В памяти есть вражеская фигура.
                  2 - Пешка съедает вражескую фигуру.
                  3 - Пешка ходит вперед. """

            if self.memory.get(to_where, False):
                # Передаю переменную кортежа вражеской фигуры
                # все значения для удаления из общего словаря фигур.
                enemy_piece = self.memory[to_where]
                board_list[enemy_piece.get_y()][enemy_piece.get_x()] = Empty()
                self.alien_id = enemy_piece.get_id()

                self.memory.clear()
                self.pre_order_move(board_list, to_where)
                return self.alien_id

            elif BoardManipulator.get_color(board_list, to_where) == self.enemy_color:
                self.alien_id = board_list[to_where[0]][to_where[1]].get_id()
                # self._check_enemy_pawns_passed_by(board_list, to_where)
                self.pre_order_move(board_list, to_where)
                return self.alien_id

            else:

                self._check_enemy_pawns_passed_by(board_list, to_where)
                self.pre_order_move(board_list, to_where)
                return self.alien_id

        # board_inst.make_msg('E: You cannot move there')
        return False

    def pre_order_move(self, board_list, to_where):
        self.allowed_moves = 1
        self._finish_move(board_list, to_where)
        self._get_all_moves(board_list)
        return

    def _is_valid_move(self, board_list: list, new_pos: tuple) -> bool:
        """ Метод для проверки состояния поля на доске."""
        # Если заданная координата не меняется относительно оси X, значит
        # пешка ходит вперед. Она не может занять вражескую позицию.
        if self.get_x() == new_pos[1] and BoardManipulator.get_color(board_list, new_pos) != Color.empty:
            return False  # Условие не выполняется.
        else:
            if super()._is_valid_move(board_list, new_pos):
                return True
            return False


    def _check_enemy_pawns_passed_by(self, board_list: list, to_where: tuple):
        """ Проверяет, если пешка, заданная пройти два хода вперед, имеет слева или справа вражескую пешку.
            Затем программа заносит ее координаты в словарь memory вражеской пешке. """
        curr_pos = self.loc
        if self.allowed_moves == 2 and (curr_pos[1] == to_where[1]):

            new_pos_on_right_side = (curr_pos[0]+2*self.back_or_forth, curr_pos[1] + 1)
            # Проверка на индексацию новой координаты, чтобы не выходило за рамки доски.
            # Проверка на существование вражеской пешки справа.
            if (curr_pos[1] + 1 <= 7
                    and BoardManipulator.get_color(board_list, new_pos_on_right_side) == self.enemy_color
                    and BoardManipulator.get_class(board_list, new_pos_on_right_side) == 'class.Pawn'):

                enemy_pawn = board_list[new_pos_on_right_side[0]][new_pos_on_right_side[1]]
                # создание промежуточной координаты между прошлым и текущим ходом данной пешки.
                mid_move_for_this_pawn_list = tuple([self.loc[0] + 1 * self.back_or_forth, self.loc[1]])
                # финальный результат входит в атрибут вражеской пешки.
                enemy_pawn.memory[mid_move_for_this_pawn_list] = self

            new_pos_on_left_side = (curr_pos[0]+2*self.back_or_forth, curr_pos[1] - 1)
            # Проверка на отрицательность x, так как индексация начинается с нуля.
            # Проверка на существование вражеской пешки справа.
            if (curr_pos[1] - 1 >= 0
                    and BoardManipulator.get_color(board_list, new_pos_on_left_side) == self.enemy_color
                    and BoardManipulator.get_class(board_list, new_pos_on_left_side) == 'class.Pawn'):

                enemy_pawn = board_list[new_pos_on_left_side[0]][new_pos_on_left_side[1]]
                # создание промежуточной координаты между прошлым и текущим ходом данной пешки
                mid_move_for_this_pawn_list = tuple([self.loc[0]+1*self.back_or_forth, self.loc[1]])
                # финальный результат входит в атрибут вражеской пешки.
                enemy_pawn.memory[mid_move_for_this_pawn_list] = self



        return None

    def _check_move(self, board_list: list, from_where, to_where):
        """ Проверят, если пешка ходит вперед.  """
        if (to_where[0] - from_where[0]) * self.back_or_forth < 0 or from_where[1] != to_where[1]:
            if BoardManipulator.get_color(board_list, to_where) != self.enemy_color and not self.memory:
                # BoardManipulator.make_msg('E: You cannot move this way')
                return False
        elif from_where == to_where:
            # BoardManipulator.make_msg('E: You have to make a move')
            return False

        return True

class Rock(Piece, ABC):
    def __init__(self, window, loc, color):
        self.ways_to_go = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        super().__init__(window, loc, color)


    def _get_all_moves(self, board_list: list) -> list:
        # Обновляет переменную экземпляра с возможными ходами.
        self.moves.clear()
        # Простой список с направлениями: вниз, вверх, вправо, влево.
        resulted_moves = self._prep_moves(board_list, self.ways_to_go)
        # Возвращает все возможные ходы в список.
        self.moves.extend(resulted_moves)
        return self.moves

    def _move_object(self, to_where: tuple, board_list: list ) -> int or None:
        # Получает все возможные ходы фигуры.
        self._get_all_moves(board_list)
        # Проверяет, если заданное перемещение присутствует в списке возможных ходов.
        if to_where in self.moves:

            if BoardManipulator.get_color(board_list, to_where) == self.enemy_color:
                perhaps_enemy = board_list[to_where[0]][to_where[1]].get_id()
                self.alien_id = perhaps_enemy

            # Удаление вражеской фигуры из общего списка фигур.
            self._finish_move(board_list, to_where)
            self._get_all_moves(board_list)
            return self.alien_id

        # BoardManipulator.make_msg('E: You cannot move there')
        return False

class Knight(Piece, ABC):
    def __init__(self, window, loc, color):
        self.ways_to_go = [(2, 1), (2, -1), (-2, 1),
                             (-2, -1), (1, -2), (1, 2),
                           (-1, 2), (-1, -2)]
        super().__init__(window, loc, color)


    def _prep_moves(self, board_list: list, array_dirs):
        curr_pos, temp_moves = self.loc, list()
        for d1r in self.ways_to_go:
            new_pos = (curr_pos[0] + d1r[0], curr_pos[1] + d1r[1])
            if new_pos[0] < 0 or new_pos[1] < 0:
                continue
            elif self._is_valid_move(board_list, new_pos):
                temp_moves.extend([new_pos])
                continue


        return temp_moves

    def _get_all_moves(self, board_list: list):
        self.moves.clear()
        resulted_moves = self._prep_moves(board_list, self.ways_to_go)
        self.moves.extend(resulted_moves)
        return self.moves

    def _move_object(self, to_where: tuple, board_list: list):
        self._get_all_moves(board_list)  # noqa
        if to_where in self.moves:

            if BoardManipulator.get_color(board_list, to_where) == self.enemy_color:
                perhaps_enemy = board_list[to_where[0]][to_where[1]].get_id()
                self.alien_id = perhaps_enemy

            self._finish_move(board_list, to_where)
            self._get_all_moves(board_list)   # noqa
            return self.alien_id

        # BoardManipulator.make_msg('E: You cannot move there')
        return False

class Bishop(Piece, ABC):
    def __init__(self, window, loc, color):
        self.ways_to_go = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        super().__init__(window, loc, color)


    def _get_all_moves(self, board_list: list) -> list:
        self.moves.clear()
        resulted_moves = self._prep_moves(board_list, self.ways_to_go)
        self.moves.extend(resulted_moves)
        return self.moves

    def _move_object(self, to_where: tuple, board_list: list) -> int or None:
        self._get_all_moves(board_list)
        if to_where in self.moves:

            if BoardManipulator.get_color(board_list, to_where) == self.enemy_color:
                perhaps_enemy = board_list[to_where[0]][to_where[1]].get_id()
                self.alien_id = perhaps_enemy

            self._finish_move(board_list, to_where)
            self._get_all_moves(board_list)
            return self.alien_id

        # BoardManipulator.make_msg('E: You cannot move there')
        return False

class Queen(Piece, ABC):
    def __init__(self, window, loc, color):
        self.ways_to_go = [(1, 1), (-1, 1), (1, -1),
                             (-1, -1), (1, 0), (-1, 0),
                             (0, 1), (0, -1)]
        super().__init__(window, loc, color)

    def _get_all_moves(self, board_list: list) -> list:
        self.moves.clear()
        resulted_moves = self._prep_moves(board_list, self.ways_to_go)
        self.moves.extend(resulted_moves)
        return self.moves

    def _move_object(self, to_where: tuple, board_list: list) -> dict or None:
        self._get_all_moves(board_list)
        if to_where in self.moves:

            if BoardManipulator.get_color(board_list, to_where) == self.enemy_color:
                perhaps_enemy = board_list[to_where[0]][to_where[1]].get_id()
                self.alien_id = perhaps_enemy

            self._finish_move(board_list, to_where)
            self._get_all_moves(board_list)
            return self.alien_id

        # BoardManipulator.make_msg('E: You cannot move there')
        return False

class King(Piece, ABC):
    def __init__(self, window, loc, color):
        self.ways_to_go = [(1, 0), (-1, 0), (0, 1),
                             (0, -1), (1, 1), (1, -1),
                             (-1, 1), (-1, -1)]
        super().__init__(window, loc, color)
        self.safe_zone = self.loc


    def _prep_moves(self, board_list: list, array_dirs):
        curr_pos, temp_moves = self.loc, list()
        for d1r in self.ways_to_go:
            new_pos = (curr_pos[0] + d1r[0],
                       curr_pos[1] + d1r[1])

            if new_pos[0] < 0 or new_pos[1] < 0:
                continue

            elif self._is_valid_move(board_list, new_pos):
                temp_moves.extend([new_pos])

        return temp_moves


    def _get_all_moves(self, board_list: list):
        self.moves.clear()
        resulted_moves = self._prep_moves(board_list, self.ways_to_go)
        self.moves.extend(resulted_moves)
        return self.moves

    def _move_object(self, to_where: tuple, board_list: list):
        self._get_all_moves(board_list)
        if to_where in self.moves:

            if BoardManipulator.get_color(board_list, to_where) == self.enemy_color:
                perhaps_enemy = board_list[to_where[0]][to_where[1]].get_id()
                self.alien_id = perhaps_enemy

            self._finish_move(board_list, to_where)
            self._get_all_moves(board_list)
            self.safe_zone = self.loc
            # Не позволяет королю сделать
            # рокировку после сделанного хода.
            self.is_not_changed = False
            return self.alien_id

        # BoardManipulator.make_msg('E: You cannot move there')
        return False



