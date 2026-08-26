import pygame

# Import configuration for colors and fonts
# Ensure config.py is in the same directory
from config import CONFIG 

class Button:
    """
    A reusable UI button for the Pygame visualizer.
    Handles rendering, text display, and click detection.
    """
    def __init__(self, x: int, y: int, width: int, height: int, text: str, color: tuple, text_color: tuple):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        
        # Initialize the font. 
        # None uses the default pygame font, size 20.
        self.font = pygame.font.Font(None, 20)

    def draw(self, surface: pygame.Surface):
        """
        Renders the button rectangle and centers the text inside it.
        """
        pygame.draw.rect(surface, self.color, self.rect)
        
        # Render the text and get its rectangular bounding box
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        surface.blit(text_surface, text_rect)

    def is_clicked(self, event: pygame.event.Event) -> bool:
        """
        Checks if a MOUSEBUTTONDOWN event occurred within the button's boundaries.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

    def update_text(self, new_text: str):
        """
        Updates the button's text. Useful for the speed indicator.
        """
        self.text = new_text