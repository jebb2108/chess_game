from abc import *
import pygame
import pygwidgets

from chess_pieces import Empty
from constants import *
from settings import Settings


class Color(object):
    empty = 0
    white = 1
    black = 2


class Empty(object):
    color = Color.empty

    def __str__(self):
        return '.'

    def get_loc(self):
        return None


class Piece(ABC):

    def __init__(self, window, loc, color):
        self.window = window
        self.loc = loc
        self.rect = None
        self.color = color
        color_name = 'white' if color == Color.white else 'black'
        full_path = color_name + '_' + self.__class__.__name__ + '_mod.png'
        self.image = pygame.image.load('images/' + full_path)
        self.is_moved = False

        # self.clicked_sound = pygame.mixer.Sound('sounds/click.wav')

    def __str__(self):
        return ('\u265F', '\u2659')[0 if self.color == Color.white else 1]

    def clicked_inside(self, mouse_pos):
        first_x, first_y = Settings.pixel_mapping[self.loc]
        this_rect = pygame.rect.Rect(first_x, first_y, first_x + 55, first_y + 55)
        clicked = this_rect.collidepoint(mouse_pos)
        if clicked:
            # self.clicked_sound.play()
            return True
        else:
            return False

    def get_loc(self):
        return self.loc

    def draw(self):
        screen_loc = Settings.pixel_mapping[self.loc]
        self.window.blit(self.image, screen_loc)


class Pawn(Piece, ABC):
    def __init__(self, window, loc, color):
        self.color = color
        self.back_or_forth = -1 if self.color == Color.white else 1
        super().__init__(window, loc, color)

class Board(ABC):

    def __init__(self, window):
        self.window = window
        self.board = [[Empty] * 8 for _ in range(8)]
        self.spot_list = self.make_all_spot_list()
        self.initialise()
        self.all_pieces = list((piece for piece in sum(self.board, []) if issubclass(type(piece), Piece)))


    def initialise(self):
        for black_indx in range(0, 8):
            self.board[1][black_indx] = Pawn(self.window,(1, black_indx), Color.black)
        for white_indx in range(0, 8):
            self.board[6][white_indx] = Pawn(self.window, (6, white_indx), Color.white)


    def make_all_spot_list(self):
        self.spot_list = []
        for y in range(0, 8):
            for x in range(0, 8):
                spot = list(Settings.pixel_mapping[(x, y)])
                spot.extend([x+55, y+55])
                single_rect = pygame.rect.Rect(spot[0], spot[1], spot[2], spot[3])
                self.board[x][y].rect = single_rect
                self.spot_list.append(single_rect)

        return self.spot_list

    def attempt_piece_to_move(self, piece, dest_coords):
        print(piece, dest_coords)
        return


    def test_click(self, mouse_pos):
        for line in self.board:
            for piece in line:
                try:
                    if piece.clicked_inside(mouse_pos):
                        return print('this is the piece', piece)
                except AttributeError:
                    pass
        print('no piece')


# if __name__ == '__main__':
#     window = None
#     board = Board(window)
#     board.make_all_spot_list()
    # print(board.spot_list)
    # board.test_click([130, 65])
    # board.test_click([130, 195])
    #
    # print(repr(board))



    # print(board.board)

