class Settings:
    '''Class to store all settings for the game.'''
    def __init__(self):
        '''Initialize the game's static settings.'''
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (230, 230, 230)
        self.icon = "Assets/app_icon.png"
        # Ship settings
        self.ship_limit = 3
        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0, 0, 0)
        self.bullets_allowed = 3
        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # Score settings
        self.alien_points = 50
        self.score_scale = 1.5
        self.scoreborder = "Assets/scoreboard.png"

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''Initialize settings that change throughout the game.'''
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0

        # Fleet_direction of 1 represents right; -1 represent left.
        self.fleet_direction = 1

    def increase_speed(self):
        '''Increases speed settings and aliens point values.'''
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)