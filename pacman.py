import pygame  # pygame library - create games with graphics, sound, and input handling
import sys  # to handle system-level functions like quitting the game
from pygame.locals import *  # imports all constants in pygame.locals, making event handling more readable
import random  # imports random to generate random numbers, used for ghost behavior and wall generation
import heapq  # imports heapq for implementing a priority queue, crucial for the A* pathfinding algorithm

#initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 640  # Screen width in pixels
SCREEN_HEIGHT = 480  # Screen height in pixels
GRID_SIZE = 20  # Defines each cell’s size for grid layout
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE  # Horizontal grid cells based on screen width
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE  # Vertical grid cells based on screen height
PACMAN_SPEED = 10  # Speed of Pac-Man; lower numbers make Pac-Man slower
GHOST_SPEED = 30  # Speed of ghosts; lower numbers mean faster movement
INITIAL_GHOST_DELAY = 5000  # Delay in milliseconds before the first ghost activates (5 seconds)
ADDITIONAL_GHOST_DELAY = 7000  # Extra delay for each new ghost activation (7 seconds after each ghost)
MAX_GHOSTS = 4  # Maximum number of ghosts that can be active simultaneously

# Directions represented as (x, y) tuples for ease in grid-based movement
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
STOP = (0, 0)  # No movement

# Colors (RGB format)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (100, 149, 237)  # Cornflower Blue
ORANGE = (144, 238, 144)  # Pellet color

# Initialize display settings
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Initializes screen with specified dimensions
pygame.display.set_caption("Pac-Man")  # title of the window to "Pac-Man"
clock = pygame.time.Clock()  # Manages frame rate and game timing
font = pygame.font.Font(None, 36)  # Font for displaying text

# Load images for Pac-Man and each ghost, adjusting the images to fit the grid
pacman_image = pygame.image.load(r'C:\Users\MITALEEE\Downloads\pacman.jpeg').convert_alpha()
ghost_images = [
    pygame.image.load(r'C:\Users\MITALEEE\Downloads\red.jpeg').convert_alpha(),
    pygame.image.load(r'C:\Users\MITALEEE\Downloads\pink.jpeg').convert_alpha(),
    pygame.image.load(r'C:\Users\MITALEEE\Downloads\blue.jpeg').convert_alpha(),
    pygame.image.load(r'C:\Users\MITALEEE\Downloads\orange.jpeg').convert_alpha()
]

# Rescale the images to fit within a grid cell
pacman_image = pygame.transform.scale(pacman_image, (GRID_SIZE, GRID_SIZE))  
ghost_images = [pygame.transform.scale(img, (GRID_SIZE, GRID_SIZE)) for img in ghost_images]  

# Define game object classes
class GameObject:
    """Base class for all game objects, providing basic position handling."""
    def __init__(self, x, y):
        self.x = x  # X-coordinate in the grid
        self.y = y  # Y-coordinate in the grid

class Pacman(GameObject):
    """Class for Pac-Man, inherits from GameObject and handles movement and scoring."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.direction = STOP  # Pac-Man starts without a direction
        self.speed_counter = 0  # Counter to control movement frequency based on PACMAN_SPEED
        self.score = 0  # Initialize score

    def move(self, walls, pellets):
        """Moves Pac-Man and checks for wall collisions or pellet consumption."""
        if self.speed_counter >= PACMAN_SPEED:  # Move only when counter reaches PACMAN_SPEED
            self.speed_counter = 0  # Reset counter to wait for next move
            # Calculate new position and wrap around screen edges
            new_x = (self.x + self.direction[0]) % GRID_WIDTH
            new_y = (self.y + self.direction[1]) % GRID_HEIGHT
            if (new_x, new_y) not in walls:  # Check if next cell is a wall
                if (new_x, new_y) in pellets:  # Check if next cell contains a pellet
                    pellets.remove((new_x, new_y))  # Remove pellet from grid
                    self.score += 10  # Increase score
                self.x, self.y = new_x, new_y  # Update Pac-Man’s position
        else:
            self.speed_counter += 1  # Increment counter if not moving

class Ghost(GameObject):
    """Class for Ghosts, with A* pathfinding to chase Pac-Man."""
    def __init__(self, x, y, image):
        super().__init__(x, y)
        self.image = image  # Assign ghost’s image
        self.speed_counter = 0  # Counter to control ghost speed
        self.active = False  # Ghosts begin inactive

    def move(self, pacman, walls):
        """Moves ghost towards Pac-Man if active and counter reaches GHOST_SPEED."""
        if self.active and self.speed_counter >= GHOST_SPEED:
            self.speed_counter = 0  # Reset counter after movement
            path = self.find_path(pacman, walls)  # Calculate path to Pac-Man
            if path:
                self.x, self.y = path[1]  # Move to next cell in path
        else:
            self.speed_counter += 1  # Increment counter if not moving

    def find_path(self, pacman, walls):
        """Uses A* algorithm to find the shortest path to Pac-Man."""
        open_list = [(0, (self.x, self.y))]  # Priority queue, starting with ghost's position
        came_from = {}  # Dictionary for reconstructing path
        g_score = {(self.x, self.y): 0}  # Cost from start to each cell

        while open_list:
            _, current = heapq.heappop(open_list)  # Pop cell with lowest f-score

            if current == (pacman.x, pacman.y):  # If path to Pac-Man found
                path = [current]
                while current in came_from:  # Trace path back to start
                    current = came_from[current]
                    path.append(current)
                path.reverse()  # Reverse path to get correct order
                return path

            # Check each neighbor cell (up, down, left, right)
            for neighbor in [(current[0] + 1, current[1]), (current[0] - 1, current[1]),
                             (current[0], current[1] + 1), (current[0], current[1] - 1)]:
                if neighbor not in walls and 0 <= neighbor[0] < GRID_WIDTH and 0 <= neighbor[1] < GRID_HEIGHT:
                    tentative_g_score = g_score[current] + 1  # Increment g-score for movement
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:  # Check if new path is shorter
                        came_from[neighbor] = current  # Track path
                        g_score[neighbor] = tentative_g_score
                        f_score = tentative_g_score + self.manhattan_distance(neighbor, (pacman.x, pacman.y))
                        heapq.heappush(open_list, (f_score, neighbor))  # Add neighbor to open list

        return []  # Return empty if no path found

    def manhattan_distance(self, point1, point2):
        """Heuristic function for A*, calculates Manhattan distance."""
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

# Maze generation and wall handling functions

def generate_symmetric_walls():
    """Generates symmetric maze layout with random walls and boundaries."""
    walls = set()
    wall_density = 0.15  # Probability of each cell being a wall (15% chance)

    for y in range(GRID_HEIGHT // 2):  # Populate half the grid and mirror
        for x in range(GRID_WIDTH):
            if random.random() < wall_density and (x, y) != (1, 1):  # Exclude Pac-Man start point
                walls.add((x, y))
                walls.add((GRID_WIDTH - x - 1, GRID_HEIGHT - y - 1))  # Mirror wall position

    # Create boundary walls around the grid edges
    for x in range(GRID_WIDTH):
        walls.add((x, 0))
        walls.add((x, GRID_HEIGHT - 1))
    for y in range(GRID_HEIGHT):
        walls.add((0, y))
        walls.add((GRID_WIDTH - 1, y))

    return walls

def initialize_pellets(walls):
    """Places pellets in all grid cells not occupied by walls."""
    return {(x, y) for y in range(GRID_HEIGHT) for x in range(GRID_WIDTH) if (x, y) not in walls}

def initialize_game():
    """Sets up initial game state with walls, pellets, Pac-Man, and ghosts."""
    global pacman, ghosts, pellets, walls
    walls = generate_symmetric_walls()  # Generate maze walls
    pellets = initialize_pellets(walls)  # Place pellets
    pacman = Pacman(1, 1)  # Place Pac-Man at initial position
    # Set initial positions for ghosts
    ghost_spawn_positions = [(GRID_WIDTH - 2, y) for y in range(1, 5)]
    ghosts = [Ghost(x, y, ghost_images[i]) for i, (x, y) in enumerate(ghost_spawn_positions[:MAX_GHOSTS])]

# Game over screen with retry button

def game_over_screen(score):
    """Displays 'Game Over' screen with retry option."""
    game_over = True
    retry_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50, 100, 50)  # Defines retry button
    while game_over:
        screen.fill(BLACK)  # Clear screen with black
        game_over_text = font.render("Game Over!", True, WHITE)
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 100))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
        draw_button("Retry", retry_button, BLUE)

        pygame.display.update()  # Refresh screen

        # Handle retry button events
        for event in pygame.event.get():
            if event.type == QUIT:  # If quit event, close game
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if retry_button.collidepoint(event.pos):  # Restart game on retry
                    game_over = False
                    initialize_game()  # Reset game state
                    main()  # Restart main game loop

def draw_button(text, rect, color, text_color=WHITE):
    """Draws a button with specified text and color."""
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)  # Center text
    screen.blit(text_surface, text_rect)

# Main game loop

def main():
    """Main loop for running the game and handling events."""
    running = True
    game_start_time = pygame.time.get_ticks()  # Record game start time
    last_ghost_time = game_start_time  # Last ghost addition time

    while running:
        # Handle events for input and game controls
        for event in pygame.event.get():
            if event.type == QUIT:  # Exit game if quit event
                running = False
            elif event.type == KEYDOWN:
                handle_user_input()

        current_time = pygame.time.get_ticks()  # Current game time in milliseconds
        pacman.move(walls, pellets)  # Move Pac-Man and check for pellets

        # Activate and move ghosts based on delay times
        for i, ghost in enumerate(ghosts):
            if not ghost.active and current_time - game_start_time > INITIAL_GHOST_DELAY + i * ADDITIONAL_GHOST_DELAY:
                ghost.active = True  # Activate ghost
            if ghost.active:
                ghost.move(pacman, walls)  # Move active ghosts

        if check_ghost_collision():  # Check if Pac-Man and ghost collide
            game_over_screen(pacman.score)
            break

        draw_game()  # Update screen with current game state
        clock.tick(60)  # Frame rate

    pygame.quit()
    sys.exit()

def handle_user_input():
    """Handles user keyboard input for Pac-Man movement."""
    keys = pygame.key.get_pressed()
    if keys[K_a]:
        pacman.direction = LEFT
    elif keys[K_d]:
        pacman.direction = RIGHT
    elif keys[K_w]:
        pacman.direction = UP
    elif keys[K_s]:
        pacman.direction = DOWN

def draw_game():
    """Draws walls, pellets, Pac-Man, ghosts, and score on the screen."""
    screen.fill(BLACK)
    for wall in walls:
        pygame.draw.rect(screen, BLUE, (wall[0] * GRID_SIZE, wall[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))  # Draw walls
    for pellet in pellets:
        pygame.draw.circle(screen, ORANGE, (pellet[0] * GRID_SIZE + GRID_SIZE // 2, pellet[1] * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 5.5)  # Draw pellets
    screen.blit(pacman_image, (pacman.x * GRID_SIZE, pacman.y * GRID_SIZE))  # Draw Pac-Man
    for ghost in ghosts:
        screen.blit(ghost.image, (ghost.x * GRID_SIZE, ghost.y * GRID_SIZE))  # Draw ghosts
    score_text = font.render(f"Score: {pacman.score}", True, WHITE)
    screen.blit(score_text, (10, 10))  # Display score
    pygame.display.update()

def check_ghost_collision():
    """Checks if Pac-Man collides with any ghost."""
    return any(ghost.x == pacman.x and ghost.y == pacman.y for ghost in ghosts)  # Check for collisions

if __name__ == "__main__":
    initialize_game()  # Initialize all game elements
    main()  # Start main game loop








