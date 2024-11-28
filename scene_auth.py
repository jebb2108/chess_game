import pyghelpers
import pygwidgets
import pygame

from pygame.locals import *
from constants import *


class SceneAuth(pyghelpers.Scene):

    BACKGROUND_IMAGE = pygame.image.load('images/background.png')

    def __init__(self, window):
        self.window = window

        self.box_name = pygwidgets.DisplayText(window, (660, 50), 'Chess Game', fontSize=40)

        self.login_input = pygwidgets.InputText(window, (655, 85), width=180, fontSize=40,
                                                backgroundColor=LIGHT_GRAY, textColor=DARK_GRAY)

        self.password_input = pygwidgets.InputText(window, (655, 125), width=180, fontSize=40,
                                                   backgroundColor=LIGHT_GRAY, textColor=DARK_GRAY)

        self.login_button = pygwidgets.TextButton(window, (655, 165), 'Login', width=65, height=30)

        self.reg_button = pygwidgets.TextButton(window, (725, 165), 'Register', width=110, height=30)

        self.buttons = [self.box_name, self.login_input, self.password_input, self.login_button, self.reg_button]

    def getSceneKey(self):
        return SCENE_AUTH

    def enter(self, data):
        pass


    def handleInputs(self, eventsList, keyPressedList):
        self.login_n_psswrd = str(self.login_input.getValue() + ' '
                                  + self.password_input.getValue())
        for event in eventsList:
            if self.login_n_psswrd == 'gabriel bouchard':
                if self.login_button.handleEvent(event):
                    self.goToScene(SCENE_PLAY)
            self.login_input.handleEvent(event)
            self.password_input.handleEvent(event)

    def update(self):
        self.check_on_login_button()
        return

    def check_on_login_button(self):
        if self.login_input.getValue() != '' and self.password_input.getValue() != '':
            self.login_button.enable()
        else:
            self.login_button.disable()
        return

    def draw(self):
        self.window.blit(SceneAuth.BACKGROUND_IMAGE, (-170, 40))
        pygame.draw.rect(self.window, GRAY, (635, 40, 220, 180), 0)
        for button in self.buttons:
            button.draw()
        return

    def leave(self):
        self.login_input.setValue('')
        self.password_input.setValue('')
        self.login_button.disable()
        return None

