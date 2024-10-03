class Settings:

    GRAY = (200, 200, 200)
    DARK_GRAY = (50, 50, 50)
    LIGHT_GRAY = (240, 240, 240)
    FRAMES_PER_SECOND = 60

    BOX_NAME = 'Chess Game'
    BOX_NAME_LOC = (685, 20)
    BOX_NAME_FONT_SIZE = 40
    BOX_LOC_SIZE = (660, 15, 220, 180)

    LOGIN_LOC = (680, 60)
    LOGIN_WIDTH = 180
    LOGIN_FONT_SIZE = 40

    PASSWORD_LOC = (680, 100)
    PASSWORD_WIDTH = 180
    PASSWORD_FONT_SIZE = 40

    LOGIN_BUTTON_LOC = (680, 140)
    LOGIN_BUTTON_WIDTH = 65
    LOGIN_BUTTON_HEIGHT = 30

    REG_BUTTON_LOC = (750, 140)
    REG_BUTTON_WIDTH = 110
    REG_BUTTON_HEIGHT = 30

    MATCHMAKING_WINDOW_LOC = (150, 150, 600, 330)
    MATCHMAKING_WINDOW_COLOR = (210, 210, 210)

    DISPLAY_BUTTON_LOC = (500, 250)
    DISPLAY_BUTTON_WIDTH = 110
    DISPLAY_BUTTON_HEIGHT = 30

    PLAY_BUTTON_LOC = (500, 200)
    PLAY_BUTTON_WIDTH = 170
    PLAY_BUTTON_HEIGHT = 30

    def __init__(self):
        self.time = 10
        self.time_increase = 5

    def alter_settings(self, option1, option2):
        self.time = option1
        self.time_increase = option2
        return None

    def draw_pawns(self):
        pass