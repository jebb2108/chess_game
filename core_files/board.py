""" Класс шахматной доски """
import copy
from abc import ABC

from core_files.settings import Settings
from core_files.pieces import BoardManipulator, Empty, Piece, King, Rock, Color


class Board(BoardManipulator, ABC):
    def __init__(self, window, board_ls):
        self.board = [[Empty()] * 8 for _ in range(8)]
        if board_ls is not None:  # оставленная возможность
            # замены для копирования доски
            self.board.clear()
            self.board = board_ls

        self.all_poss_moves = dict()
        self.settings = Settings(window)
        self.initialize()

    def initialize(self):
        for piece in self.settings.all_pieces:
            self.board[piece.get_y()][piece.get_x()] = piece


        self.update_all_poss_moves_dict(container=[self.board, self.settings.all_pieces],
                                        color_indx=[Color.white, Color.black])

    def update_all_poss_moves_dict(self, container=None, color_indx=None):

        """ Главный смысл этого метода в том, чтобы обновить по дефолту
            все значения словаря ИЛИ обновление словаря вражеских фигур в
            скопированном словаре возможных ходов. """

        # Проверка на то, чтобы НИЧЕГО не было передано в аргументах метода.
        # Тогда операция считается деволтной
        if (container is None) and (color_indx is None):
            board_list = self.board
            all_possible_moves_dict = self.all_poss_moves
            color_indx = [Color.white, Color.black]

        else:
            board_list = container[0]
            all_possible_moves_dict = container[1]

        self.all_poss_moves = { key: key._get_all_moves(board_list)
                                for  key in all_possible_moves_dict if key.color in color_indx }

        return

    def get_class_as_str(self, coords):
        return BoardManipulator.get_class(self.board, coords)


class BoardUser(Board):
    def __init__(self, window, board_ls):

        self.chosen_piece_object = Empty
        self.chosen_piece_class = None
        self.chosen_piece_color = None

        super().__init__(window, board_ls)

    def pick_piece(self, its_loc_on_board: tuple) -> object:
        coord_y, coord_x = its_loc_on_board
        the_piece = self.board[coord_y][coord_x]
        return the_piece

    @property
    def chosen_piece_object(self):
        return self.__chosen_piece_object

    @chosen_piece_object.setter
    def chosen_piece_object(self, chosen_piece_object=None):
        if chosen_piece_object is not None:
            if issubclass(type(chosen_piece_object), Piece):
                # Новые обязательные динамические атрибуты классу BoardTools
                self.chosen_piece_class = self.get_class(self.board, chosen_piece_object.loc)
                self.chosen_piece_color = self.get_color(self.board, chosen_piece_object.loc)
                # Выролняет назначение основному атрибуту
                self.__chosen_piece_object = chosen_piece_object

        else:
            self.__chosen_piece_object = Empty()
            self.chosen_piece_class = None
            self.chosen_piece_color = None


    def attempt_piece_to_move(self, dest_coords: list) -> [True or False or Piece]:
        """ Проверяет, если по правилам шахмат возможно совершить ход с данными координатами """
        if self.chosen_piece_object._move_object(dest_coords, board_list=self.board) is not False:  # noqa

            if isinstance(self.chosen_piece_object.alien_id, int):
                eaten_piece = next((key for key in self.all_poss_moves
                                    if key.id == self.chosen_piece_object.alien_id), None)
                # проигрывает звук при съедании
                self.chosen_piece_object.capture_sound.play()
                self.chosen_piece_object.alien_id = None
                del self.all_poss_moves[eaten_piece]
                # Обновление всего, чтобы было затронуто перемещением.
                self.update_all_poss_moves_dict()
                return eaten_piece

            self.update_all_poss_moves_dict()
            return True

        self.update_all_poss_moves_dict()
        return False


    def conduct_change(self, to_where, from_where=None):
        """ Метод изменяет доску, совершая ход и не делая проверки """

        # Позволяет назначить активную фигуру из другой доски
        if from_where is not None:
            the_piece = self.pick_piece(from_where)
            self.chosen_piece_object = the_piece

        dest_color = self.get_color(self.board, to_where)
        if dest_color != Color.empty:
            if dest_color == self.chosen_piece_object.enemy_color:

                enemy_piece = self.pick_piece(to_where)
                # удаление фигуры из общего списка
                del self.all_poss_moves[enemy_piece]

                orig_y, orig_x = self.chosen_piece_object.loc
                self.chosen_piece_object.set_loc(to_where)
                self.board[orig_y][orig_x] = Empty()


                if self.chosen_piece_class == 'class.King':
                    self.chosen_piece_object.safe_zone = self.chosen_piece_object.loc

                return enemy_piece


            else:
                # ДОРАБОТАТЬ в случае обнаружении дружественной фигуры!
                tmp = self.pick_piece(to_where)
                return tmp

        orig_y, orig_x = self.chosen_piece_object.loc
        new_y, new_x = to_where
        self.board[orig_y][orig_x] = Empty()
        self.board[new_y][new_x] = self.chosen_piece_object
        self.chosen_piece_object.set_loc(to_where)

        if self.chosen_piece_class == 'class.King':
            self.chosen_piece_object.safe_zone = self.chosen_piece_object.loc

        return None

    def conduct_force_change(self, old_pos, new_pos, removed_piece=None) -> [True or False]:

        if removed_piece:
            old_x, old_y = new_pos
            e_old_y, e_old_x = removed_piece.loc
            self.board[old_y][old_x] = self.chosen_piece_object
            self.board[e_old_y][e_old_x] = removed_piece

            # Помимо этого, надо вернуть фигуру в общий список
            self.all_poss_moves[removed_piece] = removed_piece.access_all_moves()

            self.chosen_piece_object.set_loc(new_pos)


            if self.chosen_piece_class == 'class.King':
                self.chosen_piece_object.safe_zone = self.chosen_piece_object.loc

            self.update_all_poss_moves_dict()
            return

        else:
            old_y, old_x = new_pos
            new_y, new_x = old_pos
            self.board[old_y][old_x] = self.chosen_piece_object
            self.board[new_y][new_x] = Empty()

            self.chosen_piece_object.set_loc(new_pos)

            if self.chosen_piece_class == 'class.King':
                self.chosen_piece_object.safe_zone = self.chosen_piece_object.loc

            self.update_all_poss_moves_dict()
            return

    def check_castling_and_move(self, to_where: list) -> [True or False]:

        if isinstance(self.chosen_piece_object, King):

            # Вытаскиваю из настроек нужные мне значения для рокировки.
            all_rock_coords = self.settings.get_rock_coords(True)
            all_rock_possible_moves = self.settings.get_rock_moves(True)

            to_where = tuple(to_where)  # Словарные ключи могут быть только неизменными кортежами.
            rock_coords = all_rock_coords[to_where]  # Вытаскиваю значение по ключу. Перевожу все в кортежи.
            # Может быть только один ход для ладьи в рокировке.
            # Вытаскиваю значение по местонахождению.5
            rock_possible_move = all_rock_possible_moves[tuple(rock_coords)]

            # Может быть только ладьею на заданной координате.
            rock = self.pick_piece(rock_coords)
            if not isinstance(rock, Rock):
                return False

            # Условие, при котором ладья не может быть тронутой.
            if rock.is_not_changed and self.chosen_piece_object.is_not_changed:
                for move in rock.moves:  # noqa
                    # Ладье должна быть доступна клетка перед королем.
                    if list(move) in [[0, 3], [0, 5], [7, 3], [7, 5]]:
                        king_from_where, king_to_where = king.loc, to_where  # noqa
                        # Происходит перестановка фигур и обновление словаря ходов.
                        self.conduct_change(rock_possible_move)
                        self.conduct_force_change(king_from_where, king_to_where)  # noqa
                        self.update_all_poss_moves_dict()
                        return True
                    else:
                        return False

        return True
