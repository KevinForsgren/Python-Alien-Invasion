import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    '''A class to manage shiplife icon.'''
    def __init__(self, ai_game):
        '''Initialize the ship and set its starting position.'''
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the ship image and get its rect
        self.image = pygame.image.load("Assets/shiplife.bmp")
        self.rect = self.image.get_rect()

    def blitme(self):
        '''Draw the ship at its current location.'''
        self.screen.blit(self.image, self.rect)
