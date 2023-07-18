import pygame

class Animation(pygame.sprite.Sprite):
    def __init__(self, animation_sheet, steps, speed, width, height, scale) -> None:
        super().__init__()
        self.sheet_image = pygame.image.load(animation_sheet).convert_alpha()
        self.frame = 0
        self.ended = True
        self.animation_speed = speed
        self.steps = steps
        self.width = width
        self.height = height
        self.scale = scale
        self.last_update = pygame.time.get_ticks()
        self.animation_list = []
        for counter in range(self.steps):
            self.animation_list.append(self.get_image(counter))
        self.image = self.animation_list[self.frame]

    def get_image(self, counter):
        image = pygame.Surface((self.width, self.height)).convert_alpha()
        image.blit(self.sheet_image, (0, 0), ((counter * self.width), 0, self.width, self.height))
        image = pygame.transform.scale(image, (self.width * self.scale, self.height * self.scale))
        image.set_colorkey((0, 0, 0))

        return image
    
    def update(self):
        current_time = pygame.time.get_ticks()
        self.ended = False
        self.image = self.animation_list[self.frame]

        if current_time - self.last_update >= self.animation_speed:
            self.frame += 1
            self.last_update = current_time
        if self.frame >= self.steps:
            self.ended = True
            self.frame = 0