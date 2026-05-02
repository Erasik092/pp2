import pygame, sys, random, json, os, time
from pygame.locals import *

pygame.init()

# ---------- PATH ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_DIR, "assets")

def load_img(name):
    return pygame.image.load(os.path.join(ASSETS, name))

# ---------- SETTINGS ----------
def load_settings():
    try:
        with open("settings.json") as f:
            return json.load(f)
    except:
        return {"sound": True, "difficulty": "normal"}

def save_settings(data):
    with open("settings.json", "w") as f:
        json.dump(data, f, indent=4)

settings = load_settings()

# ---------- LEADERBOARD ----------
def load_leaderboard():
    try:
        with open("leaderboard.json") as f:
            return json.load(f)
    except:
        return []

def save_score(score):
    data = load_leaderboard()
    data.append(score)
    data = sorted(data, reverse=True)[:10]
    with open("leaderboard.json", "w") as f:
        json.dump(data, f, indent=4)

# ---------- VARS ----------
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Game")

FPS = 60
clock = pygame.time.Clock()

background = load_img("AnimatedStreet.png")

# difficulty
if settings["difficulty"] == "easy":
    BASE_SPEED = 4
elif settings["difficulty"] == "normal":
    BASE_SPEED = 5
else:
    BASE_SPEED = 7

SPEED = BASE_SPEED
SCORE = 0
COIN_SCORE = 0

HAS_SHIELD = False
NITRO_ACTIVE = False
nitro_end = 0

barrier_timer = 0
shield_timer = 0
nitro_timer = 0

game_state = "menu"

# ---------- FONTS ----------
font_big = pygame.font.SysFont("Verdana", 50)
font_small = pygame.font.SysFont("Verdana", 20)

# ---------- BUTTON ----------
class Button:
    def __init__(self, text, x, y):
        self.rect = pygame.Rect(x, y, 200, 50)
        self.text = font_small.render(text, True, (255,255,255))

    def draw(self):
        pygame.draw.rect(screen, (0,0,0), self.rect)
        screen.blit(self.text, (self.rect.x+40, self.rect.y+15))

    def click(self, pos):
        return self.rect.collidepoint(pos)

play_btn = Button("Play", 100, 150)
settings_btn = Button("Settings", 100, 220)
leader_btn = Button("Leaderboard", 100, 290)
quit_btn = Button("Quit", 100, 360)
retry_btn = Button("Retry", 100, 350)
menu_btn = Button("Menu", 100, 420)

# ---------- CLASSES ----------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_img("Player.png")
        self.rect = self.image.get_rect(center=(160,520))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5,0)
        if keys[K_RIGHT] and self.rect.right < WIDTH:
            self.rect.move_ip(5,0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_img("Enemy.png")
        self.rect = self.image.get_rect(center=(random.randint(40, WIDTH-40), 0))

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, WIDTH-40), 0)

class Barrier(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = load_img("barrier.png")
        self.image = pygame.transform.scale(img, (50,80))
        self.rect = self.image.get_rect()
        self.active = False

    def spawn(self):
        while True:
            self.rect.center = (random.randint(40, WIDTH-40), -100)
            if not pygame.sprite.spritecollideany(self, enemies):
                break
        self.active = True

    def move(self):
        if self.active:
            self.rect.move_ip(0, SPEED)
            if self.rect.top > HEIGHT:
                self.active = False

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = load_img("coin.png")
        self.image = pygame.transform.scale(img, (30,30))
        self.rect = self.image.get_rect()
        self.spawn()

    def spawn(self):
        self.rect.center = (random.randint(40, WIDTH-40), -50)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > HEIGHT:
            self.spawn()

class Shield(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = load_img("shield.png")
        self.image = pygame.transform.scale(img, (35,35))
        self.rect = self.image.get_rect()
        self.active = False

    def spawn(self):
        self.rect.center = (random.randint(40, WIDTH-40), -50)
        self.active = True

    def move(self):
        if self.active:
            self.rect.move_ip(0, SPEED)
            if self.rect.top > HEIGHT:
                self.active = False

class Nitro(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = load_img("nitro.png")
        self.image = pygame.transform.scale(img, (35,35))
        self.rect = self.image.get_rect()
        self.active = False

    def spawn(self):
        self.rect.center = (random.randint(40, WIDTH-40), -50)
        self.active = True

    def move(self):
        if self.active:
            self.rect.move_ip(0, SPEED)
            if self.rect.top > HEIGHT:
                self.active = False

# ---------- INIT ----------
P1 = Player()
E1 = Enemy()
B1 = Barrier()
C1 = Coin()
S1 = Shield()
N1 = Nitro()

enemies = pygame.sprite.Group(E1)

def reset_game():
    global SPEED, SCORE, COIN_SCORE, HAS_SHIELD, NITRO_ACTIVE
    SPEED = BASE_SPEED
    SCORE = 0
    COIN_SCORE = 0
    HAS_SHIELD = False
    NITRO_ACTIVE = False
    E1.rect.top = 0
    B1.active = False

# ---------- LOOP ----------
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN:

            if game_state == "menu":
                if play_btn.click(event.pos):
                    reset_game()
                    game_state = "game"
                elif settings_btn.click(event.pos):
                    game_state = "settings"
                elif leader_btn.click(event.pos):
                    game_state = "leaderboard"
                elif quit_btn.click(event.pos):
                    pygame.quit()
                    sys.exit()

            elif game_state == "game_over":
                if retry_btn.click(event.pos):
                    reset_game()
                    game_state = "game"
                elif menu_btn.click(event.pos):
                    game_state = "menu"

            elif game_state == "settings":
                if menu_btn.click(event.pos):
                    save_settings(settings)
                    game_state = "menu"
                else:
                    settings["sound"] = not settings["sound"]
                    if settings["difficulty"] == "easy":
                        settings["difficulty"] = "normal"
                    elif settings["difficulty"] == "normal":
                        settings["difficulty"] = "hard"
                    else:
                        settings["difficulty"] = "easy"

            elif game_state == "leaderboard":
                if menu_btn.click(event.pos):
                    game_state = "menu"

    # ---------- MENU ----------
    if game_state == "menu":
        screen.fill((255,255,255))
        screen.blit(font_big.render("CAR GAME", True, (0,0,0)), (70,50))
        play_btn.draw()
        settings_btn.draw()
        leader_btn.draw()
        quit_btn.draw()

    # ---------- GAME ----------
    elif game_state == "game":
        screen.blit(background, (0,0))

        barrier_timer += 1
        shield_timer += 1
        nitro_timer += 1

        if barrier_timer > random.randint(120,300):
            B1.spawn()
            barrier_timer = 0

        if shield_timer > random.randint(500,900):
            S1.spawn()
            shield_timer = 0

        if nitro_timer > random.randint(500,900):
            N1.spawn()
            nitro_timer = 0

        for e in [E1, B1, C1, S1, N1]:
            if hasattr(e, "active") and not e.active:
                continue
            screen.blit(e.image, e.rect)
            e.move()

        P1.move()
        screen.blit(P1.image, P1.rect)

        if P1.rect.colliderect(C1.rect):
            COIN_SCORE += 1
            C1.spawn()

        if S1.active and P1.rect.colliderect(S1.rect):
            HAS_SHIELD = True
            S1.active = False

        if N1.active and P1.rect.colliderect(N1.rect):
            NITRO_ACTIVE = True
            nitro_end = pygame.time.get_ticks() + random.randint(3000,5000)
            SPEED = BASE_SPEED + 3
            N1.active = False

        if NITRO_ACTIVE and pygame.time.get_ticks() > nitro_end:
            SPEED = BASE_SPEED
            NITRO_ACTIVE = False

        if P1.rect.colliderect(E1.rect) or (B1.active and P1.rect.colliderect(B1.rect)):
            if HAS_SHIELD:
                HAS_SHIELD = False
                B1.active = False
                E1.rect.top = 0
            else:
                save_score(SCORE)
                game_state = "game_over"

        screen.blit(font_small.render(f"Score: {SCORE}", True, (0,0,0)), (10,10))
        screen.blit(font_small.render(f"Coins: {COIN_SCORE}", True, (0,0,0)), (280,10))

    # ---------- GAME OVER ----------
    elif game_state == "game_over":
        screen.fill((255,255,255))
        screen.blit(font_big.render("GAME OVER", True, (255,0,0)), (50,150))
        screen.blit(font_small.render(f"Score: {SCORE}", True, (0,0,0)), (140,230))
        screen.blit(font_small.render(f"Coins: {COIN_SCORE}", True, (0,0,0)), (140,260))

        retry_btn.draw()
        menu_btn.draw()

    # ---------- SETTINGS ----------
    elif game_state == "settings":
        screen.fill((255,255,255))
        screen.blit(font_big.render("SETTINGS", True, (0,0,0)), (70,50))
        screen.blit(font_small.render(f"Sound: {settings['sound']}", True, (0,0,0)), (100,200))
        screen.blit(font_small.render(f"Difficulty: {settings['difficulty']}", True, (0,0,0)), (100,250))
        menu_btn.draw()

    # ---------- LEADERBOARD ----------
    elif game_state == "leaderboard":
        screen.fill((255,255,255))
        screen.blit(font_big.render("TOP SCORES", True, (0,0,0)), (50,50))
        scores = load_leaderboard()
        y = 150
        for s in scores:
            screen.blit(font_small.render(str(s), True, (0,0,0)), (180,y))
            y += 30
        menu_btn.draw()

    pygame.display.update()
    clock.tick(FPS)