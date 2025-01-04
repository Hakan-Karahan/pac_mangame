import pygame
import sys
import random
import math

from pygame.time import Clock

pygame.init()

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 650
CELL_SIZE = 40

# Grid dimensions
GRID_WIDTH = 15
GRID_HEIGHT = 15

# game states
PLAYING = 0
GAME_OVER = 1
# Global game state
game_state = PLAYING

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")

# Font for score
font = pygame.font.Font(None, 36)

# Game grid
grid = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Pac-Man
pacman = {
    'x': 1,
    'y': 1,
    'direction': 3,  # 0: right, 1: down, 2: left, 3: up
    'mouth_open': False
}

# Ghosts
ghosts = [
    {'x': 1, 'y': 13, 'color': RED},
    {'x': 13, 'y': 1, 'color': PINK},
    {'x': 13, 'y': 13, 'color': CYAN},
    {'x': 11, 'y': 11, 'color': ORANGE}
]

# Score
score = 0

# Game Loop
clock: Clock = pygame.time.Clock()
running = True

# Movement delays
pacman_move_delay = 150  # milliseconds
ghost_move_delay = 300
mouth_anim_delay = 600
# timing varibles
last_pacman_move_time = 0
last_ghost_move_time = 0
last_mouth_anim_time = 0


def move_pacman():
    global score
    dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][pacman['direction']]
    new_x, new_y = pacman['x'] + dx, pacman['y'] + dy
    if grid[new_y][new_x] != 1:
        pacman['x'], pacman['y'] = new_x, new_y
        if grid[new_y][new_x] == 0:
            grid[new_y][new_x] = 2  # Mark as eaten
            score += 10


def move_ghost(ghost):
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    random.shuffle(directions)
    for dx, dy in directions:
        new_x, new_y = ghost['x'] + dx, ghost['y'] + dy
        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and grid[new_y][new_x] != 1:
            ghost['x'], ghost['y'] = new_x, new_y
            break


def draw_pacman():
    x = pacman['x'] * CELL_SIZE + CELL_SIZE // 2
    y = pacman['y'] * CELL_SIZE + CELL_SIZE // 2 + 50

    # Mouth opening angle varies between 0 (fully closed) and 45 degrees (fully open)
    mouth_opening = 45 if pacman['mouth_open'] else 0

    # Draw Pac-Man as a circle
    pygame.draw.circle(screen, YELLOW, (x, y), CELL_SIZE // 2)

    # Calculate the angles for the mouth based on direction
    if pacman['direction'] == 0:  # Right
        start_angle = 360 - mouth_opening / 2
        end_angle = mouth_opening / 2
    elif pacman['direction'] == 3:  # Down
        start_angle = 90 - mouth_opening / 2
        end_angle = 90 + mouth_opening / 2
    elif pacman['direction'] == 2:  # Left
        start_angle = 180 - mouth_opening / 2
        end_angle = 180 + mouth_opening / 2
    else:  # Up
        start_angle = 270 - mouth_opening / 2
        end_angle = 270 + mouth_opening / 2

    # Draw the mouth using a pie shape (filled arc)
    pygame.draw.arc(screen, BLACK,
                    (x - CELL_SIZE // 2, y - CELL_SIZE // 2, CELL_SIZE, CELL_SIZE),
                    math.radians(start_angle), math.radians(end_angle), CELL_SIZE // 2)

    # Draw a line from the center to create the "slice" effect
    mouth_line_end_x = x + math.cos(math.radians(start_angle)) * CELL_SIZE // 2
    mouth_line_end_y = y - math.sin(math.radians(start_angle)) * CELL_SIZE // 2
    pygame.draw.line(screen, BLACK, (x, y), (mouth_line_end_x, mouth_line_end_y), 2)

    mouth_line_end_x = x + math.cos(math.radians(end_angle)) * CELL_SIZE // 2
    mouth_line_end_y = y - math.sin(math.radians(end_angle)) * CELL_SIZE // 2
    pygame.draw.line(screen, BLACK, (x, y), (mouth_line_end_x, mouth_line_end_y), 2)


def draw_ghost(ghost):
    x = ghost['x'] * CELL_SIZE + CELL_SIZE // 2
    y = ghost['y'] * CELL_SIZE + CELL_SIZE // 2 + 50
    pygame.draw.circle(screen, ghost['color'], (x, y), CELL_SIZE // 2)


def reset_game():
    global pacman, ghosts, score, grid, game_state
    pacman = {
        'x': 1,
        'y': 1,
        'direction': 3,
        'mouth_open': False
    }
    ghosts = [
        {'x': 1, 'y': 13, 'color': RED},
        {'x': 13, 'y': 1, 'color': PINK},
        {'x': 13, 'y': 13, 'color': CYAN},
        {'x': 11, 'y': 11, 'color': ORANGE}
    ]
    score = 0
    grid = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
    game_state = PLAYING


def draw_game_over():
    screen.fill(BLACK)
    game_over_font = pygame.font.Font(None, 64)
    score_font = pygame.font.Font(None, 48)
    restart_font = pygame.font.Font(None, 36)

    game_over_text = game_over_font.render("GAME OVER", True, RED)
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    restart_text = restart_font.render("Press SPACE to restart", True, YELLOW)

    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 2 * SCREEN_HEIGHT // 3))


# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == PLAYING:
                if event.key == pygame.K_UP:
                    pacman['direction'] = 3
                elif event.key == pygame.K_DOWN:
                    pacman['direction'] = 1
                elif event.key == pygame.K_LEFT:
                    pacman['direction'] = 2
                elif event.key == pygame.K_RIGHT:
                    pacman['direction'] = 0
            elif game_state == GAME_OVER:
                if event.key == pygame.K_SPACE:
                    reset_game()

    if game_state == PLAYING:
        # Move Pac-Man only if enough time has passed
        if current_time - last_pacman_move_time > pacman_move_delay:
            move_pacman()
            last_pacman_move_time = current_time
            # Move Ghosts only if enough time has passed
        if current_time - last_ghost_move_time > ghost_move_delay:
            for ghost in ghosts:
                move_ghost(ghost)
            last_ghost_move_time = current_time
        # Animate Pac-Man's mouth
        if current_time - last_mouth_anim_time > mouth_anim_delay:
            pacman['mouth_open'] = not pacman['mouth_open']
            last_mouth_anim_time = current_time

            # clear the screen
        screen.fill(BLACK)
        # Draw the maze and dots
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if grid[y][x] == 1:
                    pygame.draw.rect(screen, BLUE, (x * CELL_SIZE, y * CELL_SIZE + 50, CELL_SIZE, CELL_SIZE))
                elif grid[y][x] == 0:
                    pygame.draw.circle(screen, YELLOW,
                                       (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2 + 50), 3)
        # Draw pacman
        draw_pacman()
        # Draw ghost
        for ghost in ghosts:
            draw_ghost(ghost)
        # displaying the score
        score_text = font.render(f"score:{score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Check for collision with ghosts
        for ghost in ghosts:
            if pacman['x'] == ghost['x'] and pacman['y'] == ghost['y']:
                game_state = GAME_OVER
    elif game_state == GAME_OVER:
        draw_game_over()

    # update the display
    pygame.display.flip()

    # cap the from rate
    clock.tick(60)

pygame.quit()

sys.exit()


