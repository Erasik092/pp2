import pygame
import math

def main():
    # Инициализация Pygame
    pygame.init()
    WIDTH, HEIGHT = 900, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame Paint: Touchpad & Mouse Edition")
    
    # Цветовая палитра
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    DARK_GRAY = (50, 50, 50)
    COLORS = {'Red': (255, 0, 0), 'Green': (0, 255, 0), 'Blue': (0, 0, 255)}

    # Холст (Surface), на котором мы рисуем. Он находится под панелью управления.
    canvas = pygame.Surface((WIDTH, HEIGHT - 100))
    canvas.fill(BLACK)
    
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)
    
    # Состояние редактора
    radius = 15
    drawing = False
    tool = 'brush'
    color = COLORS['Blue']
    last_pos = None
    start_pos = None

    # Описание кнопок интерфейса
    tools_ui = [
        {'name': 'brush', 'rect': pygame.Rect(10, 10, 80, 30)},
        {'name': 'eraser', 'rect': pygame.Rect(100, 10, 80, 30)},
        {'name': 'square', 'rect': pygame.Rect(190, 10, 80, 30)},
        {'name': 'right_tri', 'rect': pygame.Rect(280, 10, 80, 30)},
        {'name': 'eq_tri', 'rect': pygame.Rect(370, 10, 80, 30)},
        {'name': 'rhombus', 'rect': pygame.Rect(460, 10, 80, 30)},
    ]

    running = True
    while running:
        # Фон основного окна
        screen.fill(DARK_GRAY)
        
        # --- Отрисовка интерфейса ---
        pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 100)) # Панель инструментов
        
        for t in tools_ui:
            # Подсветка выбранной кнопки
            btn_color = WHITE if tool == t['name'] else BLACK
            pygame.draw.rect(screen, btn_color, t['rect'], 2)
            lbl = font.render(t['name'], True, BLACK)
            screen.blit(lbl, (t['rect'].x + 5, t['rect'].y + 5))

        # Индикаторы цветов
        pygame.draw.circle(screen, COLORS['Red'], (600, 25), 15)
        pygame.draw.circle(screen, COLORS['Green'], (640, 25), 15)
        pygame.draw.circle(screen, COLORS['Blue'], (680, 25), 15)

        # Текст с текущим размером (для тачпада очень полезно)
        size_txt = font.render(f"Size: {radius}  (Use +/- or Scroll)", True, BLACK)
        screen.blit(size_txt, (720, 20))

        # --- Обработка событий ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 1. Изменение размера через клавиатуру (+ и -)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    radius = min(100, radius + 2)
                if event.key == pygame.K_MINUS:
                    radius = max(1, radius - 2)

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Проверка нажатия на кнопки меню
                in_menu = False
                for t in tools_ui:
                    if t['rect'].collidepoint(event.pos):
                        tool = t['name']
                        in_menu = True
                
                # Проверка выбора цвета
                if math.dist(event.pos, (600, 25)) < 15: color = COLORS['Red']; in_menu = True
                if math.dist(event.pos, (640, 25)) < 15: color = COLORS['Green']; in_menu = True
                if math.dist(event.pos, (680, 25)) < 15: color = COLORS['Blue']; in_menu = True

                # 2. Изменение размера через колесико мыши
                if event.button == 4: # Scroll Up
                    radius = min(100, radius + 2)
                    in_menu = True
                elif event.button == 5: # Scroll Down
                    radius = max(1, radius - 2)
                    in_menu = True

                # Начало рисования (если мы не в меню)
                if not in_menu and event.pos[1] > 100:
                    drawing = True
                    start_pos = (event.pos[0], event.pos[1] - 100)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    # Финальная отрисовка фигуры на холст
                    end_p = (event.pos[0], event.pos[1] - 100)
                    draw_shape(canvas, tool, color, start_pos, end_p, radius)
                    drawing = False
                    start_pos = None

            if event.type == pygame.MOUSEMOTION:
                curr_p = (event.pos[0], event.pos[1] - 100)
                if drawing:
                    if tool == 'brush':
                        drawLineBetween(canvas, curr_p, last_pos, radius, color)
                    elif tool == 'eraser':
                        drawLineBetween(canvas, curr_p, last_pos, radius, BLACK)
                last_pos = curr_p

        # --- Отрисовка на экран ---
        screen.blit(canvas, (0, 100)) # Рисуем холст с отступом под панель

        # Превью фигуры (пока тянем мышь)
        if drawing and start_pos and tool not in ['brush', 'eraser']:
            # Рисуем временную фигуру поверх всего
            # Прибавляем 100 к Y, так как на экран рисуем без смещения Surface
            preview_start = (start_pos[0], start_pos[1] + 100)
            draw_shape(screen, tool, color, preview_start, pygame.mouse.get_pos(), radius)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# --- Вспомогательные функции рисования ---

def drawLineBetween(surface, start, end, width, color):
    """Рисует плавную линию кругами."""
    if end is None:
        pygame.draw.circle(surface, color, start, width)
        return
    dx, dy = start[0] - end[0], start[1] - end[1]
    dist = max(abs(dx), abs(dy))
    for i in range(dist):
        p = i / dist
        x = int((1 - p) * start[0] + p * end[0])
        y = int((1 - p) * start[1] + p * end[1])
        pygame.draw.circle(surface, color, (x, y), width)

def draw_shape(surf, name, color, start, end, width):
    """Универсальная функция для отрисовки выбранной фигуры."""
    x1, y1 = start
    x2, y2 = end
    
    if name == 'square':
        side = max(abs(x1 - x2), abs(y1 - y2))
        sx = x1 if x2 > x1 else x1 - side
        sy = y1 if y2 > y1 else y1 - side
        pygame.draw.rect(surf, color, (sx, sy, side, side), width)
        
    elif name == 'right_tri':
        pygame.draw.polygon(surf, color, [start, (x1, y2), end], width)
        
    elif name == 'eq_tri':
        side = math.dist(start, end)
        h = (math.sqrt(3)/2) * side
        points = [(x1, y1 - h/2), (x1 - side/2, y1 + h/2), (x1 + side/2, y1 + h/2)]
        pygame.draw.polygon(surf, color, points, width)
        
    elif name == 'rhombus':
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        points = [(mx, y1), (x2, my), (mx, y2), (x1, my)]
        pygame.draw.polygon(surf, color, points, width)

if __name__ == "__main__":
    main()