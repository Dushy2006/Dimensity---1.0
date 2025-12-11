import pygame
import sys

pygame.init()

# Screen Setup
WIDTH, HEIGHT = 1425, 825
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen= pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

pygame.display.set_caption("Brick Breaker / Breakout")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Paddle
paddle_width = 120
paddle_height = 15
paddle_x = WIDTH // 2 - paddle_width // 2
paddle_y = HEIGHT - 40
paddle_speed = 8

# Ball
ball_radius = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 4
ball_dy = -4

# Bricks
brick_rows = 5
brick_cols = 8
brick_width = WIDTH // brick_cols
brick_height = 25

def create_bricks():
    bricks_list = []
    for row in range(brick_rows):
        brick_row = []
        for col in range(brick_cols):
            brick_x = col * brick_width
            brick_y = row * brick_height + 50
            brick_row.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))
        bricks_list.append(brick_row)
    return bricks_list

bricks = create_bricks()
score = 0

def reset_game():
    global ball_x, ball_y, ball_dx, ball_dy, paddle_x, score, bricks
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_dx = 4
    ball_dy = -4
    paddle_x = WIDTH // 2 - paddle_width // 2
    bricks = create_bricks()
    score = 0

def draw_bricks():
    colors = [RED, BLUE, GREEN, YELLOW, WHITE]
    for row_index, row in enumerate(bricks):
        for brick in row:
            pygame.draw.rect(screen, colors[row_index], brick)

# Main Game Loop
running = True
while running:
    screen.fill(BLACK)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    # Paddle Control
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
        paddle_x += paddle_speed

    # Draw Paddle
    paddle = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
    pygame.draw.rect(screen, BLUE, paddle)

    # Move Ball
    ball_x += ball_dx
    ball_y += ball_dy
    ball = pygame.Rect(ball_x - ball_radius, ball_y - ball_radius,
                       ball_radius * 2, ball_radius * 2)

    # Draw Ball
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), ball_radius)

    # Ball Collisions with walls
    if ball_x <= ball_radius or ball_x >= WIDTH - ball_radius:
        ball_dx *= -1
    if ball_y <= ball_radius:
        ball_dy *= -1

    # Ball Paddle Collision
    if ball.colliderect(paddle):
        ball_dy *= -1

    # Brick Collision
    for row in bricks:
        for brick in row[:]:
            if ball.colliderect(brick):
                ball_dy *= -1
                row.remove(brick)
                score += 1
                break

    # Draw Bricks
    draw_bricks()

    # GAME OVER
    if ball_y > HEIGHT:
        text = font.render("GAME OVER! Press R to Restart", True, RED)
        screen.blit(text, (WIDTH//2 - 160, HEIGHT//2))
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    reset_game()
                    waiting = False
                

    # WIN CONDITION
    if score == brick_rows * brick_cols:
        text = font.render("YOU WIN! Press R to Restart", True, GREEN)
        screen.blit(text, (WIDTH//2 - 150, HEIGHT//2))
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    reset_game()
                    waiting = False
                

    # Score HUD
    score_text = font.render(f"Score : {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(60)
