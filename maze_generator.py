import random
from config import CONFIG

def recursive_backtracker_generator(grid, start_node, end_node):
    """
    Generator function for the Recursive Backtracker maze generation algorithm.
    Creates a perfect maze by carving paths through a grid full of walls.
    Yields after carving each new passage to allow for visualization.
    """
    # Initialize all cells as walls
    for r in range(CONFIG["ROWS"]):
        for c in range(CONFIG["COLS"]):
            if grid[r][c] != start_node and grid[r][c] != end_node:
                grid[r][c].set_state("WALL")
    
    # Choose a random starting cell for the maze generation
    # Avoid the row/column of start and end nodes to prevent overwriting them
    start_row = random.randint(0, CONFIG["ROWS"] - 1)
    start_col = random.randint(0, CONFIG["COLS"] - 1)
    
    # Ensure we don't start on the start or end node
    while grid[start_row][start_col] == start_node or grid[start_row][start_col] == end_node:
        start_row = random.randint(0, CONFIG["ROWS"] - 1)
        start_col = random.randint(0, CONFIG["COLS"] - 1)
    
    start_cell = grid[start_row][start_col]
    start_cell.set_state("EMPTY")  # Carve the starting cell
    
    # Stack for the backtracking algorithm
    stack = [start_cell]
    
    # Define the 4 cardinal directions (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while stack:
        current = stack[-1]  # Peek at the top of the stack
        
        # Find all unvisited neighbors (walls that are 2 cells away)
        unvisited_neighbors = []
        
        for dr, dc in directions:
            # Calculate the neighbor cell (2 steps away)
            neighbor_row = current.row + dr * 2
            neighbor_col = current.col + dc * 2
            
            # Check if the neighbor is within bounds
            if 0 <= neighbor_row < CONFIG["ROWS"] and 0 <= neighbor_col < CONFIG["COLS"]:
                neighbor = grid[neighbor_row][neighbor_col]
                
                # Check if the neighbor is still a wall and not start/end
                if neighbor.state == "WALL" and neighbor != start_node and neighbor != end_node:
                    unvisited_neighbors.append((neighbor, dr, dc))
        
        if unvisited_neighbors:
            # Choose a random unvisited neighbor
            chosen_neighbor, dr, dc = random.choice(unvisited_neighbors)
            
            # Calculate the wall between current and chosen neighbor
            wall_row = current.row + dr
            wall_col = current.col + dc
            wall = grid[wall_row][wall_col]
            
            # Carve the passage: remove the wall and mark the neighbor as visited
            if wall != start_node and wall != end_node:
                wall.set_state("EMPTY")
            
            chosen_neighbor.set_state("EMPTY")
            stack.append(chosen_neighbor)
            
            # Yield control to allow visualization of this step
            yield True
        else:
            # Backtrack: pop the current cell from the stack
            stack.pop()
            
            # Yield occasionally during backtracking for smoother visualization
            if len(stack) % 5 == 0:
                yield True
    
    # Signal completion
    yield False

def get_maze_neighbors(cell, grid):
    """
    Helper function to get valid neighbors for maze generation.
    Used to find cells that are 2 steps away (separated by a wall).
    """
    neighbors = []
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    
    for dr, dc in directions:
        new_row = cell.row + dr
        new_col = cell.col + dc
        
        if 0 <= new_row < CONFIG["ROWS"] and 0 <= new_col < CONFIG["COLS"]:
            neighbors.append(grid[new_row][new_col])
    
    return neighbors