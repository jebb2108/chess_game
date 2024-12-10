import sys

import sqlite3

import pygame
import pygwidgets
import pyghelpers

from hashlib import sha256

from PIL import Image, ImageFilter

from constants import *


class SceneReg(pyghelpers.Scene):

    BACKGROUND_IMAGE = None

    def __init__(self, window):
        self.window = window

        self.reg_display = pygwidgets.DisplayText(self.window, (350, 200), 'Registration', fontSize=50)

        self.email_input = pygwidgets.InputText(self.window, (350, 280), 'Email', width=200, fontSize=40)

        self.login_input = pygwidgets.InputText(self.window, (350, 330), 'Login', width=200, fontSize=40)

        self.password_input = pygwidgets.InputText(self.window, (350, 380), 'Password', width=200, fontSize=40)

        self.password_confirmation = pygwidgets.InputText(self.window, (350, 430),'Confirmation', width=200, fontSize=40)

        self.register_button = pygwidgets.TextButton(self.window, (350, 500), 'Register', width=80, height=30)

        self.go_back_button = pygwidgets.TextButton(self.window, (450, 500), 'Go Back', width=100, height=30)

        self.inputs = [ self.email_input, self.login_input, self.password_input,
                         self.password_confirmation ]

        self.buttons = [ self.register_button, self.go_back_button ]

        if SceneReg.BACKGROUND_IMAGE is None:
            img = Image.open('images/background.png').filter(ImageFilter.GaussianBlur(radius=5))
            img.save('images/background_blur.png')
            SceneReg.BACKGROUND_IMAGE = pygame.image.load('images/background_blur.png')

    def getSceneKey(self):
        return SCENE_REG

    def handleInputs(self, eventsList, keyPressedList):
        for event in eventsList:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for index, obj in enumerate(self.inputs):
                    old_values_list = ['Email', 'Login', 'Password', 'Confirmation']
                    if obj.rect.collidepoint(event.pos):
                        if obj.getValue() in old_values_list:
                            obj.setValue('')
                            continue



                    elif obj.getValue() == '':
                            obj.setValue(old_values_list[index])





            self.email_input.handleEvent(event)
            self.login_input.handleEvent(event)
            self.password_input.handleEvent(event)
            self.password_confirmation.handleEvent(event)

            if self.register_button.handleEvent(event) and self.validate():
                self.create_user()

                self.goToScene(SCENE_AUTH)

            if self.go_back_button.handleEvent(event):
                self.goToScene(SCENE_AUTH)

    def validate(self):
        email = self.email_input.getValue()
        login = self.login_input.getValue()
        password = self.password_input.getValue()
        confirmation = self.password_confirmation.getValue()

        ls = [email, login, password, confirmation]

        if '' in ls or ' ' in ls:
            return False

        elif '@' not in email or '.' not in email:
            return False

        for item in ls:
            if 5 >= len(item) > 30:
                return False

        if password != confirmation:
            return False


        return True

    def create_user(self):
        email = self.email_input.getValue()
        login = self.login_input.getValue()
        password = self.password_input.getValue()

        hashed_password = sha256(password.encode('utf-8')).hexdigest()

        con = sqlite3.connect('users.db')
        cur = con.cursor()

        cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, login TEXT, password TEXT)')

        cur.execute('INSERT INTO users (email, login, password) VALUES (?, ?, ?)', (email, login, hashed_password))
        con.commit()
        con.close()

        return

    def draw(self):
        self.window.fill(BLACK)
        self.window.blit(SceneReg.BACKGROUND_IMAGE, (-170, 40))

        pygame.draw.rect(self.window, GRAY, ( 300, 150, 300, 400), 0, 5)

        for button in self.buttons:
            button.draw()

        for inpt in self.inputs:
            inpt.draw()

        self.reg_display.draw()
        return

    def leave(self):
        for inpt in self.inputs:
            inpt.setValue('')

        return None