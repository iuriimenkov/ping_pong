
import pygame
import random
import time

# Инициализация Pygame
pygame.init()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
#фон
background = pygame.transform.scale(pygame.image.load('backgroung.png'),(1000, 800))

# Настройки окна
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-понг")


# Настройки ракетки
paddle_width = 10
paddle_height = 100
player_paddle_x = 50
opponent_paddle_x = WIDTH - 50 - paddle_width
player_paddle_y = HEIGHT // 2 - paddle_height // 2
opponent_paddle_y = HEIGHT // 2 - paddle_height // 2
paddle_speed = 7

# Настройки мяча
ball_width = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 7 * random.choice((-1, 1))
ball_dy = 7 * random.choice((-1, 1))

# Счет
player_score = 0
opponent_score = 0

# Загрузка звуков
hit_sound = pygame.mixer.Sound('hit_sound.wav')
score_sound = pygame.mixer.Sound('score_sound.wav')


# Главный игровой цикл
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_paddle_y > 0:
        player_paddle_y -= paddle_speed
    if keys[pygame.K_DOWN] and player_paddle_y < HEIGHT - paddle_height:
        player_paddle_y += paddle_speed

    # Движение ракетки противника (с заглушкой для простоты)
    if opponent_paddle_y < ball_y and opponent_paddle_y < HEIGHT - paddle_height:
        opponent_paddle_y += paddle_speed
    elif opponent_paddle_y > 0:
        opponent_paddle_y -= paddle_speed

    # Обновление положения мяча
    ball_x += ball_dx
    ball_y += ball_dy

    # Проверка столкновений с верхней и нижней стенкой
    if ball_y > HEIGHT - ball_width or ball_y < 0:
        ball_dy *= -1

    # Проверка столкновений с ракетками
    if (ball_x < player_paddle_x + paddle_width and
            player_paddle_y < ball_y < player_paddle_y + paddle_height):
        ball_dx *= -1
        hit_sound.play()
    elif (ball_x > opponent_paddle_x and
            opponent_paddle_y < ball_y < opponent_paddle_y + paddle_height):
        ball_dx *= -1
        hit_sound.play()

    # Проверка забития гола
    if ball_x > WIDTH:
        player_score += 1
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_dx = 7 * random.choice((-1, 1))
        ball_dy = 7 * random.choice((-1, 1))
        score_sound.play()
    elif ball_x < 0:
        opponent_score += 1
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_dx = 7 * random.choice((-1, 1))
        ball_dy = 7 * random.choice((-1, 1))
        score_sound.play()

    # Проверка завершения игры
    if player_score >= 10:
        print("Победа!")
        run = False
    elif opponent_score >= 10:
        print("Поражение!")
        run = False

    # Отрисовка экрана
    win.blit(background,(-100,-100))
    pygame.draw.rect(win, WHITE, (player_paddle_x, player_paddle_y, paddle_width, paddle_height))
    pygame.draw.rect(win, WHITE, (opponent_paddle_x, opponent_paddle_y, paddle_width, paddle_height))
    pygame.draw.ellipse(win, WHITE, (ball_x, ball_y, ball_width, ball_width))
    pygame.display.update()

    time.sleep(0.02)  # Задержка для симуляции скорости мяча

pygame.quit()