import pygame
import random

# Initialize
pygame.init()

# Screen
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Forest Glow Pong")

clock = pygame.time.Clock()

# Colors
DARK_GREEN = (10, 40, 10)

# Tree Colors
TREE_GREEN = (34, 90, 34)
TREE_LIGHT = (60, 140, 60)

# Paddle Glow Color
PADDLE_GLOW = (0, 255, 180)

WHITE = (255, 255, 255)

# Fonts
title_font = pygame.font.SysFont("Arial", 60)
menu_font = pygame.font.SysFont("Arial", 35)
score_font = pygame.font.SysFont("Arial", 50)

# Paddle
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 120
PADDLE_SPEED = 7

# Ball
BALL_SIZE = 20
BALL_SPEED = 6


# Glowing Paddle
def draw_glowing_paddle(surface, rect, color):
    for i in range(15, 0, -3):
        glow_surface = pygame.Surface(
            (rect.width + i * 2, rect.height + i * 2),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            glow_surface,
            (*color, 20),
            glow_surface.get_rect(),
            border_radius=12
        )

        surface.blit(glow_surface, (rect.x - i, rect.y - i))

    pygame.draw.rect(surface, color, rect, border_radius=8)


# Forest Background
def draw_forest():
    screen.fill(DARK_GREEN)

    for x in range(0, WIDTH, 100):

        # Tree trunk
        pygame.draw.rect(
            screen,
            (70, 40, 20),
            (x + 40, HEIGHT - 180, 20, 180)
        )

        # Tree leaves
        pygame.draw.circle(screen, TREE_GREEN, (x + 50, HEIGHT - 200), 50)
        pygame.draw.circle(screen, TREE_LIGHT, (x + 20, HEIGHT - 170), 40)
        pygame.draw.circle(screen, TREE_LIGHT, (x + 80, HEIGHT - 170), 40)


# Main Menu
def main_menu():
    while True:
        draw_forest()

        title = title_font.render("FOREST GLOW PONG", True, PADDLE_GLOW)
        one_player = menu_font.render("1 - Single Player", True, WHITE)
        two_player = menu_font.render("2 - Two Players", True, WHITE)
        quit_text = menu_font.render("ESC - Quit", True, WHITE)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))
        screen.blit(one_player, (WIDTH // 2 - one_player.get_width() // 2, 260))
        screen.blit(two_player, (WIDTH // 2 - two_player.get_width() // 2, 320))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 380))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1

                if event.key == pygame.K_2:
                    return 2

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return None


# Game
def game(mode):
    left_paddle = pygame.Rect(40, HEIGHT // 2 - 60, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(WIDTH - 55, HEIGHT // 2 - 60, PADDLE_WIDTH, PADDLE_HEIGHT)

    ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)

    ball_dx = random.choice((BALL_SPEED, -BALL_SPEED))
    ball_dy = random.choice((BALL_SPEED, -BALL_SPEED))

    left_score = 0
    right_score = 0

    running = True

    while running:
        clock.tick(60)

        draw_forest()

        pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        keys = pygame.key.get_pressed()

        # Left Paddle
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= PADDLE_SPEED

        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += PADDLE_SPEED

        # Right Paddle
        if mode == 2:
            if keys[pygame.K_UP] and right_paddle.top > 0:
                right_paddle.y -= PADDLE_SPEED

            if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
                right_paddle.y += PADDLE_SPEED
        else:
            # AI
            if right_paddle.centery < ball.centery:
                right_paddle.y += 5

            if right_paddle.centery > ball.centery:
                right_paddle.y -= 5

        # Ball Movement
        ball.x += ball_dx
        ball.y += ball_dy

        # Wall Collision
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_dy *= -1

        # Paddle Collision
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            ball_dx *= -1

        # Score
        if ball.left <= 0:
            right_score += 1
            ball.center = (WIDTH // 2, HEIGHT // 2)
            ball_dx *= -1

        if ball.right >= WIDTH:
            left_score += 1
            ball.center = (WIDTH // 2, HEIGHT // 2)
            ball_dx *= -1

        # Draw Glowing Paddles
        draw_glowing_paddle(screen, left_paddle, PADDLE_GLOW)
        draw_glowing_paddle(screen, right_paddle, PADDLE_GLOW)

        # Ball (No Glow)
        pygame.draw.ellipse(screen, WHITE, ball)

        # Scores
        left_text = score_font.render(str(left_score), True, WHITE)
        right_text = score_font.render(str(right_score), True, WHITE)

        screen.blit(left_text, (WIDTH // 4, 30))
        screen.blit(right_text, (WIDTH * 3 // 4, 30))

        pygame.display.update()


# Main Loop
while True:
    selected_mode = main_menu()

    if selected_mode is None:
        break

    game(selected_mode)

pygame.quit()