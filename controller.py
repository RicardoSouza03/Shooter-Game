import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_size) -> None:
        super().__init__()
        self.x = screen_size[0]/2
        self.y = screen_size[1]/2
        self.screen = (screen_size[0], screen_size[1])
        self.image = pygame.Surface((60,60))
        self.image.fill((225, 225, 225))
        self.rect = self.image.get_rect(center = (self.x, self.y))

class Controller():
    def __init__(self) -> None:
        self.running = True
        self.clock = pygame.time.Clock()
        self.screen_width = 800
        self.screen_heigth = 500
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_heigth))

    def start(self):
        pygame.init()
        pygame.display.set_caption("Shooter game")
        player = Player((self.screen_width, self.screen_heigth))
        player_group = pygame.sprite.Group()
        player_group.add(player)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            player_group.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    Controller().start()