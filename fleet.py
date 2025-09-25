import pygame as pg
from vector import Vector
from random import choice
from laser import Laser 
from alien import Alien
from pygame.sprite import Sprite
from random import uniform


class Fleet(Sprite):
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.ship = ai_game.ship
        self.aliens = pg.sprite.Group()
        self.fleet_lasers = pg.sprite.Group()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.sb = ai_game.sb
        self.spacing = 1.4
        self.initial_alien_count = 0
        self.music_thresholds = [0.8, 0.4]
        self.music_speed_level = 0
        self.shooter_alien = None
        self.last_shooter_change_time = pg.time.get_ticks()  # Timer for shooter change
        self.shooter_change_interval = 1000  # Change shooter every second
        self.last_shot_time = 0  # Store the last shot time
        self.shoot_interval = uniform(500, 1000)

    def reset_fleet(self):
        self.aliens.empty()
        self.fleet_lasers.empty()
        self.settings.initialize_dynamic_settings()
        self.create_fleet()
        self.assign_shooter()

        

    def create_fleet(self):
        self.v = Vector(self.settings.alien_speed, 0)
        self.alien = Alien(ai_game=self.ai_game, v=self.v)
        alien_height = self.alien.rect.height
        current_y = alien_height
        while current_y < (self.settings.scr_height - self.spacing * 6 * alien_height):
            self.create_row(current_y)
            current_y += self.spacing * alien_height
        self.initial_alien_count = len(self.aliens)
        if self.ai_game.game_active:
            self.ai_game.mothership.reset()
            self.ai_game.sound.reset_track()
        self.music_speed_level = 0
        
    def create_row(self, y):
        alien = Alien(ai_game=self.ai_game, v=self.v)
        alien_width = alien.rect.width
        current_x = alien_width
        while current_x < (self.settings.scr_width - self.spacing * alien_width):
            new_alien = Alien(self.ai_game, v=self.v)
            new_alien.rect.y = y
            new_alien.y = y
            new_alien.x = current_x
            new_alien.rect.x = current_x
            self.aliens.add(new_alien)
            current_x += self.spacing * alien_width

    def update_fleet_speeds(self):
        self.v.x *= self.settings.speedup_scale
    
    def adjust_music_speed(self):
        """Adjust the music speed based on the number of remaining aliens."""
        alien_count = len(self.aliens)
        alien_percentage = alien_count / self.initial_alien_count
        
        # Loop through the thresholds to change the music speed
        if self.music_speed_level < len(self.music_thresholds) and alien_percentage < self.music_thresholds[self.music_speed_level]:
            self.ai_game.sound.change_music_speed(self.music_speed_level + 1)
            self.music_speed_level += 1
           
    def assign_shooter(self):
        """Assign a single alien to shoot for the entire game."""
        if self.aliens:  
            # Randomly pick one alien as the shooter
            self.shooter_alien = choice(self.aliens.sprites())
            # Disable shooting for all aliens except the designated shooter
            for alien in self.aliens:
                if alien != self.shooter_alien:
                    alien.can_shoot = False
            self.shooter_alien.can_shoot = True

    def shoot(self):
        """Make the alien shoot a laser downward."""
        # Create a new laser and add it to the fleet_lasers group
        laser = Laser(self.ai_game, shooter=self.shooter_alien, direction=1)
        laser.rect.midtop = self.shooter_alien.rect.midbottom 
        self.fleet_lasers.add(laser)
        self.last_shot_time = self.current_time

    def check_edges(self):
        for alien in self.aliens:
            if alien.check_edges():
                return True
        return False

    def check_bottom(self):
        for alien in self.aliens:
            if alien.rect.bottom >= self.settings.scr_height:
                self.ship.ship_hit()
                return True
        return False

    def update(self):
        if not self.alien.dying:
            collisions = pg.sprite.groupcollide(self.ship.lasers, self.aliens, True, False)

            if collisions:
                for aliens in collisions.values():
                    for alien in aliens:
                        alien.start_explosion()
                        self.settings.increase_speed()


        if not self.aliens:
            self.ship.lasers.empty()
            self.create_fleet()
            self.assign_shooter()  # Assign a new shooter when the fleet is reset
            if self.ai_game.game_active:
                self.stats.level += 1
            self.sb.prep_level()
            return
        
        if not self.ai_game.mothership.appear:
            self.adjust_music_speed()
        
        if not self.ship.dying:
            if pg.sprite.spritecollideany(self.ship, self.aliens):
                print("Ship hit!")
                self.ship.kill()
                self.ship.ship_hit()
                return
        
            if pg.sprite.spritecollideany(self.ship, self.fleet_lasers):
                print("Ship hit!")
                self.ship.ship_hit()
                return

        if self.check_bottom():
            return

        if self.check_edges():
            self.v.x *= -1
            for alien in self.aliens:
                alien.v.x = self.v.x
                alien.y += self.settings.fleet_drop_speed

        self.current_time = pg.time.get_ticks()
        if self.current_time - self.last_shooter_change_time >= self.shooter_change_interval:
            self.assign_shooter()  
            self.last_shooter_change_time = self.current_time

        # Update all aliens' movement 
        for alien in self.aliens:
            alien.update()

        # Update fleet lasers 
        self.fleet_lasers.update()
        for laser in self.fleet_lasers.copy():
            if laser.rect.top >= self.screen.get_rect().bottom:
                self.fleet_lasers.remove(laser)

        for laser in self.fleet_lasers.sprites():
            laser.draw()


        # Shoot at regular intervals
        if self.current_time - self.last_shot_time >= self.shoot_interval:
            self.shoot()

    def draw(self): pass
        # for alien in self.aliens:
        #     alien.draw()

def main():
    print('\n run from alien_invasions.py\n')

if __name__ == "__main__":
    main()