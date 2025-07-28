# Pac-Man with AI Ghosts (Python + Pygame)

A modern twist on the classic Pac-Man game built using Python and Pygame. This version includes AI-controlled ghosts powered by the A* pathfinding algorithm, a dynamic and symmetric maze generator, and progressively activating ghosts to increase difficulty over time.

## Features

- Grid-based Pac-Man movement
- Ghost AI with A* Pathfinding
- Procedurally generated symmetrical walls
- Pellet collection and scoring system
- Game Over screen with Retry option
- Dynamic ghost activation with increasing challenge

## Technologies Used

- Python 3
- Pygame
- A* Pathfinding (via `heapq`)
- Object-Oriented Programming (OOP)

## Game Mechanics

- **Pac-Man** can move in four directions using WASD keys.
- **Ghosts** spawn after timed delays and chase Pac-Man using the A* algorithm.
- **Pellets** are placed in all open spaces; collecting them increases the score.
- **Walls** are procedurally generated and symmetrical for fair gameplay.

## AI Logic

- Each ghost calculates the shortest path to Pac-Man using the A* pathfinding algorithm.
- Ghosts activate one after another with increasing delay, adding progressive difficulty.


## How to Run

1. Ensure Python 3 and Pygame are installed:
   ```bash
   pip install pygame
2. Replace the image paths in the script with valid paths on your system for:
   pacman.jpeg
   red.jpeg, pink.jpeg, blue.jpeg, orange.jpeg

3. Run the script:
   ```bash
   python pacman_game.py

## File Structure
pacman_game.py – Main game logic
assets/ – Image files for characters (not included; add manually)
