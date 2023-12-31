import pygame, math, random
from utils.angle_between import get_angle_between
from utils.animation import Animation

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_size) -> None:
        super().__init__()
        self.x = screen_size[0]/2
        self.y = screen_size[1]/2
        self.is_left = False
        self.life = 1
        self.death_animation = Animation((60,70), 'sprites/characters/death_0', 8)
        self.screen = (screen_size[0], screen_size[1])
        self.original_image = pygame.image.load('sprites/characters/Player_idle.png').convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (60,70))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def throw_animation(self):
        is_cliked = pygame.mouse.get_pressed()
        if is_cliked[0] or is_cliked[1] or is_cliked[2]:
            self.original_image = pygame.image.load('sprites/characters/Player_throw.png').convert_alpha()
            self.original_image = pygame.transform.scale(self.original_image, (55,70))
        elif not (is_cliked[0] or is_cliked[1] or is_cliked[2]):
            self.original_image = pygame.image.load('sprites/characters/Player_idle.png').convert_alpha()
            self.original_image = pygame.transform.scale(self.original_image, (60,70))

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

        if self.life <= 0:
            self.death_animation.update()
            self.image = self.death_animation.image
            if self.death_animation.ended == True:
                self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_size, enemy_level) -> None:
        super().__init__()
        self.enemy_randomizer(enemy_level)
        self.spawn(screen_size)
        self.screen_size = screen_size
        self.speed = 1
        self.image = pygame.transform.scale(self.original_image, (40,40))
        self.explosion_animation = Animation((40,40), 'sprites/pop_0', 4)
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def update(self, player):
        # Move enemy towards player.
        direction_x, direction_y = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        distance = math.hypot(direction_x, direction_y)
        direction_x, direction_y = direction_x / distance, direction_y / distance
        self.rect.x += direction_x * self.speed
        self.rect.y += direction_y * self.speed

        if self.life <= 0:
            self.explosion_animation.update()
            self.image = self.explosion_animation.image
            if self.explosion_animation.ended == True:
                self.kill()

    def enemy_randomizer(self, enemy_level: int):
        random_level = random.randint(1, enemy_level)
        if enemy_level == 1: random_level = 1
        enemy_by_level = {1: 'sprites/characters/enemie.png', 2: 'sprites/characters/enemie2.png', 3: 'sprites/characters/enemie3.png'}
        self.original_image = pygame.image.load(enemy_by_level[random_level]).convert_alpha()
        self.life = random_level

    def spawn(self, screen_size):
        # Sets enemy position at a random position on screen.
        random_x = random.randrange(screen_size[0])
        random_y = random.randrange(screen_size[1])
        random_z = random.randint(0, 1)

        # Apply spawn rules to enemy be spawned outside screen
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