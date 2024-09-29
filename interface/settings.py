class Settings:

    GRAY = (200, 200, 200)
    DARK_GRAY = (50, 50, 50)
    LIGHT_GRAY = (240, 240, 240)

    def __init__(self):

        self.box_name = 'Chess Game'
        self.box_name_loc = (685, 20)
        self.box_name_font_size = 40
        self.box_loc_size = (660, 15, 220, 180)

        self.login_loc = (680, 60)
        self.login_width = 180
        self.login_font_size = 40

        self.password_loc = (680, 100)
        self.password_width = 180
        self.password_font_size = 40

        self.login_button_loc = (680, 140)
        self.login_button_width= 65
        self.login_button_height = 30

        self.reg_button_loc = (750, 140)
        self.reg_button_width = 110
        self.reg_button_height = 30