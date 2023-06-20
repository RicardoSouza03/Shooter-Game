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
        self.is_left = False
        self.screen = (screen_size[0], screen_size[1])
        self.original_image = pygame.image.load('sprites/characters/Player_idle.png').convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (80,80))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def throw_animation(self):
        is_cliked = pygame.mouse.get_pressed()[0]
        if is_cliked:
            self.original_image = pygame.image.load('sprites/characters/Player_throw.png').convert_alpha()
            self.original_image = pygame.transform.scale(self.original_image, (80,80))
        elif not is_cliked:
            self.original_image = pygame.image.load('sprites/characters/Player_idle.png').convert_alpha()
            self.original_image = pygame.transform.scale(self.original_image, (80,80))

    def create_bullet(self):
        mouse_pos = pygame.mouse.get_pos()
        angle = get_angle_between((self.x, self.y), mouse_pos)
        return Bullet(self.x, self.y, self.screen, angle)

    def update(self):
        mouse_x, _ = pygame.mouse.get_pos()
        if mouse_x <= self.x: self.is_left = True
        elif mouse_x > self.x: self.is_left = False
        self.image = pygame.transform.flip(self.original_image, self.is_left, False)
        self.throw_animation()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_size) -> None:
        super().__init__()
        self.spawn(screen_size)
        self.screen_size = screen_size
        self.speed = 1
        self.original_image = pygame.image.load('sprites/characters/enemie.png').convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (40,40))
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
        random_z = random.randint(0, 1)

        if random_x > random_y and random_z == 0:
            random_y = 0
        elif random_y > random_x and random_z == 0:
            random_x = 0
        elif random_x > random_y and random_z == 1:
            random_y = screen_size[1]
        elif random_y > random_x and random_z == 1:
            random_x = screen_size[0]
        else:
            random_y = screen_size[1]
        
        self.x = random_x
        self.y = random_y

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, screen, angle) -> None:
        super().__init__()
        self.speed = 8
        self.angle = angle
        self.screen_w = screen[0]
        self.screen_h = screen[1]
        self.original_image = pygame.image.load('sprites/Bullet.png')
        self.image = pygame.transform.scale(self.original_image, (40,40))
        self.rect = self.image.get_rect(center = (pos_x, pos_y))

    def update(self):
        self.rect.x += math.cos(self.angle) * self.speed
        self.rect.y += math.sin(self.angle) * self.speed

        if self.rect.x >= self.screen_w or self.rect.x < -20:
            self.kill()
            return True
        if self.rect.y >= self.screen_h or self.rect.y < -20:
            self.kill()
            return True

class Controller():
    def __init__(self) -> None:
        self.running = True
        self.clock = pygame.time.Clock()
        self.screen_width = 600
        self.screen_heigth = 800
        self.score = 0
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_heigth))

    def create_enemy(self, enemy_group):
        enemy = Enemy((self.screen_width, self.screen_heigth))
        enemy_group.add(enemy)

    def change_cursor(self):
        image = pygame.image.load('sprites/cross hair.png').convert_alpha()
        self.cursor = pygame.transform.scale(image, (40, 40))

    def display_score(self):
        font = pygame.font.Font('sprites/Planes_ValMore.ttf', 60)
        text_surface = font.render(str(self.score), False, 'White')
        self.screen.blit(text_surface, (self.screen_width-160, 20))

    def set_background(self):
        img_01 = pygame.transform.scale(pygame.image.load('sprites/background/sky.png').convert_alpha(), (self.screen_width, self.screen_heigth))
        img_02 = pygame.transform.scale(pygame.image.load('sprites/background/moon.png').convert_alpha(), (self.screen_width, 324))
        img_03 = pygame.transform.scale(pygame.image.load('sprites/background/clouds_front.png').convert_alpha(), (self.screen_width, 324))
        img_04 = pygame.transform.scale(pygame.image.load('sprites/background/clouds_back.png').convert_alpha(), (self.screen_width, 324))
        img_05 = pygame.transform.scale(pygame.image.load('sprites/background/Spaceship.png').convert_alpha(), (45, 45))
        img_05 = pygame.transform.flip(img_05, False, True)
        self.screen.blit(img_01, (0, 0))
        self.screen.blit(img_02, (0, 0))
        self.screen.blit(img_05, (self.screen_width/2-25, self.screen_heigth/2+18))
        self.screen.blit(img_03, (0, self.screen_heigth/2+75))
        self.screen.blit(img_04, (0, self.screen_heigth/2+75))

    def start(self):
        pygame.init()
        pygame.display.set_caption("Shooter game")
        pygame.mouse.set_visible(False)
        self.change_cursor()

        player = Player((self.screen_width, self.screen_heigth))
        player_group = pygame.sprite.Group()
        bullet_group = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()

        for _ in range(4):
            self.create_enemy(enemy_group)
        player_group.add(player)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    bullet_group.add(player.create_bullet())

            if self.score <= 0: self.score = 0
            self.set_background()

            if pygame.sprite.spritecollide(player, enemy_group, True): self.running = False
            if pygame.sprite.groupcollide(enemy_group, bullet_group, True, True):
                self.score += 10
                self.create_enemy(enemy_group)

            bullet_group.draw(self.screen)
            player_group.draw(self.screen)
            enemy_group.draw(self.screen)
            self.screen.blit(self.cursor, pygame.mouse.get_pos())
            enemy_group.update(player)
            player_group.update()

            for bullet in bullet_group.sprites():
                if bullet.update():
                    self.score -= 20

            self.display_score()
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    Controller().start()