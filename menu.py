import pygame

class Menu():
    """A class to access menu screens."""
    def __init__(self, ai_game):
        self.menu_screen = ai_game.screen
        self.menu_width = ai_game.settings.screen_width
        self.menu_height = ai_game.settings.screen_height
        self.menu_rect = ai_game.screen.get_rect()
        self.background = ai_game.background

    def startup_menu(self):
        """Show star up menu screen on start."""
        self.menu_screen.blit(self.background, (0,0))