import os
from fileinput import filename

import pygame
import pygwidgets
import sys
import json


class Main:

    pygame.font.init()

    GRAY = (200, 200, 200)
    DARK_GRAY = (50, 50, 50)
    LIGHT_GRAY = (240, 240, 240)
    FRAMES_PER_SECOND = 30
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

        self.greeting_field = pygwidgets.DisplayText(self.screen, (685, 20), fontSize=35)

        self.text_field = pygwidgets.DisplayText(self.screen, (685, 20),
                                                 'Chess Game', fontSize=40)

        self.input_field_login = pygwidgets.InputText(self.screen, (680, 60),
                                                      width=180, fontSize=40,
                                                      backgroundColor= Main.LIGHT_GRAY,
                                                      textColor=Main.DARK_GRAY)

        self.input_field_password = pygwidgets.InputText(self.screen, (680, 100),
                                                         width=180, fontSize=40,
                                                         backgroundColor= Main.LIGHT_GRAY,
                                                         textColor=Main.DARK_GRAY)

        self.login_button = pygwidgets.TextButton(self.screen, (680, 140),
                                                  'log in', width=65, height=30)
        self.reg_button = pygwidgets.TextButton(self.screen, (750, 140),
                                                  'registration', width=110, height=30)

    def run_game(self):
        pygame.init()

        while self.active:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if not self.login_info:

                    self.input_field_login.handleEvent(event)
                    self.input_field_password.handleEvent(event)
                    users_login= self.input_field_login.getValue()
                    users_password= self.input_field_password.getValue()

                    if users_login and users_password:
                        if self.login_button.handleEvent(event):
                            if self.check_password([users_login, users_password]):
                                self.login_info = [
                                    users_login,
                                        users_password
                                ]

                if self.login_info:
                    ls_name = self.login_info[0]
                    self.greeting_field.setValue(f'Hello, {ls_name.title()}!')

            self.screen.fill(Main.GRAY)

            self.login_page()


            pygame.display.update()
            self.CLOCK.tick(Main.FRAMES_PER_SECOND)

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


    def login_page(self):
        if self.login_info:
            self.greeting_field.draw()
            self.place_board()
            return
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background_image, (-150, 40))
        rect = pygame.draw.rect(self.screen, Main.DARK_GRAY, (660, 15, 220, 180), 0)
        self.text_field.draw()
        self.input_field_login.draw()
        self.input_field_password.draw()
        self.login_button.draw()
        self.reg_button.draw()
        return






    def place_board(self):
        w_pawn = pygame.image.load('images/white_pawn1.png')
        self.screen.blit(self.board_img, (10, 10))
        self.screen.blit(w_pawn, (49, 440))
        return

if __name__ == '__main__':
    this_chess = Main()
    this_chess.run_game()