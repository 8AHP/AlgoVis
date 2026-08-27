import pygame
import sys

# Import our modular components
from config import CONFIG
from node import Node
from algorithms import bfs_generator
from ui import Button
from maze_generator import recursive_backtracker_generator

# --- Window and Layout Configuration ---
# Calculate the exact pixel dimensions of the grid itself
GRID_WIDTH = CONFIG["COLS"] * (CONFIG["NODE_SIZE"] + CONFIG["MARGIN"]) + CONFIG["MARGIN"]
GRID_HEIGHT = CONFIG["ROWS"] * (CONFIG["NODE_SIZE"] + CONFIG["MARGIN"]) + CONFIG["MARGIN"]

# Define UI bar heights to create space for buttons
TOP_BAR_HEIGHT = 50
BOTTOM_BAR_HEIGHT = 50

# Total window dimensions
WINDOW_WIDTH = GRID_WIDTH
WINDOW_HEIGHT = GRID_HEIGHT + TOP_BAR_HEIGHT + BOTTOM_BAR_HEIGHT

# The Y offset is crucial for translating mouse clicks to grid coordinates
GRID_OFFSET_Y = TOP_BAR_HEIGHT

def initialize_grid():
    """
    Creates and returns a 2D list of Node objects, along with default start and end nodes.
    """
    grid = []
    for r in range(CONFIG["ROWS"]):
        row = []
        for c in range(CONFIG["COLS"]):
            node = Node(r, c)
            row.append(node)
        grid.append(row)
        
    # Set default start and end nodes for immediate usability
    start_node = grid[CONFIG["ROWS"] // 2][2]
    start_node.set_state("START")
    
    end_node = grid[CONFIG["ROWS"] // 2][CONFIG["COLS"] - 3]
    end_node.set_state("END")
    
    return grid, start_node, end_node

def main():
    """
    The main execution loop for the Pathfinding Visualizer.
    Handles events, updates algorithm state, and renders the UI and grid.
    """
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pathfinding Visualizer - BFS")
    clock = pygame.time.Clock()

    # Initialize core state
    grid, start_node, end_node = initialize_grid()
    algorithm_gen = None
    is_running = False
    frame_counter = 0
    speed_delay = 5  # Frames to wait before advancing the algorithm
    
    # Initialize the step counter to track algorithm progress
    step_count = 0
    # Maze generation state
    maze_gen = None
    is_generating_maze = False

    # --- UI Initialization ---
    btn_width = 80
    btn_height = 30
    btn_margin = 10
    
    # Top Bar Buttons
    start_btn = Button(btn_margin, 10, btn_width, btn_height, "START", (39, 174, 96), (255, 255, 255))
    step_counter_btn = Button(btn_margin * 2 + btn_width, 10, 100, btn_height, "STEPS: 0", (41, 128, 185), (255, 255, 255))
    clear_btn = Button(btn_margin * 3 + btn_width + 100, 10, btn_width, btn_height, "CLEAR", (192, 57, 43), (255, 255, 255))
    maze_btn = Button(btn_margin * 4 + btn_width * 2 + 100, 10, btn_width, btn_height, "MAZE", (142, 68, 173), (255, 255, 255))
    
    # Bottom Bar Buttons (Speed Controls)
    speed_down_btn = Button(btn_margin, WINDOW_HEIGHT - BOTTOM_BAR_HEIGHT + 10, 40, btn_height, "-", (127, 140, 141), (255, 255, 255))
    speed_text_btn = Button(btn_margin * 2 + 40, WINDOW_HEIGHT - BOTTOM_BAR_HEIGHT + 10, 120, btn_height, f"Delay: {speed_delay}", (52, 73, 94), (255, 255, 255))
    speed_up_btn = Button(btn_margin * 3 + 160, WINDOW_HEIGHT - BOTTOM_BAR_HEIGHT + 10, 40, btn_height, "+", (127, 140, 141), (255, 255, 255))

    running = True
    while running:
        clock.tick(60) # Cap at 60 FPS for smooth rendering
        
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle UI Button Clicks (Left click only)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_btn.is_clicked(event) and not is_running and not is_generating_maze:
                    # Reset step count when starting a new run
                    step_count = 0
                    step_counter_btn.update_text(f"STEPS: {step_count}")
                    algorithm_gen = bfs_generator(grid, start_node, end_node)
                    is_running = True
                    
                elif maze_btn.is_clicked(event) and not is_running and not is_generating_maze:
                    # Start maze generation
                    maze_gen = recursive_backtracker_generator(grid, start_node, end_node)
                    is_generating_maze = True
                    
                elif clear_btn.is_clicked(event):
                    # Reset grid, step count, and generators
                    step_count = 0
                    step_counter_btn.update_text(f"STEPS: {step_count}")
                    for r in range(CONFIG["ROWS"]):
                        for c in range(CONFIG["COLS"]):
                            if grid[r][c].state not in ["START", "END"]:
                                grid[r][c].set_state("EMPTY")
                    algorithm_gen = None
                    maze_gen = None
                    is_running = False
                    is_generating_maze = False
                    
                elif speed_down_btn.is_clicked(event):
                    if speed_delay < 20:
                        speed_delay += 1
                        speed_text_btn.update_text(f"Delay: {speed_delay}")
                        
                elif speed_up_btn.is_clicked(event):
                    if speed_delay > 1:
                        speed_delay -= 1
                        speed_text_btn.update_text(f"Delay: {speed_delay}")

            # Handle Grid Clicks (Only if algorithm is not running)
            if event.type == pygame.MOUSEBUTTONDOWN and not is_running:
                # CRITICAL: Adjust Y coordinate for the top UI bar offset
                adjusted_y = event.pos[1] - GRID_OFFSET_Y
                
                # Calculate grid coordinates using integer division
                col = event.pos[0] // (CONFIG["NODE_SIZE"] + CONFIG["MARGIN"])
                row = adjusted_y // (CONFIG["NODE_SIZE"] + CONFIG["MARGIN"])
                
                # Validate boundaries to prevent index errors
                if 0 <= row < CONFIG["ROWS"] and 0 <= col < CONFIG["COLS"]:
                    clicked_node = grid[row][col]
                    
                    if event.button == 1: # Left click: Toggle Wall
                        if clicked_node.state == "EMPTY":
                            clicked_node.set_state("WALL")
                        elif clicked_node.state == "WALL":
                            clicked_node.set_state("EMPTY")
                    elif event.button == 3: # Right click: Set Start
                        if start_node: 
                            start_node.set_state("EMPTY")
                        clicked_node.set_state("START")
                        start_node = clicked_node
                    elif event.button == 2: # Middle click: Set End
                        if end_node: 
                            end_node.set_state("EMPTY")
                        clicked_node.set_state("END")
                        end_node = clicked_node

        # 2. Algorithm Execution (Non-blocking speed control)
        if is_running and algorithm_gen is not None:
            frame_counter += 1
            
            # Only advance the algorithm if enough frames have passed
            if frame_counter >= speed_delay:
                frame_counter = 0
                try:
                    # Unpack the tuple from the generator
                    running_state, is_exploring = next(algorithm_gen)
                    
                    # If the generator signals it is completely done
                    if not running_state:
                        is_running = False
                        algorithm_gen = None
                    # Only increment the step counter during the exploration phase
                    elif is_exploring:
                        step_count += 1
                        step_counter_btn.update_text(f"STEPS: {step_count}")
                        
                except StopIteration:
                    # Fallback safety net if the generator exhausts without yielding (False, False)
                    is_running = False
                    algorithm_gen = None
        # 3. Maze Generation Execution (Non-blocking speed control)
        if is_generating_maze and maze_gen is not None:
            frame_counter += 1
            
            # Only advance the maze generation if enough frames have passed
            if frame_counter >= speed_delay:
                frame_counter = 0
                try:
                    next(maze_gen)
                except StopIteration:
                    # Maze generation is complete
                    is_generating_maze = False
                    maze_gen = None

        # 3. Rendering
        # Clear the screen with the background color to prevent the black screen issue
        screen.fill(CONFIG["COLORS"]["BACKGROUND"])
        
        # Draw Top Bar Background and Buttons
        pygame.draw.rect(screen, (236, 240, 241), (0, 0, WINDOW_WIDTH, TOP_BAR_HEIGHT))
        start_btn.draw(screen)
        step_counter_btn.draw(screen)
        clear_btn.draw(screen)
        maze_btn.draw(screen)
        
        # Draw Bottom Bar Background and Buttons
        pygame.draw.rect(screen, (236, 240, 241), (0, WINDOW_HEIGHT - BOTTOM_BAR_HEIGHT, WINDOW_WIDTH, BOTTOM_BAR_HEIGHT))
        speed_down_btn.draw(screen)
        speed_text_btn.draw(screen)
        speed_up_btn.draw(screen)

        # Draw the Grid (Shifted down by GRID_OFFSET_Y)
        for r in range(CONFIG["ROWS"]):
            for c in range(CONFIG["COLS"]):
                node = grid[r][c]
                
                # Calculate the drawing Y coordinate on the fly to avoid mutating the node's actual state
                draw_y = node.y + GRID_OFFSET_Y
                
                # Get the color based on the node's current state
                color = CONFIG["COLORS"].get(node.state, CONFIG["COLORS"]["BACKGROUND"])
                rect = pygame.Rect(node.x, draw_y, CONFIG["NODE_SIZE"], CONFIG["NODE_SIZE"])
                
                # Draw the filled background of the node
                pygame.draw.rect(screen, color, rect)
                
                # Draw the 1-pixel border to create the grid page effect
                border_color = CONFIG["COLORS"]["BORDER"]
                pygame.draw.rect(screen, border_color, rect, width=1)

        # Update the display to show the drawn frame
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()