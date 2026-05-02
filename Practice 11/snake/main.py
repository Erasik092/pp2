import pygame
import random
import time

# --- БЛОК ЦВЕТОВ ---
colorWHITE = (255, 255, 255)
colorGRAY = (40, 40, 40)
colorBLACK = (0, 0, 0)
colorRED = (255, 0, 0)
colorGREEN = (0, 255, 0)
colorYELLOW = (255, 255, 0)
colorGOLD = (255, 215, 0) # Цвет для "тяжелой" еды

# --- ИНИЦИАЛИЗАЦИЯ ---
pygame.init()

WIDTH = 600
HEIGHT = 600
CELL = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Food Weights & Timers")

font_small = pygame.font.SysFont("Verdana", 20)
font_big = pygame.font.SysFont("Verdana", 60)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 0
        self.dy = -1 

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def draw(self):
        for i, segment in enumerate(self.body):
            color = colorRED if i == 0 else colorYELLOW
            pygame.draw.rect(screen, color, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self):
        head = self.body[0]
        if head.x < 0 or head.x >= WIDTH // CELL or head.y < 0 or head.y >= HEIGHT // CELL:
            return True
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True
        return False

class Food:
    def __init__(self, snake_body):
        self.pos = Point(0, 0)
        self.weight = 1
        self.timer = 0
        self.last_update_time = time.time()
        self.generate_random_pos(snake_body)

    def generate_random_pos(self, snake_body):
        # 1. Рандомный вес: 20% шанс на золотую еду (вес 3), иначе обычная (вес 1)
        if random.random() < 0.2:
            self.weight = 3
            self.color = colorGOLD
            self.lifetime = 3  # Золотая еда исчезает через 3 секунды
        else:
            self.weight = 1
            self.color = colorGREEN
            self.lifetime = 7  # Обычная еда исчезает через 7 секунд
        
        self.timer = self.lifetime
        self.last_update_time = time.time()

        # 2. Генерация позиции вне тела змейки
        while True:
            self.pos.x = random.randint(0, (WIDTH // CELL) - 1)
            self.pos.y = random.randint(0, (HEIGHT // CELL) - 1)
            is_on_snake = any(s.x == self.pos.x and s.y == self.pos.y for s in snake_body)
            if not is_on_snake:
                break

    def update(self, snake_body):
        # Проверяем, сколько времени прошло с момента последней генерации
        current_time = time.time()
        elapsed = current_time - self.last_update_time
        
        # Если время вышло, пересоздаем еду
        if elapsed >= self.lifetime:
            self.generate_random_pos(snake_body)

    def draw(self):
        # Рисуем еду
        pygame.draw.rect(screen, self.color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))
        # Рисуем маленькую полоску таймера над едой для наглядности
        timer_width = (self.lifetime - (time.time() - self.last_update_time)) / self.lifetime * CELL
        if timer_width > 0:
            pygame.draw.rect(screen, colorWHITE, (self.pos.x * CELL, self.pos.y * CELL - 5, timer_width, 3))

def draw_grid():
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, colorGRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, colorGRAY, (0, y), (WIDTH, y))

# --- ГЛАВНЫЙ ЦИКЛ ---
snake = Snake()
food = Food(snake.body)
score = 0
level = 1
base_fps = 5

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake.dx != -1:
                snake.dx, snake.dy = 1, 0
            elif event.key == pygame.K_LEFT and snake.dx != 1:
                snake.dx, snake.dy = -1, 0
            elif event.key == pygame.K_DOWN and snake.dy != -1:
                snake.dx, snake.dy = 0, 1
            elif event.key == pygame.K_UP and snake.dy != 1:
                snake.dx, snake.dy = 0, -1

    snake.move()

    # Проверка таймера еды (исчезновение по времени)
    food.update(snake.body)

    if snake.check_collision():
        screen.fill(colorRED)
        over_text = font_big.render("GAME OVER", True, colorWHITE)
        screen.blit(over_text, (WIDTH//2 - 180, HEIGHT//2 - 50))
        pygame.display.flip()
        time.sleep(2)
        running = False

    head = snake.body[0]
    if head.x == food.pos.x and head.y == food.pos.y:
        # Прибавляем вес еды к счету
        score += food.weight
        # Змейка растет (пропорционально весу или на 1 сегмент)
        snake.body.append(Point(head.x, head.y))
        
        # Обновляем уровень каждые 5 очков
        level = (score // 5) + 1
        
        # Генерируем новую еду сразу после поедания
        food.generate_random_pos(snake.body)

    screen.fill(colorBLACK)
    draw_grid()
    snake.draw()
    food.draw()

    # Интерфейс
    score_text = font_small.render(f"Score: {score}  Level: {level}", True, colorWHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    # Скорость растет с уровнем
    current_fps = base_fps + (level - 1) * 2
    clock.tick(current_fps)

pygame.quit()