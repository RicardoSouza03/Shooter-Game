import pygame

def display_text(screen, text: str, location: tuple, font_size: int):
    font = pygame.font.Font('sprites/Planes_ValMore.ttf', font_size)
    text_surface = font.render(str(text), False, 'White')
    screen.blit(text_surface, location)