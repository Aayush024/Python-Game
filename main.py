
import pygame  # type: ignore
from random import randrange as rnd

# Screen settings
WIDTH, HEIGHT = 1200, 800
FPS = 60

# Paddle settings
paddle_w, paddle_h = 330, 35
paddle_speed = 15
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)

# Ball settings
ball_radius = 20
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1

# Blocks settings
block_cols, block_rows = 10, 4
block_width, block_height = 100, 50
block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, block_width, block_height)
              for i in range(block_cols) for j in range(block_rows)]
color_list = [(rnd(50, 256), rnd(50, 256), rnd(50, 256))
              for _ in range(block_cols * block_rows)]

# Initialize pygame
pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Background image
img = pygame.image.load('1.jpg').convert()

# Score settings
score = 0
font = pygame.font.Font(None, 36)

# Pause flag
paused = False


def draw_text(surface, text, x, y, color=(255, 255, 255)):
    """Helper function to draw text on the screen."""
    render = font.render(text, True, color)
    surface.blit(render, (x, y))


def detect_collision(dx, dy, ball, rect):
    """Detect collision between the ball and another rectangle."""
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    else:
        dx = -dx
    return dx, dy


def reset_ball():
    """Reset ball position and direction."""
    global ball, dx, dy
    ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
    dx, dy = 1, -1


while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused

    if paused:
        draw_text(sc, "Paused - Press 'P' to Resume", WIDTH // 2 - 200, HEIGHT // 2, (255, 255, 255))
        pygame.display.flip()
        clock.tick(FPS)
        continue

    # Draw background
    sc.blit(img, (0, 0))

    # Draw blocks
    [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]

    # Draw paddle and ball
    pygame.draw.rect(sc, pygame.Color('darkorange'), paddle)
    pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)

    # Draw score
    draw_text(sc, f"Score: {score}", 10, 10)

    # Ball movement
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy

    # Ball collision with walls
    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        dx = -dx
    if ball.centery < ball_radius:
        dy = -dy

    # Ball collision with paddle
    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle)

    # Ball collision with blocks
    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)
        # Special effect
        hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
        pygame.draw.rect(sc, hit_color, hit_rect)
        score += 10
        FPS += 1  # Increase speed slightly as the game progresses

    # Game over
    if ball.bottom > HEIGHT:
        draw_text(sc, "GAME OVER! Press any key to restart", WIDTH // 2 - 200, HEIGHT // 2, (255, 0, 0))
        pygame.display.flip()
        pygame.time.wait(2000)
        reset_ball()
        block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, block_width, block_height)
                      for i in range(block_cols) for j in range(block_rows)]
        color_list = [(rnd(50, 256), rnd(50, 256), rnd(50, 256))
                      for _ in range(block_cols * block_rows)]
        score = 0
        FPS = 60

    # Win condition
    if not block_list:
        draw_text(sc, "YOU WIN!!! Press any key to restart", WIDTH // 2 - 200, HEIGHT // 2, (0, 255, 0))
        pygame.display.flip()
        pygame.time.wait(2000)
        reset_ball()
        block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, block_width, block_height)
                      for i in range(block_cols) for j in range(block_rows)]
        color_list = [(rnd(50, 256), rnd(50, 256), rnd(50, 256))
                      for _ in range(block_cols * block_rows)]
        score = 0
        FPS = 60

    # Paddle control
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if key[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += paddle_speed

    # Update display
    pygame.display.flip()
    clock.tick(FPS)
