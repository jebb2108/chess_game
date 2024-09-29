import pygame
import pygwidgets

from settings import Settings


class Authorization:

    def __init__(self, screen):
        self.screen = screen
        self.settings = Settings()

        self.box_rect = self._create_box_rect()
        self.box_name = self._create_box_name()

        self.login_input = self._create_login_input_field()
        self.password_input = self._create_password_input_field()
        self.login_button = self._create_login_button()
        self.reg_button = self._create_reg_button()


    def _create_box_rect(self):
        rect_box = pygame.draw.rect(self.screen, self.settings.DARK_GRAY,
                                    self.settings.box_loc_size, 0)

        return rect_box

    def _create_box_name(self):
        box_name = pygwidgets.DisplayText(self.screen, self.settings.box_name_loc,
                                          'Chess Game',
                                          fontSize=self.settings.box_name_font_size)

        return box_name

    def _create_login_input_field(self):
        login_field = pygwidgets.InputText(self.screen, self.settings.login_loc,
                                           width=self.settings.login_width,
                                           fontSize=self.settings.login_font_size,
                                           backgroundColor=self.settings.LIGHT_GRAY,
                                           textColor=self.settings.DARK_GRAY)
        return login_field

    def _create_password_input_field(self):
        password_field = pygwidgets.InputText(self.screen, self.settings.password_loc,
                                              width=self.settings.password_width,
                                              fontSize=self.settings.password_font_size,
                                              backgroundColor=self.settings.LIGHT_GRAY,
                                              textColor=self.settings.DARK_GRAY)
        return password_field

    def _create_login_button(self):
        login_button = pygwidgets.TextButton(self.screen, self.settings.login_button_loc,
                                             'log in', width=self.settings.login_button_width,
                                             height=self.settings.login_button_height)
        return login_button

    def _create_reg_button(self):
        reg_button = pygwidgets.TextButton(self.screen, self.settings.reg_button_loc,
                                           'registration', width=self.settings.reg_button_width,
                                           height=self.settings.reg_button_height)
        return reg_button

    def show_authorization_window(self):
        visuals = [

            self._create_box_rect(),

            self.box_name.draw(),
            self.login_input.draw(),
            self.password_input.draw(),
            self.login_button.draw(),
            self.reg_button.draw()

        ]

        return visuals
