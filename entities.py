import pygame, math, random
from utils.angle_between import get_angle_between
from utils.animation import Animation


skins_dict = {
    'Rodolfo': {
        'Idle': { 'sheet': 'sprites/characters/blue_character/Idle_sheet.png', 'steps': 4, 'speed': 150, 'width': 18, 'height': 28, 'scale': 3, 'loop': True },
        'Throw': { 'sheet': 'sprites/characters/blue_character/Throw_sheet.png', 'steps': 4, 'speed': 30, 'width': 19, 'height': 28, 'scale': 3, 'loop': False },
        'Death': { 'sheet': 'sprites/characters/blue_character/Death_sheet.png', 'steps': 7, 'speed': 95, 'width': 35, 'height': 28, 'scale': 3, 'loop': False },
    },
    'Yeti': {
        'Idle': { 'sheet': 'sprites/characters/yeti_character/Idle_sheet.png', 'steps': 4, 'speed': 150, 'width': 22, 'height': 28, 'scale': 3, 'loop': True },
        'Throw': { 'sheet': 'sprites/characters/yeti_character/Throw_sheet.png', 'steps': 4, 'speed': 30, 'width': 22, 'height': 28, 'scale': 3, 'loop': False },
        'Death': { 'sheet': 'sprites/characters/yeti_character/Death_sheet.png', 'steps': 7, 'speed': 95, 'width': 35, 'height': 28, 'scale': 3, 'loop': False },
    },
}

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_size, skin) -> None:
        super().__init__()
        self.x = screen_size[0]/2
        self.y = screen_size[1]/2
        self.life = 1
        self.animations = {}
        for key in skins_dict[skin]:
            self.animations[key] = Animation(
                skins_dict[skin][key]['sheet'],
                skins_dict[skin][key]['steps'],
                skins_dict[skin][key]['speed'],
                skins_dict[skin][key]['width'],
                skins_dict[skin][key]['height'],
                skins_dict[skin][key]['scale'],
                skins_dict[skin][key]['loop'],
            )
        self.idle_animation = self.animations['Idle']
        self.throw_animation = self.animations['Throw']
        self.death_animation = self.animations['Death']
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
        img_folder_path = 'sprites/characters/enemies/'
        random_level = random.randint(1, enemy_level)
        if enemy_level == 1: random_level = 1
        enemy_by_level = {1: f'{img_folder_path}enemie.png', 2: f'{img_folder_path}enemie2.png', 3: f'{img_folder_path}enemie3.png'}
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