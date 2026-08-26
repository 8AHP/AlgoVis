# Interactive Pathfinding Visualizer

A modular, interactive Python application built with Pygame that visually demonstrates the Breadth-First Search (BFS) algorithm on a 2D grid. This project was built to explore algorithmic visualization, event-driven UI design, and clean software architecture.

## Features

- **Real-Time Visualization:** Watch the algorithms explore the grid uniformly, expanding outward like a wave until it finds the target.
- **Step-by-Step Execution:** Pause the continuous run and advance the algorithm one step at a time to deeply analyze the decision-making process.
- **Dynamic Speed Control:** Adjust the visualization speed on the fly using discrete UI buttons.
- **Interactive Grid:** Click to place walls, set start points, and define targets. 
- **Path Reconstruction:** Automatically traces and highlights the shortest path once the target is found.
- **Modular Architecture:** Cleanly separated concerns across multiple files for maintainability and scalability.

## Architecture

This project strictly follows the Separation of Concerns principle. Instead of dumping all logic into a single script, the codebase is divided into five distinct modules:

- `main.py`: The conductor. Handles the Pygame initialization, the main event loop, state management, and rendering coordination.
- `config.py`: Centralized configuration. Holds all grid dimensions, colors, and margins to prevent magic numbers in the codebase, all changeable.
- `node.py`: The data model. Defines the `Node` class, managing individual cell states, coordinates, and rendering logic.
- `algorithms.py`: The brain. Contains the pure algorithmic logic. The Algorithm is implemented as a Python Generator, yielding control back to the main loop to ensure the UI never freezes.
- `ui.py`: The interface. Contains the reusable `Button` class for handling UI rendering and click detection.

## Controls

### Grid Interaction
- **Left Click:** Place or remove a wall (Black).
- **Right Click:** Set the Start node (Green).
- **Middle Click:** Set the End node (Red).

### UI Controls
- **START:** Begins the continuous BFS execution.
- **CLEAR:** Wipes all walls, open/closed sets, and paths, resetting the board while keeping the Start and End nodes.
- **Delay (- / +):** Decreases or increases the delay between algorithm steps.

## How to Run

1. Ensure you have Python 3.x installed on your machine.
2. Install the required dependency:
   ```bash
   pip install pygame
# Interactive Pathfinding Visualizer (BFS)

A modular, interactive Python application built with Pygame that visually demonstrates the Breadth-First Search (BFS) algorithm on a 2D grid. This project was built to explore algorithmic visualization, event-driven UI design, and clean software architecture.

## Features

- **Real-Time Visualization:** Watch the BFS algorithm explore the grid uniformly, expanding outward like a wave until it finds the target.
- **Step-by-Step Execution:** Pause the continuous run and advance the algorithm one step at a time to deeply analyze the decision-making process.
- **Dynamic Speed Control:** Adjust the visualization speed on the fly using discrete UI buttons.
- **Interactive Grid:** Click to place walls, set start points, and define targets. 
- **Path Reconstruction:** Automatically traces and highlights the shortest path once the target is found.
- **Modular Architecture:** Cleanly separated concerns across multiple files for maintainability and scalability.

## Architecture

This project strictly follows the Separation of Concerns principle. Instead of dumping all logic into a single script, the codebase is divided into five distinct modules:

- `main.py`: The conductor. Handles the Pygame initialization, the main event loop, state management, and rendering coordination.
- `config.py`: Centralized configuration. Holds all grid dimensions, colors, and margins to prevent magic numbers in the codebase.
- `node.py`: The data model. Defines the `Node` class, managing individual cell states, coordinates, and rendering logic.
- `algorithms.py`: The brain. Contains the pure algorithmic logic. The BFS is implemented as a Python Generator, yielding control back to the main loop to ensure the UI never freezes.
- `ui.py`: The interface. Contains the reusable `Button` class for handling UI rendering and click detection.

## Controls

### Grid Interaction
- **Left Click:** Place or remove a wall.
- **Right Click:** Set the Start node (Green).
- **Middle Click:** Set the End node (Red).

### UI Controls
- **START:** Begins the continuous BFS execution.
- **CLEAR:** Wipes all walls, open/closed sets, and paths, resetting the board while keeping the Start and End nodes.
- **Speed (- / +):** Decreases or increases the delay between algorithm steps.

## How to Run

1. Ensure you have Python 3.x installed on your machine.
2. Install the required dependency:
   ```bash
   pip install pygame
3. Run the application:
   ```bash
   python main.py
