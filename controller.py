import pygame, math, random

def get_angle_between(point1, point2):
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    angle = math.atan2(dy, dx)
    return angle

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_size) -> None:
        super().__init__()
        self.x = screen_size[0]/2
        self.y = screen_size[1]/2
        self.screen = (screen_size[0], screen_size[1])
        self.image = pygame.Surface((60,60))
        self.image.fill((225, 225, 225))
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def create_bullet(self):
        mouse_pos = pygame.mouse.get_pos()
        angle = get_angle_between((self.x+(self.rect.width/2), self.y+(self.rect.height/2)), mouse_pos)
        return Bullet(self.x, self.y, self.screen, angle)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_size) -> None:
        super().__init__()
        self.spawn(screen_size)
        self.screen_size = screen_size
        self.speed = 1
        self.image = pygame.Surface((30,30))
        self.image.fill((225, 225, 225))
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def update(self, player):
        # Move enemy towards player.
        direction_x, direction_y = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        distance = math.hypot(direction_x, direction_y)
        direction_x, direction_y = direction_x / distance, direction_y / distance
        self.rect.x += direction_x * self.speed
        self.rect.y += direction_y * self.speed

    def spawn(self, screen_size):
        # Sets enemy position at a random position outside screen.
        random_x = random.randrange(screen_size[0])
        random_y = random.randrange(screen_size[1])
        
        if random_x > random_y:
            random_y = 0
        elif random_x == random_y:
            random_y = screen_size[1]
        elif random_y > random_x:
            random_x = 0
        
        self.x = random_x
        self.y = random_y

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, screen, angle) -> None:
        super().__init__()
        self.speed = 5
        self.angle = angle
        self.screen_w = screen[0]
        self.screen_h = screen[1]
        self.image = pygame.Surface((20,20))
        self.image.fill((225, 0, 0))
        self.rect = self.image.get_rect(center = (pos_x, pos_y))

    def update(self) -> None:
        self.rect.x += math.cos(self.angle) * self.speed
        self.rect.y += math.sin(self.angle) * self.speed

        if self.rect.x >= self.screen_w:
            self.kill()
        if self.rect.y >= self.screen_h:
            self.kill()

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
        bullet_group = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()
        for _ in range(4):
            enemy = Enemy((self.screen_width, self.screen_heigth))
            enemy_group.add(enemy)
        player_group.add(player)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    bullet_group.add(player.create_bullet())

            self.screen.fill('black')
            if pygame.sprite.spritecollide(player, enemy_group, True): self.running = False
            killed = pygame.sprite.groupcollide(enemy_group, bullet_group, True, True)
            if killed:
                print('yheaa')
            bullet_group.draw(self.screen)
            player_group.draw(self.screen)
            enemy_group.draw(self.screen)
            enemy_group.update(player)
            bullet_group.update()
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    Controller().start()