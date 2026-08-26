from collections import deque
from config import CONFIG


def get_neighbors(node, grid):
    """
    Returns a list of valid neighboring nodes for a given node.
    Checks grid boundaries to prevent index out-of-bounds errors.
    Strictly evaluates 4-way neighbors (up, down, left, right).
    """
    neighbors = []
    row = node.row
    col = node.col
    
    # Define the 4 directional offsets as coordinate deltas
    directions = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1)    # Right
    ]
    
    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc
        
        # Validate that the new coordinates are within the grid boundaries
        if 0 <= new_row < CONFIG["ROWS"] and 0 <= new_col < CONFIG["COLS"]:
            neighbors.append(grid[new_row][new_col])
            
    return neighbors

def bfs_generator(grid, start_node, end_node):
    """
    Generator function for the Breadth-First Search algorithm.
    Yields a tuple: (is_running, is_exploring).
    is_exploring is True during the search phase, False during path reconstruction.
    """
    queue = deque([start_node])
    came_from = {start_node: None}
    
    # Start node state is already "START", no need to change it to "OPEN"

    while queue:
        current = queue.popleft()

        if current == end_node:
            break

        # Protect the start node from being overwritten to "CLOSED"
        if current != start_node:
            current.set_state("CLOSED")

        for neighbor in get_neighbors(current, grid):
            # Allow traversal into empty nodes or the end node itself
            if neighbor.state == "EMPTY" or neighbor == end_node:
                if neighbor not in came_from:
                    came_from[neighbor] = current
                    # Protect the end node from being overwritten to "OPEN"
                    if neighbor != end_node:
                        neighbor.set_state("OPEN")
                    queue.append(neighbor)
        
        # Yield control: algorithm is running, and we are in the exploration phase
        yield (True, True)

    # --- Path Reconstruction Phase ---
    if end_node in came_from:
        current = end_node
        end_state = end_node.state 
        
        while current is not None:
            # Protect start and end nodes from being overwritten to "PATH"
            if current != start_node and current != end_node:
                current.set_state("PATH")
            current = came_from[current]
            
            # Yield control: algorithm is running, but we are in the reconstruction phase
            yield (True, False)
            
        # Restore the end node state just in case
        end_node.set_state(end_state)

    # Signal completion: algorithm is not running
    yield (False, False)