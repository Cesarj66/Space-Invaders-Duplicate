import pygame as pg
from pygame.sprite import Sprite
from random import randint

class Laser(Sprite):
    @staticmethod
    def random_color(): 
        return (randint(0, 255), randint(0, 255), randint(0, 255))
    
    def __init__(self, ai_game, shooter, direction=-1):  # Pass the shooter (alien or ship)
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = Laser.random_color()
        self.rect = pg.Rect(0, 0, self.settings.laser_width, 
                                self.settings.laser_height)
        
        if direction == -1:
            # Fired by the ship
            self.rect.midtop = shooter.rect.midtop
        elif direction == 1:
            # Fired by the alien
            self.rect.midbottom = shooter.rect.midbottom  # Use the passed alien's position
        
        self.y = float(self.rect.y)
        self.direction = direction  # -1 for upward (ship), 1 for downward (alien)

    def update(self):
        """Move the laser based on its direction."""
        self.y += self.direction * self.settings.laser_speed  # Move up for ship, down for alien
        self.rect.y = self.y

    def draw(self):
        """Draw the laser to the screen."""
        pg.draw.rect(self.screen, self.color, self.rect)

def main():
    print("\nYou have to run from alien_invasion.py\n")

if __name__ == "__main__":
    main()