import pygame

def load_image(path: str, scale: bool, dimensions: tuple):
    if scale:
        image = pygame.transform.scale(pygame.image.load(path).convert_alpha(), dimensions)
    else:
        image = pygame.image.load(path).convert_alpha()
    return image