import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from scoreboard import Scoreboard
from menu import Menu

class AlienInvasion:
    '''Overall class to manage game assets and behavior'''

    def __init__(self):
        '''Initailize the game, and create game resource'''
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        # Set caption and app icon.
        pygame.display.set_caption("Alien Invasion")
        self.displayicon = pygame.image.load(self.settings.icon)
        pygame.display.set_icon(self.displayicon)

        # Background
        self.background = pygame.image.load("Assets/bg.bmp")

        # Create an instance to store game statistics,
        # and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        # Ship
        self.ship = Ship(self)
        # Bullet
        self.bullets = pygame.sprite.Group()
        # Aleins
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        # Start Alien Invasion in an active state.
        self.game_active = False
        # Make the Play button and menu screen.
        self.play_button = Button(self, "PLAY")
        self.menu = Menu(self)


    def run_game(self):
        '''Start the main loop for the game.'''
        while True:
            self.check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self.update_screen()           
            self.clock.tick(60)


    def _create_fleet(self):
        '''Creating the fleet of aliens.'''
        # Create an alien and keep adding aliens until there's no room left,
        # spacing betweem aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2*alien_width

            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height


    def _create_alien(self, x_positon, y_position):
        '''Create an alien and place it in the fleet.'''
        new_alien = Alien(self)
        new_alien.x = x_positon
        new_alien.rect.x = x_positon
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)


    def _update_aliens(self):
        '''Update the position of all aliens in the fleet.'''
        self._check_fleet_edges()
        self.aliens.update()

        # Looks for alien_ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Looks for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()


    def _check_fleet_edges(self):
        '''Respond appropriately if any aliens have reached an edge.'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        '''Drop the entire fleet and change the fleet's direction.'''
        for aliens in self.aliens.sprites():
            aliens.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def check_events(self):
        '''Respond to mouse and keypress events.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)


    def _check_keydown_events(self, event):
        '''Respond to keypresses.'''
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Move the ship to the right
            self.ship.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self, event):
        '''Respond to key releases.'''              
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            # Move the ship to the right
            self.ship.moving_left = False


    def _fire_bullet(self):
        '''Create a new bullet and add it to the bullets group.'''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)   


    def _update_bullets(self):
        '''Update position of bullets and get rid of old bullets.'''
        # Update bullet position
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)

        # Check for any bullets that have hit aliens
        #  If so, get rid of the bullets and the alien.

        self._check_bullet_alien_collisons()


    def _check_bullet_alien_collisons(self):
        '''Respond to bullet-alien collisons.'''
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high__score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()


    def _ship_hit(self):
        '''Respond to the ship being hit by an aliens.'''
        if self.stats.ships_left > 0:
            # Decrement ship_left, and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        '''Checks if any aliens have reached the bottom of the screen.'''
        for aliens in self.aliens.sprites():
            if aliens.rect.bottom >= self.settings.screen_height:
                # Treat this the same as the ship got hit
                self._ship_hit()
                break


    def _check_play_button(self, mouse_pos):
        '''Start a new game when the player click Play.'''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset the game statistics.
            self.settings.initialize_dynamic_settings()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)


    def update_screen(self):
        '''Updates images in screen, and flip to the new screen.'''
        self.screen.fill(self.settings.bg_color)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()

        # Draw aliens on the screen
        self.aliens.draw(self.screen)

        # Draw score information
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.game_active:
            self.menu.startup_menu()
            self.play_button.draw_button()

        # Make the most recently draw screen visible
        pygame.display.flip()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()