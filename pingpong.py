import pygame
import sys
import random

# Pygame setup
pygame.init()
size = surface_width, height = (500, 600)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption("Ping Pong Game")

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 50)

# Game Variables
rect_width, rect_height = 100, 30
rect_speed = 8
ball_speed = [random.choice([-3, 3]), 3]
score_top = 0
score_bottom = 0
max_score = 11
smash_speed_increment = 4

# Paddle positions
top_rect_x = (surface_width - rect_width) // 2
bottom_rect_x = (surface_width - rect_width) // 2
rect_y_top = 10
rect_y_bottom = height - rect_height - 10

# Ball setup
ball = pygame.Surface((15, 15), pygame.SRCALPHA)
pygame.draw.circle(ball, (255, 255, 255), (7, 7), 7)
ballrect = ball.get_rect(center=(surface_width // 2, height // 2))

# Game state variables
running = False
paused = False
top_moving_left = top_moving_right = False
bottom_moving_left = bottom_moving_right = False
smash_active = False

# Player names
player_names = []

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (150, 150, 150)

# Functions
def reset_ball():
    ballrect.center = (surface_width // 2, height // 2)
    ball_speed[0] = random.choice([-3, 3])
    ball_speed[1] = random.choice([-3, 3])
    pygame.time.wait(1000)

def handle_collision():
    """Handle ball collisions with paddles to avoid absorbing."""
    global ball_speed

    # Top paddle
    if ballrect.colliderect(pygame.Rect(top_rect_x, rect_y_top, rect_width, rect_height)):
        ball_speed[1] = abs(ball_speed[1])  # Ensure the ball goes downward
        ball_speed[0] += random.choice([-1, 1])  # Add horizontal variation
        if smash_active:
            ball_speed[1] += smash_speed_increment

    # Bottom paddle
    if ballrect.colliderect(pygame.Rect(bottom_rect_x, rect_y_bottom, rect_width, rect_height)):
        ball_speed[1] = -abs(ball_speed[1])  # Ensure the ball goes upward
        ball_speed[0] += random.choice([-1, 1])
        if smash_active:
            ball_speed[1] -= smash_speed_increment

def draw_text_centered(text, font, color, y):
    """Draw text centered on the screen."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (surface_width // 2 - text_surface.get_width() // 2, y))

# Menu screen
def get_player_names():
    """Prompt for player names one by one."""
    player_names = []
    prompts = ["Player 1 (Top) Name:", "Player 2 (Bottom) Name:"]
    current_input = ""
    current_prompt = 0

    while len(player_names) < 2:
        screen.fill(BLACK)

        draw_text_centered("Ping Pong Game", large_font, WHITE, 50)
        draw_text_centered(prompts[current_prompt], font, WHITE, height // 2 - 50)
        draw_text_centered(current_input, font, RED if current_prompt == 0 else BLUE, height // 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    current_input = current_input[:-1]
                elif event.key == pygame.K_RETURN:
                    player_names.append(current_input)
                    current_input = ""
                    current_prompt += 1
                else:
                    current_input += event.unicode

        pygame.display.flip()
        clock.tick(30)

    return player_names

def show_start_button():
    """Display a start button and wait for it to be clicked."""
    button_rect = pygame.Rect(surface_width // 2 - 75, height // 2 + 50, 150, 50)

    while True:
        screen.fill(BLACK)

        draw_text_centered("Ping Pong Game", large_font, WHITE, 50)
        draw_text_centered(f"Player 1: {player_names[0]}", font, RED, 150)
        draw_text_centered(f"Player 2: {player_names[1]}", font, BLUE, 200)

        # Draw the button
        pygame.draw.rect(screen, GREEN, button_rect)
        draw_text_centered("Start", font, BLACK, button_rect.y + 10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return  # Start the game

        pygame.display.flip()
        clock.tick(30)

# Pause screen
def show_pause():
    draw_text_centered("Game Paused", large_font, WHITE, height // 2 - 50)
    draw_text_centered("Press P to Resume", font, WHITE, height // 2 + 20)
    pygame.display.flip()

# Main Game Loop
player_names = get_player_names()
show_start_button()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                top_moving_left = True
            elif event.key == pygame.K_RIGHT:
                top_moving_right = True
            if event.key == pygame.K_a:
                bottom_moving_left = True
            elif event.key == pygame.K_d:
                bottom_moving_right = True
            if event.key == pygame.K_SPACE:
                smash_active = True
            if event.key == pygame.K_p:
                paused = not paused
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                top_moving_left = False
            elif event.key == pygame.K_RIGHT:
                top_moving_right = False
            if event.key == pygame.K_a:
                bottom_moving_left = False
            elif event.key == pygame.K_d:
                bottom_moving_right = False
            if event.key == pygame.K_SPACE:
                smash_active = False

    if paused:
        show_pause()
        continue

    # Update paddle positions
    if top_moving_left and top_rect_x > 0:
        top_rect_x -= rect_speed
    if top_moving_right and top_rect_x < surface_width - rect_width:
        top_rect_x += rect_speed
    if bottom_moving_left and bottom_rect_x > 0:
        bottom_rect_x -= rect_speed
    if bottom_moving_right and bottom_rect_x < surface_width - rect_width:
        bottom_rect_x += rect_speed

    # Move the ball
    ballrect = ballrect.move(ball_speed)

    # Handle collisions
    handle_collision()

    # Ball collision with walls
    if ballrect.left <= 0 or ballrect.right >= surface_width:
        ball_speed[0] = -ball_speed[0]

    # Check for scoring
    if ballrect.top <= 0:
        score_bottom += 1
        reset_ball()
    elif ballrect.bottom >= height:
        score_top += 1
        reset_ball()

    # Check win condition
    if score_top == max_score or score_bottom == max_score:
        running = False

    # Draw the game
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, (0, height // 2), (surface_width, height // 2), 2)
    pygame.draw.rect(screen, RED, (top_rect_x, rect_y_top, rect_width, rect_height))
    pygame.draw.rect(screen, BLUE, (bottom_rect_x, rect_y_bottom, rect_width, rect_height))
    screen.blit(ball, ballrect)

    # Draw scores and names
    top_score_text = font.render(f"{player_names[0]}: {score_top}", True, WHITE)
    bottom_score_text = font.render(f"{player_names[1]}: {score_bottom}", True, WHITE)
    screen.blit(top_score_text, (20, 20))
    screen.blit(bottom_score_text, (20, height - 40))

    pygame.display.flip()
    clock.tick(60)

# End game screen
screen.fill(BLACK)
winner_text = f"{player_names[0]} Wins!" if score_top == max_score else f"{player_names[1]} Wins!"
draw_text_centered(winner_text, large_font, WHITE, height // 2)
pygame.display.flip()
pygame.time.wait(3000)
pygame.quit()
