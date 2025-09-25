import sys
import pygame as pg
from colors import OFF_WHITE, DARK_GREY
from settings import Settings
from ship import Ship
from vector import Vector
from fleet import Fleet
from game_stats import GameStats
from scoreboard import Scoreboard
from event import Event
from barrier import Barriers
from sound import Sound
from mothership import Mothership
from title_screen import TitleScreen
from high_scores import HighScores



class AlienInvasion:
    def __init__(self):
        pg.init()   
        self.clock = pg.time.Clock()
        self.settings = Settings()
        self.screen = pg.display.set_mode(self.settings.w_h)
        self.screen_rect = self.screen.get_rect()
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.sound = Sound()
        self.ship = Ship(ai_game=self)
        self.fleet = Fleet(ai_game=self)
        self.mothership = Mothership(ai_game=self)
        self.ship.set_fleet(self.fleet)
        self.ship.set_sb(self.sb)
        self.barriers = Barriers(ai_game=self)

        pg.display.set_caption("Space Invasion")
        self.bg_color = self.settings.bg_color
        self.title_screen = TitleScreen(ai_game=self)
        self.high_scores = HighScores(self)

        # Start Alien Invasion in an inactive state.
        self.game_active = False
        self.first = True
        self.title_screen_active = True  
        self.high_score_menu_active = False
        
        self.event = Event(self)

    def show_title_screen(self):
        """Return to the title screen from the high score menu."""
        self.title_screen_active = True
        self.high_score_menu_active = False

    def show_high_scores(self):
        self.title_screen_active = False
        self.high_score_menu_active = True

    def game_over(self):
        print("Game over!") 
        self.sound.play_gameover()
        self.game_active = False
        self.high_score_menu_active = False  
        self.title_screen_active = True  
        # Check if current score is a high score
        if self.stats.high_scores:
            if self.stats.score > self.stats.high_scores[-1]:  # Check if the score is in top 10
                self.stats.update_high_scores(self.stats.score)  
        else:
            # If no high scores exist, add the score directly
            self.stats.update_high_scores(self.stats.score)
            
        pg.mouse.set_visible(True)

    def reset_game(self):
        self.stats.reset_stats()
        self.sb.prep_score_level_ships()
        self.game_active = True
        self.title_screen_active = False  
        self.barriers.reset()
        self.ship.reset_ship()
        self.fleet.reset_fleet()
        self.mothership.reset()
        pg.mouse.set_visible(False)

    def restart_game(self):
        self.game_active = False
        self.first = True
        self.reset_game()

    def run_game(self):
        self.finished = False
        self.first = True
        self.game_active = False
        while not self.finished:
            self.finished = self.event.check_events()
            if self.title_screen_active:
                self.screen.fill(self.bg_color)
                self.title_screen.draw()  
            elif self.high_score_menu_active:
                self.screen.fill(self.high_scores.bg_color)
                self.high_scores.draw()  
            elif self.game_active:
                self.screen.fill(self.bg_color)
                self.ship.update()
                self.fleet.update()
                self.sb.show_score()
                self.barriers.update()
                self.mothership.update()
                
                
            pg.display.flip()

            self.clock.tick(60)
        sys.exit()

      

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
