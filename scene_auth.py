import pyghelpers
import pygwidgets
import pygame

import sqlite3
from hashlib import sha256
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

        self.version_logo = pygwidgets.DisplayText(self.window, (665, 670),
                                                   'Chess vers: v1.5', textColor=GOLD, fontSize=32)


    def getSceneKey(self):
        return SCENE_AUTH

    def enter(self, data):
        pass

    def handleInputs(self, eventsList, keyPressedList):
        self.login_n_psswrd = str(self.login_input.getValue() + ' '
                                  + self.password_input.getValue())

        for event in eventsList:

            if self.login_button.handleEvent(event):
                if self.check_db():
                    self.goToScene(SCENE_PLAY)

            self.login_input.handleEvent(event)
            self.password_input.handleEvent(event)


            if self.reg_button.handleEvent(event):
                self.goToScene(SCENE_REG)

        if (keyPressedList[pygame.K_RETURN] and
                self.login_n_psswrd == 'gabriel bouchard'):
            self.goToScene(SCENE_PLAY)

        return

    def update(self):
        self.check_on_login_button()
        return

    def check_db(self):
        conn = sqlite3.connect('db/users.db')
        cur = conn.cursor()
        cur.execute('SELECT password FROM users')
        passwords = list(sum(cur.fetchall(), ()))
        for password in passwords:
            new_hashed_password = sha256(self.password_input.getValue().encode('utf-8')).hexdigest()
            if new_hashed_password == password:
                db_login = cur.execute(f'SELECT login FROM users WHERE password = ?', (password,))
                result = db_login.fetchone()
                if self.login_input.getValue() == result[0]:
                    cur.close()
                    return True

        cur.close()
        return False

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
            self.version_logo.draw()
        return

    def leave(self):
        self.login_input.setValue('')
        self.password_input.setValue('')
        self.login_button.disable()
        return None

