import pygame, sys
from pygame.locals import *
import random, time

# Инициализация
pygame.init()

# Настройка FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Цвета
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Переменные
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COIN_SCORE = 0 
N_COINS_TO_SPEED_UP = 5 # Через сколько монет увеличивать скорость

# Шрифты
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("assets/AnimatedStreet.png")

DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("assets/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("assets/coin.png")
        self.weight = 1
        self.rect = pygame.Rect(0, 0, 0, 0) # Пустой rect для начала
        self.spawn_new()

    def spawn_new(self):
        # ЗАДАЧА 1: Рандомные веса монет
        # 1-3 — обычная, 4-5 — редкая/тяжелая
        chance = random.randint(1, 5)
        if chance <= 3:
            self.weight = 1
            size = (25, 25)
        else:
            self.weight = 3
            size = (40, 40)
        
        self.image = pygame.transform.scale(self.original_image, size)
        self.rect = self.image.get_rect()
        
        # ЗАДАЧА: Спавн так, чтобы не накладываться на врага
        while True:
            new_x = random.randint(40, SCREEN_WIDTH - 40)
            self.rect.center = (new_x, -50)
            # Проверяем коллизию с группой врагов при спавне
            if not pygame.sprite.spritecollideany(self, enemies):
                break

    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600):
            self.spawn_new()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("assets/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

# 1. Сначала создаем группы
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# 2. Теперь создаем игрока и врага
P1 = Player()
E1 = Enemy()
enemies.add(E1)

# 3. ТОЛЬКО ТЕПЕРЬ создаем монету 
# (теперь группа 'enemies' уже существует, и метод spawn_new() отработает без ошибок)
C1 = Coin() 
coins.add(C1)

# 4. Добавляем всех в общую группу отрисовки
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Событие таймера (оставляем для базового усложнения или убираем)
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            # Базовое ускорение со временем (можно закомментировать, если нужно только от монет)
            SPEED += 0.1     
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0,0))
    
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    coin_txt = font_small.render("Coins: " + str(COIN_SCORE), True, BLACK)
    
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coin_txt, (SCREEN_WIDTH - 120, 10))

    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # ПРОВЕРКА СБОРА МОНЕТ
    collided_coin = pygame.sprite.spritecollideany(P1, coins)
    if collided_coin:
        # Добавляем вес монеты к общему счету
        COIN_SCORE += collided_coin.weight
        
        # ЗАДАЧА 2: Увеличение скорости врага при наборе N монет
        # Если текущий счет кратен N_COINS_TO_SPEED_UP (например, 5, 10, 15...)
        if COIN_SCORE // N_COINS_TO_SPEED_UP > (COIN_SCORE - collided_coin.weight) // N_COINS_TO_SPEED_UP:
            SPEED += 1
            print(f"Speed increased! Current speed: {SPEED}")

        collided_coin.spawn_new()

    # Столкновение с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('assets/crash.wav').play()
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill() 
        time.sleep(2)
        pygame.quit()
        sys.exit()         
          
    pygame.display.update()
    FramePerSec.tick(FPS)