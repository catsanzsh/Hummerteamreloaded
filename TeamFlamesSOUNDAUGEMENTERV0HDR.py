import pygame
from array import array
import math

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Set screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("NX2 Augmenter Musicdisk - Team Hummer Tribute")

# Colors
black = (0, 0, 0)
green = (0, 128, 0)
light_green = (0, 255, 0)
retro_yellow = (255, 255, 0)

# Fonts
font_title = pygame.font.Font(None, 48)
font_text = pygame.font.Font(None, 24)
font_sound = pygame.font.Font(None, 36)

# Text elements
title = font_title.render("NX2 Augmenter Musicdisk", True, retro_yellow)
sub_title = font_text.render("Tribute to Team Hummer", True, light_green)
instructions = font_text.render("D-PAD LEFT/RIGHT: Browse Sounds | SPACE: Play Sound", True, green)

# Positions
title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 40))
sub_title_rect = sub_title.get_rect(center=(SCREEN_WIDTH // 2, 80))
instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, 520))

# Define a function to generate beep sounds with varying frequencies
def generate_beep_sound(frequency=440, duration=0.1):
    sample_rate = pygame.mixer.get_init()[0]
    max_amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    samples = int(sample_rate * duration)
    wave = [int(max_amplitude * math.sin(2 * math.pi * frequency * i / sample_rate)) for i in range(samples)]
    sound = pygame.mixer.Sound(buffer=array('h', wave))
    sound.set_volume(0.2)
    return sound

# Create a list of sound tuples (name, sound object)
sounds = [
    ("SND_1 - A4", generate_beep_sound(440, 0.5)),
    ("SND_2 - C5", generate_beep_sound(523.25, 0.5)),
    ("SND_3 - D5", generate_beep_sound(587.33, 0.5)),
    ("SND_4 - E5", generate_beep_sound(659.25, 0.5)),
    ("NES_SQ1", generate_beep_sound(440, 0.2)),
    ("NES_SQ2", generate_beep_sound(523.25, 0.2)),
    ("FAM_CLONE_SQ1", generate_beep_sound(660, 0.2)),
    ("GB_SQ1", generate_beep_sound(880, 0.2)),
]
current_sound_index = 0  # Index of the currently selected sound

# Function for rendering retro visualizer
def draw_visualizer(surface, sound_name, x, y, width, height):
    pygame.draw.rect(surface, light_green, (x, y, width, height), 2)
    text = font_text.render(sound_name, True, retro_yellow)
    text_rect = text.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text, text_rect)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Play the current sound
                print(f"Playing sound: {sounds[current_sound_index][0]}")  # Debug statement
                sounds[current_sound_index][1].play()
            elif event.key == pygame.K_RIGHT:
                # Cycle to the next sound
                current_sound_index = (current_sound_index + 1) % len(sounds)
                print(f"Selected sound: {sounds[current_sound_index][0]}")  # Debug statement
            elif event.key == pygame.K_LEFT:
                # Cycle to the previous sound
                current_sound_index = (current_sound_index - 1) % len(sounds)
                print(f"Selected sound: {sounds[current_sound_index][0]}")  # Debug statement

    # Fill background
    screen.fill(black)

    # Draw text elements
    screen.blit(title, title_rect)
    screen.blit(sub_title, sub_title_rect)
    screen.blit(instructions, instructions_rect)

    # Draw visualizer for the current sound
    draw_visualizer(screen, sounds[current_sound_index][0], 200, 250, 400, 100)

    pygame.display.flip()
    pygame.time.wait(30)

pygame.quit()
