import pygame
from pygame.locals import *
import sys


class Main:

    BLACK = (0, 0, 0)
    FRAMES_PER_SECOND = 30

    board_img = pygame.image.load('images/chess_board.png')
    board_rect = board_img.get_rect()

    pygame.init()
    window = pygame.display.set_mode(board_rect.size)
    clock = pygame.time.Clock()

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        window.fill(BLACK)
        window.blit(board_img, (0, 0))
        pygame.display.update()
        clock.tick(FRAMES_PER_SECOND)
