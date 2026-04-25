import pygame
from ball import Ball

# Инициализация
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Red Ball")

# Создаем объект шарика
# Радиус 25 (итого размер 50х50), цвет красный (255, 0, 0), позиция - центр экрана
red_ball = Ball(WIDTH // 2, HEIGHT // 2, 25, (255, 0, 0), WIDTH, HEIGHT)

clock = pygame.time.Clock()
running = True

while running:
    # 1. Заливаем фон белым цветом
    screen.fill((255, 255, 255))

    # 2. Проверяем события
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Обработка нажатий клавиш (KEYDOWN срабатывает один раз при нажатии)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                red_ball.move(0, -20)
            elif event.key == pygame.K_DOWN:
                red_ball.move(0, 20)
            elif event.key == pygame.K_LEFT:
                red_ball.move(-20, 0)
            elif event.key == pygame.K_RIGHT:
                red_ball.move(20, 0)

    # 3. Рисуем шарик
    red_ball.draw(screen)

    # 4. Обновляем экран
    pygame.display.flip()
    clock.tick(60) # Frame rate control (60 FPS)

pygame.quit()