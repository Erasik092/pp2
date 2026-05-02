import pygame
import math
import datetime

# --- Constants ---
WIDTH, HEIGHT = 900, 700
TOOLBAR_HEIGHT = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
COLORS = {'Red': (255, 0, 0), 'Green': (0, 255, 0), 'Blue': (0, 0, 255)}

def flood_fill(surface, x, y, new_color):
    """Stack-based flood fill to avoid recursion limits."""
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return
    
    w, h = surface.get_size()
    stack = [(x, y)]
    
    while stack:
        curr_x, curr_y = stack.pop()
        if surface.get_at((curr_x, curr_y)) != target_color:
            continue
        
        surface.set_at((curr_x, curr_y), new_color)
        
        # Check neighbors
        if curr_x > 0: stack.append((curr_x - 1, curr_y))
        if curr_x < w - 1: stack.append((curr_x + 1, curr_y))
        if curr_y > 0: stack.append((curr_x, curr_y - 1))
        if curr_y < h - 1: stack.append((curr_x, curr_y + 1))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame Paint: Pro Edition")
    
    canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
    canvas.fill(BLACK)
    
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)
    
    # State
    radius = 5
    drawing = False
    tool = 'brush'
    color = COLORS['Blue']
    last_pos = None
    start_pos = None
    
    # Text Tool State
    typing = False
    text_pos = (0, 0)
    current_text = ""

    tools_ui = [
        {'name': 'brush', 'rect': pygame.Rect(10, 10, 70, 30)},
        {'name': 'line', 'rect': pygame.Rect(90, 10, 70, 30)},
        {'name': 'eraser', 'rect': pygame.Rect(170, 10, 70, 30)},
        {'name': 'fill', 'rect': pygame.Rect(250, 10, 70, 30)},
        {'name': 'text', 'rect': pygame.Rect(330, 10, 70, 30)},
        {'name': 'square', 'rect': pygame.Rect(10, 50, 70, 30)},
        {'name': 'right_tri', 'rect': pygame.Rect(90, 50, 70, 30)},
        {'name': 'eq_tri', 'rect': pygame.Rect(170, 50, 70, 30)},
        {'name': 'rhombus', 'rect': pygame.Rect(250, 50, 70, 30)},
    ]

    running = True
    while running:
        screen.fill(DARK_GRAY)
        
        # --- UI Rendering ---
        pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))
        for t in tools_ui:
            btn_color = WHITE if tool == t['name'] else BLACK
            pygame.draw.rect(screen, btn_color, t['rect'], 2)
            lbl = font.render(t['name'], True, BLACK)
            screen.blit(lbl, (t['rect'].x + 5, t['rect'].y + 5))

        # Color and Size indicators
        pygame.draw.circle(screen, COLORS['Red'], (450, 25), 15)
        pygame.draw.circle(screen, COLORS['Green'], (490, 25), 15)
        pygame.draw.circle(screen, COLORS['Blue'], (530, 25), 15)
        
        size_info = font.render(f"Size: {radius} (Keys 1, 2, 3)", True, BLACK)
        screen.blit(size_info, (600, 20))
        save_info = font.render("Ctrl+S to Save", True, BLACK)
        screen.blit(save_info, (600, 50))

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # 3.4 Save Canvas
                if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    fname = datetime.datetime.now().strftime("save_%Y%m%d_%H%M%S.png")
                    pygame.image.save(canvas, fname)
                    print(f"Saved as {fname}")

                # 3.2 Brush Size Shortcuts
                if event.key == pygame.K_1: radius = 2
                if event.key == pygame.K_2: radius = 5
                if event.key == pygame.K_3: radius = 10
                
                # 3.5 Text Handling
                if typing:
                    if event.key == pygame.K_RETURN:
                        txt_surf = font.render(current_text, True, color)
                        canvas.blit(txt_surf, text_pos)
                        typing = False
                        current_text = ""
                    elif event.key == pygame.K_ESCAPE:
                        typing = False
                        current_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        current_text = current_text[:-1]
                    else:
                        current_text += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                in_menu = False
                
                # Check UI
                for t in tools_ui:
                    if t['rect'].collidepoint(event.pos):
                        tool = t['name']
                        in_menu = True
                
                if math.dist(event.pos, (450, 25)) < 15: color = COLORS['Red']; in_menu = True
                if math.dist(event.pos, (490, 25)) < 15: color = COLORS['Green']; in_menu = True
                if math.dist(event.pos, (530, 25)) < 15: color = COLORS['Blue']; in_menu = True

                if not in_menu and my > TOOLBAR_HEIGHT:
                    canvas_pos = (mx, my - TOOLBAR_HEIGHT)
                    # 3.3 Flood Fill
                    if tool == 'fill':
                        flood_fill(canvas, canvas_pos[0], canvas_pos[1], color)
                    # 3.5 Text Placement
                    elif tool == 'text':
                        typing = True
                        text_pos = canvas_pos
                        current_text = ""
                    else:
                        drawing = True
                        start_pos = canvas_pos
                        last_pos = canvas_pos

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    end_p = (event.pos[0], event.pos[1] - TOOLBAR_HEIGHT)
                    draw_shape(canvas, tool, color, start_pos, end_p, radius)
                    drawing = False

            if event.type == pygame.MOUSEMOTION:
                if drawing and tool in ['brush', 'eraser']:
                    curr_p = (event.pos[0], event.pos[1] - TOOLBAR_HEIGHT)
                    c = BLACK if tool == 'eraser' else color
                    # 3.1 Pencil Tool (Brush)
                    pygame.draw.line(canvas, c, last_pos, curr_p, radius * 2)
                    last_pos = curr_p

        # --- Final Blit & Preview ---
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

        # Shape Previews
        if drawing and start_pos and tool not in ['brush', 'eraser']:
            preview_start = (start_pos[0], start_pos[1] + TOOLBAR_HEIGHT)
            draw_shape(screen, tool, color, preview_start, pygame.mouse.get_pos(), radius)
        
        # Text Preview
        if typing:
            preview_txt = font.render(current_text + "|", True, color)
            screen.blit(preview_txt, (text_pos[0], text_pos[1] + TOOLBAR_HEIGHT))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def draw_shape(surf, name, color, start, end, width):
    x1, y1 = start
    x2, y2 = end
    
    if name == 'line':
        pygame.draw.line(surf, color, start, end, width)
    elif name == 'square':
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