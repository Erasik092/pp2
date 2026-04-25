import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    # Создаем отдельный слой (Surface) для рисования, чтобы оно не стиралось каждый кадр
    canvas = pygame.Surface((800, 600))
    canvas.fill((0, 0, 0))
    
    clock = pygame.time.Clock()
    
    radius = 15
    drawing = False
    last_pos = None
    
    # Инструменты: 'brush', 'rectangle', 'circle', 'eraser'
    tool = 'brush'
    color = (0, 0, 255) # Синий по умолчанию
    start_pos = None # Для рисования фигур

    print("Управление:")
    print("1-Кисть, 2-Прямоугольник, 3-Круг, 4-Ластик")
    print("R, G, B - Выбор цвета")
    print("Scroll / Кнопки мыши - Изменение размера")

    while True:
        screen.fill((30, 30, 30)) # Цвет фона окна
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                # Выбор инструментов
                if event.key == pygame.K_1: tool = 'brush'
                if event.key == pygame.K_2: tool = 'rectangle'
                if event.key == pygame.K_3: tool = 'circle'
                if event.key == pygame.K_4: tool = 'eraser'
                
                # Выбор цвета
                if event.key == pygame.K_r: color = (255, 0, 0)
                if event.key == pygame.K_g: color = (0, 255, 0)
                if event.key == pygame.K_b: color = (0, 0, 255)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # ЛКМ
                    drawing = True
                    start_pos = event.pos
                elif event.button == 4: # Колесо вверх
                    radius = min(100, radius + 1)
                elif event.button == 5: # Колесо вниз
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    # Если рисовали фигуру, фиксируем её на холсте при отпускании
                    if tool == 'rectangle':
                        drawRect(canvas, color, start_pos, event.pos, radius)
                    elif tool == 'circle':
                        drawCircle(canvas, color, start_pos, event.pos, radius)
                    start_pos = None

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if tool == 'brush':
                        drawLineBetween(canvas, event.pos, last_pos, radius, color)
                    elif tool == 'eraser':
                        drawLineBetween(canvas, event.pos, last_pos, radius, (0, 0, 0))
                last_pos = event.pos

        # Отрисовка холста на экран
        screen.blit(canvas, (0, 0))
        
        # Визуализация будущей фигуры в реальном времени (превью)
        if drawing and start_pos:
            curr_pos = pygame.mouse.get_pos()
            if tool == 'rectangle':
                drawRect(screen, color, start_pos, curr_pos, radius)
            elif tool == 'circle':
                drawCircle(screen, color, start_pos, curr_pos, radius)

        pygame.display.flip()
        clock.tick(60)

def drawLineBetween(surface, start, end, width, color):
    if end is None:
        pygame.draw.circle(surface, color, start, width)
        return
    
    # Алгоритм из примера: заполнение линии кругами для плавности
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    
    for i in range(iterations):
        progress = i / iterations
        x = int((1 - progress) * start[0] + progress * end[0])
        y = int((1 - progress) * start[1] + progress * end[1])
        pygame.draw.circle(surface, color, (x, y), width)

def drawRect(surface, color, start_pos, end_pos, width):
    x1, y1 = start_pos
    x2, y2 = end_pos
    rect_x = min(x1, x2)
    rect_y = min(y1, y2)
    rect_w = abs(x1 - x2)
    rect_h = abs(y1 - y2)
    if rect_w > 0 and rect_h > 0:
        pygame.draw.rect(surface, color, (rect_x, rect_y, rect_w, rect_h), width)

def drawCircle(surface, color, start_pos, end_pos, width):
    x1, y1 = start_pos
    x2, y2 = end_pos
    # Вычисляем радиус как расстояние между начальной и текущей точкой
    r = int(((x1 - x2)**2 + (y1 - y2)**2)**0.5)
    if r > 0:
        pygame.draw.circle(surface, color, start_pos, r, width)

main()