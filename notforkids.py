import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Размер окна
screen_width = 1200
screen_height = 1200
screen = pygame.display.set_mode((screen_width, screen_height))

# Название игры
pygame.display.set_caption('Лошадка')

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Игрок
player_size = 75
player_x = screen_width / 4
player_y = screen_height / 4
player_speed = 2

# Загружаем изображения
player_image = pygame.image.load('player.png')  # Изображение игрока
player_image = pygame.transform.scale(player_image, (player_size, player_size))  # Изменяем размер

# Пуля
bullet_size = 25
bullet_speed = 7
bullets = []

# Загружаем изображение пули
bullet_image = pygame.image.load('bullet.png')  # Замените на путь к вашему изображению пули
bullet_image = pygame.transform.scale(bullet_image, (bullet_size, bullet_size))  # Изменяем размер изображения пули

# Враг
enemy_size = 200
enemy_x = random.randint(0, screen_width - enemy_size)
enemy_y = 0
enemy_speed = 0.5

# Загружаем изображение врага
enemy_image = pygame.image.load('enemy.png')  # Изображение врага
enemy_image = pygame.transform.scale(enemy_image, (enemy_size, enemy_size))  # Изменяем размер

# Загружаем изображение фона
background_image = pygame.image.load('background.jpeg')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Флаг конца игры
game_over = False

# Главный цикл игры
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            bullets.append([player_x + player_size / 2, player_y + player_size / 2])
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullets.append([player_x + player_size / 2, player_y + player_size / 2])
        if event.type == pygame.KEYDOWN and game_over:
            game_over = False
            player_x = screen_width / 2
            player_y = screen_height / 2
            enemy_x = random.randint(0, screen_width - enemy_size)
            enemy_y = 0
            bullets = []

    screen.blit(background_image, (0, 0))  # Отрисовываем изображение фона

    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_y -= player_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_y += player_speed
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_x += player_speed

    # Ограничение движения игрока
    player_x = max(0, min(player_x, screen_width - player_size))
    player_y = max(0, min(player_y, screen_height - player_size))

    # Движение врага
    enemy_y += enemy_speed
    if enemy_y > screen_height:
        enemy_x = random.randint(0, screen_width - enemy_size)
        enemy_y = 0

    # Движение пуль
    for i, bullet in enumerate(bullets):
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            del bullets[i]

    # Проверка столкновения пули с врагом
    for i, bullet in enumerate(bullets):
        if (bullet[0] > enemy_x and bullet[0] < enemy_x + enemy_size and
            bullet[1] > enemy_y and bullet[1] < enemy_y + enemy_size):
            del bullets[i]
            enemy_x = random.randint(0, screen_width - enemy_size)
            enemy_y = 0

    # Проверка столкновения игрока с врагом
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size)

    if player_rect.colliderect(enemy_rect):
        game_over = True

    # Отображение изображений
    if not game_over:
        screen.blit(player_image, (player_x, player_y))  # Рисуем изображение игрока
        for bullet in bullets:
            screen.blit(bullet_image, (bullet[0], bullet[1]))  # Рисуем изображение пули
        screen.blit(enemy_image, (enemy_x, enemy_y))  # Рисуем изображение врага
    else:
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over", True, RED)
        screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 2 - text.get_height() / 2))

    # Обновление экрана
    pygame.display.update()