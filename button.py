import pygame.font

class Button:
    def __init__(self, ai_game, msg, font_size=48, x=None, y=None):
        """Initialize button attributes with customizable position and size."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the button dimensions and properties
        self.width, self.height = 200, 50
        self.button_color = (25, 25, 25)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, font_size)

        # Create the button's rect object and center it or position it manually
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        if x and y:
            self.rect.topleft = (x, y)
        else:
            self.rect.center = self.screen_rect.center  # Default center if no position specified

        self._prep_msg(msg)

    def reset_message(self, msg="Play"):
        """Reset the button's message."""
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn the msg into a rendered image and center the text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw the button and its message to the screen."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)