import pygame
import os
from player import MusicPlayer

# Инициализация
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Music Player")
font = pygame.font.SysFont("Verdana", 24)

# Пути к файлам
current_dir = os.path.dirname(__file__)
music_path = os.path.join(current_dir, 'music')

# Создаем плеер
player = MusicPlayer(music_path)

running = True
while running:
    screen.fill((25, 25, 25)) # Почти черный фон

    # Отображение информации
    track_text = font.render(f"Track: {player.get_current_name()}", True, (255, 255, 255))
    help_text = font.render("P: Play | S: Stop | N: Next | B: Back | Q: Quit", True, (150, 150, 150))
    
    screen.blit(track_text, (50, 150))
    screen.blit(help_text, (50, 250))

    # Обработка клавиш (Events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:     # P = Play
                player.play()
            elif event.key == pygame.K_s:   # S = Stop
                player.stop()
            elif event.key == pygame.K_n:   # N = Next
                player.next_track()
            elif event.key == pygame.K_b:   # B = Back (Previous)
                player.prev_track()
            elif event.key == pygame.K_q:   # Q = Quit
                running = False

    pygame.display.flip()

pygame.quit()