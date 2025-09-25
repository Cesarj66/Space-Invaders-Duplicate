import pygame as pg
from colors import BLACK, WHITE, GREEN
from button import Button

class TitleScreen:
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.bg_color = BLACK

        # Game title font
        self.title_font = pg.font.Font(None, 120) 
        self.font = pg.font.Font(None, 40)

        # Define colors
        self.white_color = WHITE 
        self.green_color = GREEN

        # Create play and high score buttons
        self.play_button = Button(self.ai_game, "PLAY")
        self.high_score_button = Button(self.ai_game, "HIGH SCORES", font_size=30)

        # Alien images and their point values
        self.alien_images = [
            (pg.image.load('images/ien00.png'), self.settings.type_one_points),
            (pg.image.load('images/ien10.png'), self.settings.type_two_points),
            (pg.image.load('images/ien20.png'), self.settings.type_three_points)
        ]
        self.mothership_image = pg.image.load('images_other/Thugles02.png')  
        self.mothership_points = "???"

    def draw(self):
        self.screen.fill(self.bg_color)  
        self._draw_title()
        self._draw_alien_points()
        self._draw_mothership_points()
        self._draw_buttons()

        pg.display.flip()

    def _draw_title(self):
        title_part1 = self.title_font.render("SPACE", True, self.white_color)
        title_part2 = self.title_font.render("INVADERS", True, self.green_color)

        # Get rectangles for each title part
        title_part1_rect = title_part1.get_rect()
        title_part2_rect = title_part2.get_rect()

        # Calculate the total width of both title parts and center them
        total_title_width = title_part1_rect.width + title_part2_rect.width + 20  # 20-pixel gap between words
        screen_center = self.screen.get_rect().centerx

        # Center both parts relative to the total width
        title_part1_rect.right = screen_center - (total_title_width // 2) + title_part1_rect.width
        title_part2_rect.left = title_part1_rect.right + 20

        title_part1_rect.top = 50
        title_part2_rect.top = 50

        self.screen.blit(title_part1, title_part1_rect)
        self.screen.blit(title_part2, title_part2_rect)

    def _draw_alien_points(self):
        """Draw the three different aliens and their respective point values."""
        y_offset = 200  
        for alien_image, points in self.alien_images:
            alien_rect = alien_image.get_rect()
            alien_rect.centerx = self.screen.get_rect().centerx - 100 
            alien_rect.y = y_offset
            self.screen.blit(alien_image, alien_rect)

            # Display the points value next to each alien
            points_image = self.font.render(f"= {points} POINTS", True, self.white_color)
            points_rect = points_image.get_rect()
            points_rect.left = alien_rect.right + 20
            points_rect.centery = alien_rect.centery
            self.screen.blit(points_image, points_rect)

            y_offset += 80

    def _draw_mothership_points(self):
        mothership_rect = self.mothership_image.get_rect()
        mothership_rect.centerx = self.screen.get_rect().centerx - 100
        mothership_rect.y = 440  
        self.screen.blit(self.mothership_image, mothership_rect)

        points_image = self.font.render(f"= {self.mothership_points} POINTS", True, self.white_color)
        points_rect = points_image.get_rect()
        points_rect.left = mothership_rect.right + 20
        points_rect.centery = mothership_rect.centery
        self.screen.blit(points_image, points_rect)

    def _draw_buttons(self):
        # Position high score button at the bottom of the screen
        self.high_score_button.rect.centerx = self.screen.get_rect().centerx
        self.high_score_button.rect.bottom = self.screen.get_rect().bottom - 50
        self.high_score_button._prep_msg("HIGH SCORES")
        self.high_score_button.draw_button()

        # Position play button above the high score button
        self.play_button.rect.centerx = self.screen.get_rect().centerx
        self.play_button.rect.bottom = self.high_score_button.rect.top - 20 
        self.play_button._prep_msg("PLAY")
        self.play_button.draw_button()

