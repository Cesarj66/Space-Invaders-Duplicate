import pygame as pg
from vector import Vector
from point import Point
from laser import Laser 
from timer import Timer
from time import sleep
from pygame.sprite import Sprite

class Ship(Sprite):
    ship_explosion_images = [pg.image.load(f"images/ship_boom{n}.png") for n in range(9)]


    def __init__(self, ai_game, v=Vector()):
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.stats = ai_game.stats
        self.settings = ai_game.settings
        self.sb = None
        
        self.image = pg.image.load('images/ship.bmp')
        self.explosion_timer = Timer(images=Ship.ship_explosion_images, delta=100, 
                                     start_index=0, loop_continuously=False)
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom
        scr_r = self.screen_rect 
        self.x = float(scr_r.midbottom[0])
        self.y = float(scr_r.height)
        self.v = v
        self.lasers = pg.sprite.Group()
        self.dying = False
        self.firing = False
        self.fleet = None
        self.fired = 0

    def set_fleet(self, fleet): self.fleet = fleet 

    def set_sb(self, sb): self.sb = sb

    def reset_ship(self):
        self.lasers.empty()
        self.center_ship()

    def center_ship(self):         
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def bound(self):
        x, y, scr_r = self.x, self.y, self.screen_rect
        self.x = max(0, min(x, scr_r.width - self.rect.width)) 
        self.y = max(0, min(y, scr_r.height - self.rect.height))

    def start_explosion(self):
        """Trigger the alien's explosion animation when hit by a laser."""
        self.dying = True  # Set the alien to dying state
        self.explosion_timer = Timer(images=Ship.ship_explosion_images, delta=100, loop_continuously=False)  # Reinitialize the timer

    def ship_hit(self):
        """Trigger the ship's explosion animation when hit."""
        self.dying = True  # Set the alien to dying state
        self.stats.ships_left -= 1
        print(f"Only {self.stats.ships_left} ships left now")
        if  self.stats.ships_left > 0:
            print("Explosion started, ship is dying")  # Debugging
            self.explosion_timer = Timer(images=Ship.ship_explosion_images, delta=100, loop_continuously=False)  # Reinitialize the timer
            self.sb.prep_ships()
            self.lasers.empty()
            self.fleet.fleet_lasers.empty()
            self.fleet.aliens.empty()
            self.fleet.create_fleet()
            self.ai_game.mothership.reset()
        else:
            self.ai_game.game_over()

    def fire_laser(self):
        self.fired += 1
        if self.fired % self.settings.ship_fire_every != 0: return
        laser = Laser(self.ai_game, shooter=self, direction=-1) 
        self.lasers.add(laser)
        
    def open_fire(self): self.firing = True 

    def cease_fire(self): self.firing = False

    def update(self):
        if self.dying:
            self.image = self.explosion_timer.current_image()
            if self.explosion_timer.finished():
                self.dying = False
                self.center_ship()
                self.image = pg.image.load('images/ship.bmp')
                if self.stats.ships_left <= 0:
                    self.ai_game.game_over()
        else:
            self.x += self.v.x 
            self.y += self.v.y
            self.bound()
            if self.firing:
                self.fire_laser()
            self.lasers.update()
            for laser in self.lasers.copy():
                if laser.rect.bottom <= 0:
                    self.lasers.remove(laser)
            for laser in self.lasers.sprites():
                laser.draw() 
        self.draw()

    def draw(self): 
        self.rect.x, self.rect.y = self.x, self.y
        self.screen.blit(self.image, self.rect)

def main():
    print('\n*** message from ship.py --- run from alien_invasions.py\n')

if __name__ == "__main__":
    main()
