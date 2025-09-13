import pygame.font
from pygame.sprite import Group
from shiplife import Ship
from math import *

class Scoreboard:
    '''A Class for report scoring information.'''
    
    def __init__(self, ai_game):
        '''Initialize scorekeeping attributes'''
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Board image
        self.board_img = pygame.image.load("Assets\scoreboard.png")

        # Font settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48, italic = True)

        # Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        '''Turns the score into a rendered image.'''
        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(score_str, True, self.text_color, (255,255,255))

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 50
        self.score_rect.top = 20

    def show_score(self):
        '''Draw score to the screen.'''
        self.sin_wave()

        # Display of score and its animation using sin-wave
        self.score_x = self.score_rect[0]
        self.score_y = self.score_rect[1]  
        self.board_img_rect = self.board_img.get_rect()
        self.board_img_rect.center = self.score_rect.center

        self.screen.blit(self.board_img, [self.board_img_rect[0], self.board_img_rect[1] + self.sin_y])
        self.screen.blit(self.score_image, [self.score_x, self.score_y + self.sin_y])
        # print(self.board_img_rect.center)

        # Display of High_score and its animation using sin-wave
        self.high_score_x = self.high_score_rect[0]
        self.high_score_y = self.high_score_rect[1]
        self.board_img_rect.center = self.high_score_rect.center

        self.screen.blit(self.board_img, [self.board_img_rect[0], self.board_img_rect[1] + self.sin_y])
        self.screen.blit(self.high_score_image, [self.high_score_x, self.high_score_y + self.sin_y])
        # print(self.board_img_rect.center)

        # Display of level and its animation using sin-wave
        self.level_x = self.level_rect[0]
        self.level_y = self.level_rect[1]
        self.screen.blit(self.level_image, [self.level_x, self.level_y + self.sin_y])


        self.ships.draw(self.screen)

    def prep_high_score(self):
        '''Turn the high score into rendered image.'''
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"{high_score:,}"
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, (255,255,255)
        )

        # Stores high_score in score.txt
        with open("score.txt", "w") as file:
            file.write(str(self.stats.high_score))
            
        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high__score(self):
        '''Check to see if there's a new high score.'''
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        '''Turn the level into a rendered image.'''
        level_str = str(self.stats.level)
        self.level_image = self.font.render(
            level_str, True, self.text_color, self.settings.bg_color
            )
        
        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 20

    def prep_ships(self):
        '''Show how many ships are left.'''
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 0
            self.ships.add(ship)

    def sin_wave(self):
        self.theta = self.ai_game.theta
        self.center = [0,0]
        self.radius = 10

        self.sin_x = self.center[0] + self.radius * cos(self.theta)
        self.sin_y = self.center[1] + self.radius * sin(self.theta)
