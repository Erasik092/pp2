import pygame

def rotate_hand(screen, image, angle):
    # Вращаем картинку вокруг её центра
    rotated_image = pygame.transform.rotate(image, angle)
    # Берем прямоугольник повернутой картинки и центрируем его по центру экрана
    rect = rotated_image.get_rect(center=screen.get_rect().center)
    return rotated_image, rect