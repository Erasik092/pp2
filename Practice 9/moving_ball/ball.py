import pygame

class Ball:
    def __init__(self, x, y, radius, color, screen_width, screen_height):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.step = 20 # Шаг перемещения по заданию

    def move(self, dx, dy):
        # Рассчитываем новые координаты
        new_x = self.x + dx
        new_y = self.y + dy

        # Проверка границ: центр шарика +/- радиус не должен выходить за края экрана
        if (self.radius <= new_x <= self.screen_width - self.radius) and \
           (self.radius <= new_y <= self.screen_height - self.radius):
            self.x = new_x
            self.y = new_y

    def draw(self, screen):
        # Рисуем круг: экран, цвет, координаты центра, радиус
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)