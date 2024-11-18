""" Класс шахматной доски """
from abc import ABC

from core_files.settings import Settings
from core_files.pieces import BoardManipulator, Empty, Piece, Color


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

        self.illegal_sound_state = False

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

    def check_castling_and_move(self, to_where: tuple) -> [True or False]:

        it_is_king = (self.chosen_piece_class == 'class.King')

        if it_is_king and self.chosen_piece_object.is_not_changed:
            rock_in_appropriate_place = Settings.hashed_dict_castling.get(to_where, False)
            if not it_is_king or not rock_in_appropriate_place:
                self.illegal_sound_state = True
                return False

            o_king = self.chosen_piece_object
            o_rock = self.board[rock_in_appropriate_place[0]][rock_in_appropriate_place[1]]

            if o_rock.is_not_changed:
                dest_for_rock = Settings.all_rock_appropriate_moves[o_rock.loc]

                if dest_for_rock in o_rock.access_all_moves():
                    # Происходит перестановка фигур и обновление словаря ходов.

                    self.board[o_king.get_y()][o_king.get_x()] = Empty()
                    self.board[o_rock.get_y()][o_rock.get_x()] = Empty()

                    self.board[to_where[0]][to_where[1]] = o_king
                    self.board[dest_for_rock[0]][dest_for_rock[1]] = o_rock

                    o_king.set_loc(to_where)
                    o_king.is_not_changed = False
                    o_king.safe_zone = to_where
                    o_rock.set_loc(dest_for_rock)
                    o_rock.is_not_changed = False

                    self.update_all_poss_moves_dict()

                    return True

        return False

    def attempt_piece_to_move(self, dest_coords: list) -> [True or False or Piece]:
        """ Проверяет, если по правилам шахмат возможно совершить ход с данными координатами """
        if self.chosen_piece_object._move_object(dest_coords, board_list=self.board) is not False:  # noqa

            if isinstance(self.chosen_piece_object.alien_id, int):
                eaten_piece = next((key for key in self.all_poss_moves
                                    if key.id == self.chosen_piece_object.alien_id), None)
                # проигрывает звук при съедании
                # self.chosen_piece_object.capture_sound.play()
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
                new_y, new_x = to_where
                self.board[orig_y][orig_x] = Empty()
                self.chosen_piece_object.set_loc(to_where)
                self.board[new_y][new_x] = self.chosen_piece_object


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
            orig_x, orig_y = new_pos
            enemy_old_y, enemy_old_x = removed_piece.loc
            self.board[orig_y][orig_x] = self.chosen_piece_object
            self.board[enemy_old_y][enemy_old_x] = removed_piece

            # Помимо этого, надо вернуть фигуру в общий список
            self.all_poss_moves[removed_piece] = removed_piece.access_all_moves()

            self.chosen_piece_object.set_loc(new_pos)


            if self.chosen_piece_class == 'class.King':
                self.chosen_piece_object.safe_zone = self.chosen_piece_object.loc

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