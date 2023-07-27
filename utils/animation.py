import pygame

class Animation(pygame.sprite.Sprite):
    def __init__(self, animation_sheet, steps, speed, width, height, scale, loop) -> None:
        super().__init__()
        self.sheet_image = pygame.image.load(animation_sheet).convert_alpha()
        self.frame = 0
        self.ended = False
        self.reset = True
        self.loop = loop
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
    
    def reset_animation(self, is_clicked):
        if not self.reset: 
            self.ended = True
            self.kill()

        if not self.ended and is_clicked:
            self.frame = len(self.animation_list) - 1
        elif self.ended:
            self.frame = 0

        if self.loop: self.frame = 0
        
    def update(self):
        is_clicked = pygame.mouse.get_pressed()

        current_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame]
        if current_time - self.last_update >= self.animation_speed:
            self.frame += 1
            self.last_update = current_time

        if self.frame >= self.steps:
            self.reset_animation(is_clicked)

    def set_ended(self, should_end):
        self.ended = should_end

    def set_reset(self, reset):
        self.reset = reset
