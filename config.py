# Configuration constants for the visualizer
# All values are centralized to prevent magic numbers in the codebase
CONFIG = {
    "ROWS": 30,
    "COLS": 30,
    "NODE_SIZE": 25,
    # Changed from 2 to 1 to allow the borders to touch and form a continuous grid
    "MARGIN": 1, 
    "COLORS": {
        "BACKGROUND": (255, 255, 255),
        # Light gray for the grid page borders
        "BORDER": (189, 195, 199), 
        "GRID_LINES": (200, 200, 200),
        "WALL": (44, 62, 80),
        "START": (39, 174, 96),
        "END": (192, 57, 43),
        "OPEN": (150, 200, 250),
        "CLOSED": (15, 82, 186),
        "PATH": (241, 196, 15)
    }
}