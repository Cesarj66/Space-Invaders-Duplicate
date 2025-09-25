import pygame as pg
from vector import Vector
from timer import Timer
from sound import Sound
from pygame.sprite import Sprite
from random import randint

class Mothership(Sprite):
    mothership_images = [pg.image.load(f"images_other/Thugles0{n}.png") for n in range(4)]  # Load appropriate images
    mothership_explosion_images = [pg.image.load(f"images_other/thugles_explosion{n}.png") for n in range(8)]  # Explosion images

    def __init__(self, ai_game, v = Vector):
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.v = v
        self.ship = ai_game.ship
        self.stats = ai_game.stats
        self.sb =  ai_game.sb
        self.settings = ai_game.settings

        self.sound = Sound()
        self.timer = Timer(images=Mothership.mothership_images, delta=500, loop_continuously=True)
        self.explosion_timer = Timer(images=Mothership.mothership_explosion_images, delta=100, loop_continuously=False)

        self.image = self.timer.current_image()
        self.rect = self.image.get_rect()
        
        # Starting position off-screen and at random X position at the top
        self.rect.x = randint(0, self.screen_rect.width - self.rect.width)
        self.rect.y = -self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.appear = False 
        self.dying = False 
        self.dead = False 
        self.appear_time = 0  
        self.direction = 1
        self.leaving = False  
        self.game_start_time = pg.time.get_ticks()
        self.last_disappear_time = 0 
        self.mothership_delay = 12000
        self.display_points = False
        self.point_display_time = 0 

    def check_edges(self):
        """Check if the mothership has hit the screen edges."""
        sr = self.screen.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        return self.x + self.rect.width >= sr.right or self.x <= 0
    
    def start(self):
        """Make the mothership appear and reset its position."""
        self.appear = True
        self.rect.y = -self.rect.height
        self.x = randint(0, self.screen_rect.width - self.rect.width)
        self.y = float(self.rect.y)
        self.appear_time = pg.time.get_ticks() 
        self.points = round(self.settings.generate_mothership_points(), -1)  # Randomize points each appearance
        self.sound.play_thugles()     

    def start_explosion(self):
        """Trigger the mothership's explosion."""
        self.dying = True
        self.explosion_timer = Timer(images=Mothership.mothership_explosion_images, delta=100, loop_continuously=False)
        self.point_display_time = pg.time.get_ticks()
        self.display_points = True

    def draw_points(self):
        """Draw mothership points after explosion"""
        font = pg.font.SysFont(None, 48)
        points_image = font.render(str(self.points), True, (0, 0, 0))
        points_rect = points_image.get_rect()
        points_rect.center = self.rect.center
        points_rect.x += 5
        self.screen.blit(points_image, points_rect)

    def reset(self):
        """Reset the mothership's state when the game restarts."""
        self.appear = False  
        self.dying = False  
        self.dead = False  
        self.leaving = False  
        self.last_disappear_time = pg.time.get_ticks()  
        self.game_start_time = pg.time.get_ticks()  
        self.rect.y = -self.rect.height  # Reset position off-screen
        self.x = randint(0, self.screen_rect.width - self.rect.width)
        self.y = float(self.rect.y)
        self.display_points = False  
        self.sound.thugles.stop()
        self.sound.play_background()

    def update(self):
        if self.appear and not self.dying and not self.leaving:
            if pg.sprite.spritecollideany(self, self.ship.lasers):
                self.start_explosion()  # Start the explosion animation
                laser = pg.sprite.spritecollideany(self, self.ai_game.ship.lasers)  
                self.ai_game.ship.lasers.remove(laser) 
                self.stats.score += self.points
                self.sb.prep_score()
                self.sb.check_high_score()

            if not self.ship.dying:
                if pg.sprite.collide_rect(self, self.ai_game.ship):
                    # Trigger the ship's explosion
                    self.ship.ship_hit()

        if self.dying:
            self.image = self.explosion_timer.current_image()
            if self.explosion_timer.finished():
                self.reset()
            self.draw()

            if self.display_points and pg.time.get_ticks() - self.point_display_time < 1500:
                self.draw_points()
            else:
                self.display_points = False  

            return

        current_time = pg.time.get_ticks()
        # Wait for at least 10 seconds after the game start before considering to show the mothership
        if not self.appear and current_time - self.last_disappear_time < self.mothership_delay:
            return 
        
        if not self.appear:
            # The mothership should randomly appear after some time
            if randint(1, 500) == 1:
                self.start()
            return

        if not self.leaving:
            if self.y < 50:
                self.y += 2
            else:
                # Mothership is fully visible, move side to side
                self.x += self.direction * 3
                if self.check_edges():
                    self.direction *= -1

                # Check if enough time has passed to make the mothership start flying back up
                if pg.time.get_ticks() - self.appear_time > 15000:
                    self.leaving = True
                    

        else:
            # Move the mothership back up off the screen
            self.sound.thugles.fadeout(2000)
            self.y -= 2
            if self.y + self.rect.height < -20:
                self.appear = False
                self.leaving = False
                self.last_disappear_time = pg.time.get_ticks() 
                self.sound.play_background()

        self.image = self.timer.current_image()
        self.rect.x, self.rect.y = self.x, self.y
        self.draw()

    def draw(self):
        self.screen.blit(self.image, self.rect)