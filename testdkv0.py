import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Game settings
FPS = 60
PLAYER_SPEED = 5
BARREL_SPEED = 4

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Donkey Kong Clone")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Player properties
player = pygame.Rect(50, SCREEN_HEIGHT - 40, 30, 30)

# Platforms
platforms = [
    pygame.Rect(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20),
    pygame.Rect(50, 300, 500, 20),
    pygame.Rect(0, 200, 400, 20),
    pygame.Rect(200, 100, 400, 20)
]

# Ladders
ladders = [
    pygame.Rect(100, 300, 20, 100),
    pygame.Rect(350, 200, 20, 100)
]

# Barrels
barrels = []
BARREL_INTERVAL = 2000  # Time between barrel spawns (ms)
last_barrel_time = pygame.time.get_ticks()

# Goal
goal = pygame.Rect(550, 80, 30, 20)

# Game loop flag
running = True

# Gravity
gravity = 1
player_velocity_y = 0
on_ground = False

while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player.x += PLAYER_SPEED

    # Check for climbing
    climbing = False
    for ladder in ladders:
        if player.colliderect(ladder):
            climbing = True
            if keys[pygame.K_UP]:
                player.y -= PLAYER_SPEED
            if keys[pygame.K_DOWN]:
                player.y += PLAYER_SPEED

    # Apply gravity if not climbing
    if not climbing:
        player_velocity_y += gravity
    else:
        player_velocity_y = 0

    # Move player vertically
    player.y += player_velocity_y

    # Check collision with platforms
    on_ground = False
    for platform in platforms:
        if player.colliderect(platform) and player_velocity_y > 0:
            player.bottom = platform.top
            player_velocity_y = 0
            on_ground = True

    # Keep player within screen bounds
    player.x = max(0, min(SCREEN_WIDTH - player.width, player.x))
    player.y = max(0, min(SCREEN_HEIGHT - player.height, player.y))

    # Spawn barrels
    current_time = pygame.time.get_ticks()
    if current_time - last_barrel_time > BARREL_INTERVAL:
        barrels.append(pygame.Rect(550, 100, 20, 20))
        last_barrel_time = current_time

    # Move barrels
    for barrel in barrels[:]:
        barrel.x -= BARREL_SPEED
        if barrel.x < 0:
            barrels.remove(barrel)

    # Check for collisions with barrels
    for barrel in barrels:
        if player.colliderect(barrel):
            print("Game Over!")
            running = False

    # Check for reaching the goal
    if player.colliderect(goal):
        print("You Win!")
        running = False

    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, BLUE, platform)

    # Draw ladders
    for ladder in ladders:
        pygame.draw.rect(screen, GREEN, ladder)

    # Draw barrels
    for barrel in barrels:
        pygame.draw.rect(screen, RED, barrel)

    # Draw player
    pygame.draw.rect(screen, WHITE, player)

    # Draw goal
    pygame.draw.rect(screen, GREEN, goal)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
