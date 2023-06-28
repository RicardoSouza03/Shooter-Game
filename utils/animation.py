import pygame

class Animation(pygame.sprite.Sprite):
    def __init__(self, scale: tuple, image_path, images_length) -> None:
        super().__init__()
        self.image_list = []
        self.index = 0
        self.counter = 0
        self.speed = 1
        self.ended = False
        for i in range(1, images_length):
            img = pygame.image.load(f'{image_path}{i + 1}.png').convert_alpha()
            img = pygame.transform.scale(img, scale)
            self.image_list.append(img)
        self.image = self.image_list[self.index]
    
    def update(self):
        self.counter += 1
        self.run_animation()

    def run_animation(self):
        if self.counter >= self.speed and self.index < len(self.image_list) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.image_list[self.index]

        if self.index >= len(self.image_list) - 1 and self.counter >= self.speed:
            self.ended = True
            self.kill()