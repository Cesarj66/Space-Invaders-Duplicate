import pygame as pg
import sys 
from vector import Vector 

class Event:
    di = {pg.K_RIGHT: Vector(1, 0), pg.K_LEFT: Vector(-1, 0),
      pg.K_UP: Vector(0, -1), pg.K_DOWN: Vector(0, 1),
      pg.K_d: Vector(1, 0), pg.K_a: Vector(-1, 0),
      pg.K_w: Vector(0, -1), pg.K_s: Vector(0, 1)}

    def __init__(self, ai_game):
        self.ai_game = ai_game 
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.sb = ai_game.sb 
        self.game_active = ai_game.game_active
        self.ship = ai_game.ship
        self.play_button = ai_game.title_screen.play_button

    def check_events(self):
        for event in pg.event.get():
            if (event.type == pg.QUIT) or (event.type == pg.KEYDOWN and event.key == pg.K_q):
                sys.exit()
                return True   # finished is True
            elif event.type == pg.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pg.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if self.ai_game.title_screen_active:
                    if self.ai_game.title_screen.play_button.rect.collidepoint(mouse_pos):
                        self.ai_game.reset_game()
                    elif self.ai_game.title_screen.high_score_button.rect.collidepoint(mouse_pos):
                        self.ai_game.show_high_scores()  # Transition to high score menu
                elif self.ai_game.high_score_menu_active:
                    if self.ai_game.high_scores.back_button.rect.collidepoint(mouse_pos):
                        self.ai_game.show_title_screen()  # Transition back to title screen

    def _check_keydown_events(self, event):
        key = event.key
        if key in Event.di.keys():
            self.ship.v += self.settings.ship_speed * Event.di[key]
        elif event.key == pg.K_SPACE:
            self.ship.open_fire()
        elif event.type == pg.KEYUP:
            if event.key in Event.di.keys():
                self.ship.v = Vector()
            elif event.key == pg.K_SPACE:
                self.ship.cease_fire()

    def _check_keyup_events(self, event):
        if event.key in Event.di.keys():
            self.ship.v = Vector()
        elif event.key == pg.K_SPACE:
            self.ship.cease_fire()