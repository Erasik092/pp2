import pygame
import datetime
import os
from clock import rotate_hand

pygame.init()
W, H = 800, 800
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Mickey's Clock")

# 1. Определяем путь к папке со скриптом
current_path = os.path.dirname(__file__)

# 2. Загружаем всё через os.path.join (это самый надежный метод)
bg_path = os.path.join(current_path, 'images', 'mickeyclock.jpeg')
long_path = os.path.join(current_path, 'images', 'mickeys_long_hand.jpg')
short_path = os.path.join(current_path, 'images', 'mickeys_short_hand.jpg')

# 3. Загружаем картинки в Pygame
bg = pygame.image.load(bg_path)
bg = pygame.transform.scale(bg, (W, H)) # Масштабируем под окно

hand_long = pygame.image.load(long_path)  # Минуты
hand_short = pygame.image.load(short_path) # Секунды

hand_long = pygame.transform.scale(hand_long, (40, 300))  
hand_short = pygame.transform.scale(hand_short, (30, 350))

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = datetime.datetime.now()
    
    # Расчет углов
    # Корректировка: чтобы 0 секунд смотрели ровно вверх (на 12 часов), 
    # иногда нужно добавить смещение в 90 градусов, 
    # но обычно достаточно просто -(now.second * 6), если картинка руки изначально вертикальная.
    angle_s = -(now.second * 6)
    angle_m = -(now.minute * 6)

    screen.fill((255, 255, 255))
    screen.blit(bg, (0, 0))

    # Минуты (длинная рука)
    img_m, rect_m = rotate_hand(screen, hand_long, angle_m)
    screen.blit(img_m, rect_m)

    # Секунды (короткая рука)
    img_s, rect_s = rotate_hand(screen, hand_short, angle_s)
    screen.blit(img_s, rect_s)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()