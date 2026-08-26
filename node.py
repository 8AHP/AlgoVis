import pygame
from config import CONFIG

class Node:
    """
    Represents a single cell in the pathfinding grid.
    Tracks its position, state, and rendering properties.
    """
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        # Calculate pixel coordinates based on configuration
        self.x = col * (CONFIG["NODE_SIZE"] + CONFIG["MARGIN"]) + CONFIG["MARGIN"]
        self.y = row * (CONFIG["NODE_SIZE"] + CONFIG["MARGIN"]) + CONFIG["MARGIN"]
        self.state = "EMPTY"

    def set_state(self, new_state: str):
        """
        Updates the node state. 
        Validates against allowed states to prevent runtime errors.
        """
        allowed_states = ["EMPTY", "WALL", "START", "END", "OPEN", "CLOSED", "PATH"]
        if new_state in allowed_states:
            self.state = new_state
        else:
            raise ValueError(f"Invalid state: {new_state}. Must be one of {allowed_states}")

    def draw(self, surface: pygame.Surface):
        """
        Renders the node on the given pygame surface based on its current state.
        Draws a filled rectangle and a 1-pixel border to create the grid page effect.
        """
        color = CONFIG["COLORS"].get(self.state, CONFIG["COLORS"]["BACKGROUND"])
        rect = pygame.Rect(self.x, self.y, CONFIG["NODE_SIZE"], CONFIG["NODE_SIZE"])
        
        # Draw the filled background of the node
        pygame.draw.rect(surface, color, rect)
        
        # Draw a 1-pixel border around the node to define the grid lines
        border_color = CONFIG["COLORS"]["BORDER"]
        pygame.draw.rect(surface, border_color, rect, width=1)