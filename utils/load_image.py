import pygame

def load_image(path: str, scale: bool, dimensions=(0,0)):
    if not scale:
        image = pygame.image.load(path).convert_alpha()
    else:
        image = pygame.transform.scale(pygame.image.load(path).convert_alpha(), dimensions)
    return image