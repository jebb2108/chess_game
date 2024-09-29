import os

import pygame
import pygwidgets
import sys

from authorization import *


class Main:
    pygame.font.init()

    GRAY = (200, 200, 200)
    DARK_GRAY = (50, 50, 50)
    LIGHT_GRAY = (240, 240, 240)
    FRAMES_PER_SECOND = 60
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption('chess game')

    active = True

    def __init__(self):
        self.background_image = pygame.image.load('images/background.png')
        self.board_img = pygame.image.load('images/chess_board.jpg')
        self.board_rect = self.board_img.get_rect()
        self.screen_w = self.board_rect.w + int(self.board_rect.w // 100 * 50)
        self.screen_h = self.board_rect.h + int(self.board_rect.h // 100 * 5)
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))

        self.login_info = dict()

        self.authorization = Authorization(self.screen)

        self.greeting_field = pygwidgets.DisplayText(self.screen, (685, 20), fontSize=35)

    def run_game(self):
        pygame.init()
        while True:

            self.check_events()

            self.screen.fill(Main.GRAY)
            self.update_screen()
            self.CLOCK.tick(Main.FRAMES_PER_SECOND)


    def check_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif not self.login_info:
                self.get_authorized(event)



    def get_authorized(self, event):

        self.authorization.login_input.handleEvent(event)
        self.authorization.password_input.handleEvent(event)

        users_login = self.authorization.login_input.getValue()
        users_password = self.authorization.password_input.getValue()

        if users_login and users_password:
            if self.authorization.login_button.handleEvent(event):
                if self.check_password([users_login, users_password]):
                    self.login_info = [
                        users_login,
                        users_password
                    ]

                    ls_name = self.login_info[0]
                    self.greeting_field.setValue(f'Hello, {ls_name.title()}!')

        return None

    def update_screen(self):
        if self.login_info:
            self.greeting_field.draw()
            self.place_board()
            return pygame.display.update()

        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background_image, (-150, 40))
        self.authorization.show_authorization_window()
        return pygame.display.update()

    def place_board(self):
        w_pawn = pygame.image.load('images/white_pawn1.png')
        self.screen.blit(self.board_img, (10, 10))
        self.screen.blit(w_pawn, (49, 440))
        return None

    @staticmethod
    def check_password(input_info):
        filename = 'players_info.txt'
        if os.path.exists(filename):
            with open(filename) as f:
                users_logins = f.readlines()
                new_login = users_logins[0].replace('\n', '').strip()
                new_password = users_logins[1].replace('\n', '').strip()
                redacted_info = [new_login, new_password]
                if redacted_info == input_info:
                    return True

        else:
            return False


if __name__ == '__main__':
    this_chess = Main()
    this_chess.run_game()
