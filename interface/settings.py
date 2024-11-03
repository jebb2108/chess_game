class Settings:

    def __init__(self):
        self.time = 10
        self.time_increase = 5

    def alter_settings(self, option1, option2):
        self.time = option1
        self.time_increase = option2
        return None

    def draw_pawns(self):
        pass