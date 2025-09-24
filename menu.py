import pygame

class Menu():
    """A class to access menu screens."""
    def __init__(self, ai_game):
        self.menu_screen = ai_game.screen
        self.settings = ai_game.settings
        self.menu_width = ai_game.settings.screen_width
        self.menu_height = ai_game.settings.screen_height
        self.menu_rect = ai_game.screen.get_rect()
        self.background = ai_game.settings.menu_bg_color
        self.ai_title = ai_game.ai_title

    def startup_menu(self):
        """Show start up menu screen on start."""
        pygame.draw.rect(self.menu_screen, (self.background), 
        (0, 0, self.menu_width, self.menu_height))
        self.ai_title_rect = self.ai_title.get_rect()
        self.ai_title_rect.midbottom = self.menu_rect.center
        self.menu_screen.blit(self.ai_title, (self.ai_title_rect))