import tkinter as tk
from tkinter import filedialog
from config import CONFIG

def open_blueprint_dialog():
    """
    Opens a native OS file dialog to select a .txt blueprint file.
    Uses tkinter hidden in the background to prevent UI conflicts with Pygame.
    Returns the absolute file path as a string, or None if canceled.
    """
    # Initialize a hidden tkinter root window
    root = tk.Tk()
    root.withdraw() 
    
    # Open the file dialog
    file_path = filedialog.askopenfilename(
        title="Select Maze Blueprint",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    
    # Destroy the hidden tkinter window immediately to free resources
    root.destroy()
    
    return file_path if file_path else None

def load_blueprint(file_path, grid):
    """
    Parses a text file and updates the grid states accordingly.
    Validates that the file dimensions exactly match the CONFIG dimensions.
    
    Returns a tuple: (start_node, end_node)
    Raises ValueError if the file format is invalid.
    """
    start_node = None
    end_node = None
    
    with open(file_path, 'r') as file:
        # splitlines() handles both Windows (\r\n) and Unix (\n) line endings safely
        lines = file.read().splitlines()
        
    # Strict validation: The file must have the exact number of rows defined in CONFIG
    if len(lines) != CONFIG["ROWS"]:
        raise ValueError(f"Invalid blueprint: Expected {CONFIG['ROWS']} rows, got {len(lines)}.")
        
    for r, line in enumerate(lines):
        # Strict validation: Every row must have the exact number of columns
        if len(line) != CONFIG["COLS"]:
            raise ValueError(f"Invalid blueprint: Row {r} has {len(line)} columns, expected {CONFIG['COLS']}.")
            
        for c, char in enumerate(line):
            node = grid[r][c]
            
            if char == '#':
                node.set_state("WALL")
            elif char == '.':
                node.set_state("EMPTY")
            elif char == 'S':
                node.set_state("START")
                start_node = node
            elif char == 'E':
                node.set_state("END")
                end_node = node
            else:
                # Reject unknown characters to prevent silent failures
                raise ValueError(f"Invalid character '{char}' at row {r}, col {c}.")
                
    # A valid blueprint MUST contain exactly one Start and one End node
    if start_node is None or end_node is None:
        raise ValueError("Blueprint must contain exactly one 'S' (Start) and one 'E' (End).")
        
    return start_node, end_node