import pygame as pg
from colors import BLACK, WHITE
from button import Button

class HighScores:
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.font = pg.font.Font(None, 40)
        self.title_font = pg.font.Font(None, 80)
        self.text_color = WHITE  
        self.bg_color = BLACK

        self.back_button = Button(ai_game, "BACK")

    def draw(self):
        """Draw the high score menu."""
        self.screen.fill(self.bg_color)  
        
        # Draw menu title
        title_image = self.title_font.render("HIGH SCORES", True, self.text_color)
        title_rect = title_image.get_rect()
        title_rect.center = (self.screen_rect.centerx, 100)
        self.screen.blit(title_image, title_rect)

        # Draw back button
        self.back_button.rect.centerx = self.screen_rect.centerx
        self.back_button.rect.bottom = self.screen_rect.bottom - 50  
        self.back_button._prep_msg("BACK")
        self.back_button.draw_button()

        # Draw the top 10 high scores
        high_scores = self.ai_game.stats.high_scores
        y_offset = 150 

        for i, score in enumerate(high_scores[:10], 1):  # Limit to 10 high scores
            score_str = f"{i}. {score}"
            score_image = self.font.render(score_str, True, (255, 255, 255))
            score_rect = score_image.get_rect()
            score_rect.centerx = self.screen_rect.centerx
            score_rect.y = y_offset
            self.screen.blit(score_image, score_rect)
            y_offset += 40  

        pg.display.flip()
