import pygame, math, random
from utils.angle_between import get_angle_between
from utils.animation import Animation

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_size, skin_path) -> None:
        super().__init__()
        self.x = screen_size[0]/2
        self.y = screen_size[1]/2
        self.life = 1
        self.skin_path = skin_path
        self.idle_animation = Animation(f'{skin_path}/Idle_sheet.png', 4, 150, 18, 28, 3, True)
        self.throw_animation = Animation(f'{skin_path}/Throw_sheet.png', 4, 30, 19, 28, 3, False)
        self.death_animation = Animation(f'{skin_path}/Death_sheet.png', 4, 95, 35, 28, 3, False)
        self.screen = (screen_size[0], screen_size[1])
        self.image = self.idle_animation.image
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def animation_setter(self):
        is_clicked = pygame.mouse.get_pressed()
        if is_clicked[0] or is_clicked[1] or is_clicked[2]:
            self.throw_animation.update()
            self.image = self.throw_animation.image
            self.throw_animation.set_ended(False)
        else:
            self.throw_animation.set_ended(True)
            self.idle_animation.update()
            self.image = self.idle_animation.image

    def create_bullet(self):
        mouse_pos = pygame.mouse.get_pos()
        angle = get_angle_between((self.x, self.y), mouse_pos)
        return Bullet(self.x, self.y, self.screen, angle)

    def flip_player(self):
        mouse_x, _ = pygame.mouse.get_pos()

        if mouse_x <= self.x: 
            self.image = pygame.transform.flip(self.image, True, False).convert_alpha()
        elif mouse_x > self.x: 
            self.image = pygame.transform.flip(self.image, False, False).convert_alpha()

    def update(self):
        self.animation_setter()
        self.flip_player()
        
        if self.life <= 0:
            self.death_animation.update()
            self.image = self.death_animation.image
            self.flip_player()
            self.death_animation.set_reset(False)
            if self.death_animation.ended:
                self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_size, enemy_level) -> None:
        super().__init__()
        self.enemy_randomizer(enemy_level)
        self.spawn(screen_size)
        self.screen_size = screen_size
        self.speed = 1
        self.image = pygame.transform.scale(self.original_image, (40,40))
        self.explosion_animation = Animation('sprites/Pop_sheet.png', 4, 10, 40, 40, 1, False)
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
            self.explosion_animation.set_reset(False)
            if self.explosion_animation.ended:
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