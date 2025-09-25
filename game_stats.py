import pygame as pg
from vector import Vector
from point import Point
from laser import Laser 
import json
import os

class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()

        self.high_scores = self.load_high_scores()  # Load high scores from file
        self.high_score = max(self.high_scores, default=0)  # Initialize high_score

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def load_high_scores(self):
        """Load high scores from a file, ensuring existing scores are kept."""
        filename = "highscore.txt"
        if os.path.isfile(filename):
            with open(filename, "r") as f:
                # Read each line, strip whitespace, and filter out invalid entries
                return [int(line.strip()) for line in f if line.strip().isdigit()]
        return []  # Return empty list if no file exists

    def save_high_scores(self):
        """Save high scores back to the file, preserving the top 10 scores."""
        filename = "highscore.txt"
        with open(filename, "w") as f:
            for score in self.high_scores[:10]:  # Keep only the top 10 scores
                f.write(str(score) + "\n")

    def update_high_scores(self, new_score):
        """Update high scores with a new score if it qualifies."""
        self.high_scores.append(new_score)
        self.high_scores = sorted(self.high_scores, reverse=True)[:10]  # Keep top 10 scores
        self.high_score = max(self.high_scores, default=0)  # Update the high score
        self.save_high_scores()  # Save the updated high scores