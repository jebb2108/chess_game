import pygwidgets

from constants import *

class Authorization:

    BACKGROUND_IMAGE = pygame.image.load('images/background.png')

    LOGIN_AWAITING_STATUS = False

    def __init__(self, window):

        self.window = window

        self.box_name = pygwidgets.DisplayText(window, (660, 50), 'Chess Game', fontSize=40)

        self.login_input = pygwidgets.InputText(window, (655, 85), width=180, fontSize=40,
                                                backgroundColor=LIGHT_GRAY, textColor=DARK_GRAY)

        self.password_input = pygwidgets.InputText(window, (655, 125), width=180, fontSize=40,
                                                   backgroundColor=LIGHT_GRAY, textColor=DARK_GRAY)

        self.login_button = pygwidgets.TextButton(window, (655, 165), 'Login', width=65, height=30,
                                                  callBack=self.check_authorization)

        self.reg_button = pygwidgets.TextButton(window, (725, 165),'Register', width=110, height=30)

        self.buttons = [self.box_name, self.login_input, self.password_input, self.login_button, self.reg_button]


    def event_manager(self, event):

        if self.login_input.getValue() != '' and self.password_input.getValue() != '':
            self.login_button.enable()
        else:
            self.login_button.disable()

        if event.type in MOUSE_EVENTS_LIST:
            if self.reg_button.rect.collidepoint(event.pos):
                pass
            else:
                pass


    def check_authorization(self, callBack):
        if (self.login_input.getValue() + ' ' +
                self.password_input.getValue() == 'gabriel bouchard'):

            self.login_input.setValue('')
            self.password_input.setValue('')
            Authorization.LOGIN_AWAITING_STATUS = False

            return True
        else:
            return False


    def draw(self):
        self.window.blit(self.BACKGROUND_IMAGE, (-170, 40))
        pygame.draw.rect(self.window, GRAY, (635, 40, 220, 180), 0)
        for button in self.buttons:
            button.draw()
        return
