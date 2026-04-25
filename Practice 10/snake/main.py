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

# --- ИНИЦИАЛИЗАЦИЯ ---
pygame.init()

WIDTH = 600
HEIGHT = 600
CELL = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Level System")

# Шрифты для интерфейса
font_small = pygame.font.SysFont("Verdana", 20)
font_big = pygame.font.SysFont("Verdana", 60)

# --- КЛАССЫ ---

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self):
        # Начальное тело змейки
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 0
        self.dy = -1 # Сразу начинаем движение вверх

    def move(self):
        # Двигаем хвост за головой
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def draw(self):
        # Рисуем голову красным, остальное желтым
        for i, segment in enumerate(self.body):
            color = colorRED if i == 0 else colorYELLOW
            pygame.draw.rect(screen, color, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self):
        head = self.body[0]
        # 1. Проверка столкновения со стенами
        if head.x < 0 or head.x >= WIDTH // CELL or head.y < 0 or head.y >= HEIGHT // CELL:
            return True
        # 2. Проверка столкновения с самим собой
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True
        return False

class Food:
    def __init__(self, snake_body):
        self.pos = Point(9, 9)
        self.generate_random_pos(snake_body)

    def draw(self):
        pygame.draw.rect(screen, colorGREEN, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_pos(self, snake_body):
        # Задача 2: Генерация еды вне тела змейки
        while True:
            self.pos.x = random.randint(0, (WIDTH // CELL) - 1)
            self.pos.y = random.randint(0, (HEIGHT // CELL) - 1)
            
            # Проверяем, не попали ли мы на змейку
            is_on_snake = False
            for segment in snake_body:
                if segment.x == self.pos.x and segment.y == self.pos.y:
                    is_on_snake = True
                    break
            
            if not is_on_snake:
                break

# --- ФУНКЦИИ ---

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
    # 1. Обработка событий (Клавиши)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Защита: нельзя повернуть в противоположную сторону
            if event.key == pygame.K_RIGHT and snake.dx != -1:
                snake.dx, snake.dy = 1, 0
            elif event.key == pygame.K_LEFT and snake.dx != 1:
                snake.dx, snake.dy = -1, 0
            elif event.key == pygame.K_DOWN and snake.dy != -1:
                snake.dx, snake.dy = 0, 1
            elif event.key == pygame.K_UP and snake.dy != 1:
                snake.dx, snake.dy = 0, -1

    # 2. Логика (Движение и столкновения)
    snake.move()

    # Проверка на проигрыш (Задача 1)
    if snake.check_collision():
        screen.fill(colorRED)
        over_text = font_big.render("GAME OVER", True, colorWHITE)
        screen.blit(over_text, (WIDTH//2 - 180, HEIGHT//2 - 50))
        pygame.display.flip()
        time.sleep(2) # Пауза перед закрытием
        running = False

    # Проверка поедания еды
    head = snake.body[0]
    if head.x == food.pos.x and head.y == food.pos.y:
        score += 1
        # Растем (добавляем точку в ту же позицию, где голова)
        snake.body.append(Point(head.x, head.y))
        food.generate_random_pos(snake.body)
        
        # Задача 3 и 4: Уровни и скорость
        # Каждые 3 съеденных фрукта — новый уровень
        if score % 3 == 0:
            level += 1

    # 3. Отрисовка
    screen.fill(colorBLACK)
    draw_grid()
    snake.draw()
    food.draw()

    # Задача 5: Счетчик очков и уровня
    score_text = font_small.render(f"Score: {score}   Level: {level}", True, colorWHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    # Управление скоростью (Задача 4)
    # С каждым уровнем прибавляем по 2 к FPS
    current_fps = base_fps + (level - 1) * 2
    clock.tick(current_fps)

pygame.quit()