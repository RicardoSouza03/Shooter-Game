import pygame

class Controller():
    def __init__(self) -> None:
        self.running = True
        self.screen_width = 800
        self.screen_heigth = 500
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_heigth))

    def start(self):
        pygame.init()
        pygame.display.set_caption("Shooter game")
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

if __name__ == "__main__":
    Controller().start()