import pygame as pg
from vector import Vector
from point import Point
from laser import Laser 
from pygame.sprite import Sprite
from timer import Timer
from random import randint

class Alien(Sprite):
    alien_images0 = [pg.image.load(f"images/ien0{n}.png") for n in range(2)]
    alien_images1 = [pg.image.load(f"images/ien1{n}.png") for n in range(2)]
    alien_images2 = [pg.image.load(f"images/ien2{n}.png") for n in range(2)]
    alien_images = [alien_images0, alien_images1, alien_images2]
    explosion_images = [pg.image.load(f"images_other/ship_boom{n}.png") for n in range(4)]
    

    def __init__(self, ai_game, v): 
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.v = v
        self.stats = ai_game.stats
        self.sb  = ai_game.sb
        self.settings = ai_game.settings


        self.type = randint(0, 2)
        self.timer = Timer(images=Alien.alien_images[self.type], delta=(self.type+1)*600, start_index=self.type % 2)
        self.explosion_timer = Timer(images=Alien.explosion_images, delta=100, start_index=0, loop_continuously=False)
        self.image = self.timer.current_image()
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width 
        self.rect.y = self.rect.height
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.dying = False
        self.dead = False

    def check_edges(self):
        sr = self.screen.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        r = self.rect 
        return self.x + self.rect.width >= sr.right or self.x <= 0
    
    def start_explosion(self):
        self.dying = True  # Set the alien to dying state

    def update(self):
        if self.dying:
            self.image = self.explosion_timer.current_image() 
            if self.explosion_timer.finished():  
                self.dead = True  
                self.ai_game.fleet.update_fleet_speeds()
                self.kill()
                if self.type == 0:
                    self.stats.score += self.settings.type_one_points
                elif self.type == 1:
                    self.stats.score += self.settings.type_two_points
                elif self.type == 2:
                    self.stats.score += self.settings.type_three_points
                self.sb.prep_score()
                self.sb.check_high_score()
        else:
            self.x += self.v.x
            self.y += self.v.y
            self.image = self.timer.current_image()
            
        self.draw()

    def draw(self): 
        self.rect.x = self.x
        self.rect.y = self.y
        self.screen.blit(self.image, self.rect)


def main():
    print('\n run from alien_invasions.py\n')

if __name__ == "__main__":
    main()