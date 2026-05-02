import pygame, random, time
from config import *
import db
import json

# --- SETTINGS ---
with open("settings.json") as f:
    settings = json.load(f)

snake_color = tuple(settings["snake_color"])
show_grid = settings["grid"]

WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
PURPLE = (150,0,150)
DARKRED = (120,0,0)
GRAY = (40,40,40)


FOOD_LIFETIME = 8000  # 8 секунд


class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y


class Snake:
    def __init__(self):
        self.body=[Point(10,10)]
        self.dx=1
        self.dy=0
        self.shield=False

    def move(self):
        head = Point(self.body[0].x+self.dx, self.body[0].y+self.dy)
        self.body.insert(0, head)
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])

    def shrink(self):
        if len(self.body)>2:
            self.body.pop()
            self.body.pop()

    def draw(self,screen):
        for i,p in enumerate(self.body):
            if i == 0:
                pygame.draw.rect(screen, RED, (p.x*CELL,p.y*CELL,CELL,CELL))
            else:
                pygame.draw.rect(screen, snake_color, (p.x*CELL,p.y*CELL,CELL,CELL))


class Food:
    def __init__(self):
        self.spawn()

    def spawn(self):
        self.x = random.randint(0, WIDTH//CELL-1)
        self.y = random.randint(0, HEIGHT//CELL-1)
        self.type = random.choice(["normal","poison","speed","slow","shield"])
        self.spawn_time = pygame.time.get_ticks()

    def alive(self):
        return pygame.time.get_ticks() - self.spawn_time < FOOD_LIFETIME

    def time_left(self):
        return max(0, FOOD_LIFETIME - (pygame.time.get_ticks() - self.spawn_time))

    def draw(self,screen):
        color = GREEN
        if self.type=="poison": color=DARKRED
        if self.type=="speed": color=WHITE
        if self.type=="slow": color=PURPLE
        if self.type=="shield": color=(0,200,200)

        x = self.x * CELL
        y = self.y * CELL

        pygame.draw.rect(screen,color,(x,y,CELL,CELL))

        # --- TIMER BAR ---
        percent = self.time_left() / FOOD_LIFETIME
        bar_width = int(CELL * percent)

        pygame.draw.rect(
            screen,
            WHITE,
            (x, y-4, bar_width, 3)
        )


class Game:
    def __init__(self, username):
        pygame.init()
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock=pygame.time.Clock()

        self.snake=Snake()

        self.foods=[]
        self.spawn_foods()

        self.score=0
        self.level=1
        self.username=username
        self.best=db.get_best(username)

        self.speed=5
        self.speed_timer=0

        self.obstacles=[]


    def spawn_foods(self):
        self.foods = []
        for _ in range(5):
            self.foods.append(Food())


    def spawn_obstacles(self):
        self.obstacles=[]
        for _ in range(self.level):
            x=random.randint(0, WIDTH//CELL-1)
            y=random.randint(0, HEIGHT//CELL-1)
            self.obstacles.append((x,y))


    def draw_grid(self):
        if not show_grid: return
        for x in range(0,WIDTH,CELL):
            pygame.draw.line(self.screen,GRAY,(x,0),(x,HEIGHT))
        for y in range(0,HEIGHT,CELL):
            pygame.draw.line(self.screen,GRAY,(0,y),(WIDTH,y))


    def run(self):
        running=True

        while running:
            for e in pygame.event.get():
                if e.type==pygame.QUIT:
                    return

                if e.type==pygame.KEYDOWN:
                    if e.key==pygame.K_UP: self.snake.dx,self.snake.dy=0,-1
                    if e.key==pygame.K_DOWN: self.snake.dx,self.snake.dy=0,1
                    if e.key==pygame.K_LEFT: self.snake.dx,self.snake.dy=-1,0
                    if e.key==pygame.K_RIGHT: self.snake.dx,self.snake.dy=1,0


            self.snake.move()
            head=self.snake.body[0]


            # --- COLLISION WALL ---
            if (head.x<0 or head.x>=WIDTH//CELL or
                head.y<0 or head.y>=HEIGHT//CELL or
                (head.x,head.y) in self.obstacles):

                if self.snake.shield:
                    self.snake.shield=False
                else:
                    db.save_game(self.username,self.score,self.level)
                    return


            # --- FOOD LOGIC ---
            for food in self.foods[:]:

                # удалить если истёк таймер
                if not food.alive():
                    self.foods.remove(food)
                    self.foods.append(Food())
                    continue

                # съедение
                if head.x == food.x and head.y == food.y:

                    if food.type == "normal":
                        self.score += 1
                        self.snake.grow()

                    elif food.type == "poison":
                        self.snake.shrink()
                        if len(self.snake.body) <= 1:
                            db.save_game(self.username,self.score,self.level)
                            return

                    elif food.type == "speed":
                        self.speed = 10
                        self.speed_timer = pygame.time.get_ticks()

                    elif food.type == "slow":
                        self.speed = 3
                        self.speed_timer = pygame.time.get_ticks()

                    elif food.type == "shield":
                        self.snake.shield = True

                    self.foods.remove(food)
                    self.foods.append(Food())

                    self.level = self.score // 5 + 1

                    if self.level >= 3:
                        self.spawn_obstacles()

                    break


            # --- RESET SPEED ---
            if pygame.time.get_ticks() - self.speed_timer > 5000:
                self.speed = 5


            # --- DRAW ---
            self.screen.fill((0,0,0))
            self.draw_grid()

            for o in self.obstacles:
                pygame.draw.rect(self.screen,(100,100,100),(o[0]*CELL,o[1]*CELL,CELL,CELL))

            for food in self.foods:
                food.draw(self.screen)

            self.snake.draw(self.screen)


            # --- UI ---
            font=pygame.font.SysFont(None,24)
            txt=font.render(f"{self.score} lvl {self.level} best {self.best}",True,WHITE)
            self.screen.blit(txt,(10,10))


            # --- SPEED TIMER BAR ---
            if self.speed != 5:
                elapsed = pygame.time.get_ticks() - self.speed_timer
                percent = max(0, 1 - elapsed / 5000)
                pygame.draw.rect(self.screen, WHITE, (10, 40, 100 * percent, 5))


            pygame.display.flip()
            self.clock.tick(self.speed)