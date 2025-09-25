from colors import DARK_GREY, RED
import random

class Settings:
    def __init__(self):
        self.scr_width = 1200
        self.scr_height = 800
        self.bg_color = DARK_GREY
        self.w_h = (self.scr_width, self.scr_height)

        # laser settings
        self.laser_speed = 3.0
        self.laser_width = 10
        self.laser_height = 15
        self.laser_color = RED

        self.ship_limit = 3
        self.ship_fire_every = 25
        self.fleet_drop_speed = 10

        self.speedup_scale = 1.005
        self.score_scale = 1.001

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 10.0
        self.laser_speed = 2.5
        self.alien_speed = 2.0

        self.type_one_points = 50
        self.type_two_points = 100
        self.type_three_points = 150
    
    def generate_mothership_points(self):
        return random.randint(250, 1000)

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        #self.ship_speed *= self.speedup_scale
        self.laser_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.type_one_points = int(self.type_one_points * self.score_scale)
        self.type_two_points = int(self.type_two_points * self.score_scale)
        self.type_three_points = int(self.type_three_points * self.score_scale)


def main():
    print('\n*** message from settings.py --- run from alien_invasions.py\n')

if __name__ == "__main__":
    main()