import pygame, math, random
from utils.angle_between import get_angle_between
from utils.animation import Animation
from utils.load_image import load_image

player_skins_dict = {
    'Rodolfo': {
        'Idle': { 'sheet': 'sprites/characters/blue_character/Idle_sheet.png', 'steps': 4, 'speed': 150, 'width': 18, 'height': 28, 'scale': 3, 'loop': True },
        'Throw': { 'sheet': 'sprites/characters/blue_character/Throw_sheet.png', 'steps': 4, 'speed': 30, 'width': 19, 'height': 28, 'scale': 3, 'loop': False },
        'Death': { 'sheet': 'sprites/characters/blue_character/Death_sheet.png', 'steps': 7, 'speed': 95, 'width': 35, 'height': 28, 'scale': 3, 'loop': False },
    },
    'Pink': {
        'Idle': { 'sheet': 'sprites/characters/pink_character/Idle_sheet.png', 'steps': 4, 'speed': 150, 'width': 20, 'height': 29, 'scale': 3, 'loop': True },
        'Throw': { 'sheet': 'sprites/characters/pink_character/Throw_sheet.png', 'steps': 4, 'speed': 30, 'width': 20, 'height': 28, 'scale': 3, 'loop': False },
        'Death': { 'sheet': 'sprites/characters/pink_character/Death_sheet.png', 'steps': 7, 'speed': 95, 'width': 35, 'height': 29, 'scale': 3, 'loop': False },
    },
    'Yeti': {
        'Idle': { 'sheet': 'sprites/characters/yeti_character/Idle_sheet.png', 'steps': 4, 'speed': 150, 'width': 22, 'height': 28, 'scale': 3, 'loop': True },
        'Throw': { 'sheet': 'sprites/characters/yeti_character/Throw_sheet.png', 'steps': 4, 'speed': 30, 'width': 22, 'height': 28, 'scale': 3, 'loop': False },
        'Death': { 'sheet': 'sprites/characters/yeti_character/Death_sheet.png', 'steps': 7, 'speed': 95, 'width': 35, 'height': 28, 'scale': 3, 'loop': False },
    },
}

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_size, skin_name) -> None:
        super().__init__()
        self.x = screen_size[0]/2
        self.y = screen_size[1]/2
        self.life = 1
        self.animations = {}
        for character_action in player_skins_dict[skin_name]:
            act = player_skins_dict[skin_name][character_action]
            self.animations[character_action] = Animation(act['sheet'],act['steps'],act['speed'],act['width'],act['height'],act['scale'],act['loop'])
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

spaceship_skins_dict = {
    "Battlecruiser": {
        "dimension": (216, 270),
        "explosion": { 'sheet': 'sprites/spaceships/battlecruiser/explosion_sheet.png', 'speed': 95, 'steps':13, 'width': 72, 'height': 90, 'scale': 3, 'loop': False }
    },
    "Dreadnought": {
        "dimension": (216, 300),
        "explosion": { 'sheet': 'sprites/spaceships/dreadnought/explosion_sheet.png', 'speed': 95, 'steps':13, 'width': 72, 'height': 100, 'scale': 3, 'loop': False }
    },
    "Fighter": {
        "dimension": (174, 126),
        "explosion": { 'sheet': 'sprites/spaceships/fighter/explosion_sheet.png', 'speed': 95, 'steps':9, 'width': 58, 'height': 42, 'scale': 3, 'loop': False }
    },
    "Scout": {
        "dimension": (150, 120),
        "explosion": { 'sheet': 'sprites/spaceships/scout/explosion_sheet.png', 'speed': 95, 'steps':10, 'width': 50, 'height': 40, 'scale': 3, 'loop': False }
    },
}


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, screen_size: tuple, skin_name) -> None:
        super().__init__()
        self.x = (screen_size[0]/2)
        self.y = (screen_size[1]/2+40)
        self.life = 1
        self.animations = {}
        for ship_action in spaceship_skins_dict[skin_name]:
            if ship_action == 'dimension':
                ...
            else:
                act = spaceship_skins_dict[skin_name][ship_action]
                self.animations[ship_action] = Animation(act['sheet'],act['steps'],act['speed'],act['width'],act['height'],act['scale'],act['loop'])
        self.explosion_animation = self.animations['explosion']
        self.image = pygame.transform.flip(load_image(f'sprites/spaceships/{skin_name}/{skin_name}.png', True, spaceship_skins_dict[skin_name]['dimension']), False, True)
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def update(self) -> None:
        if self.life <= 0:
            self.explosion_animation.update()
            self.image = pygame.transform.flip(self.explosion_animation.image, False, True).convert_alpha()
            self.explosion_animation.set_reset(False)
            if self.explosion_animation.ended:
                self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_size, enemy_level) -> None:
        super().__init__()
        self.enemy_randomizer(enemy_level)
        self.spawn(screen_size)
        self.screen_size = screen_size
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
        enemy_by_level = {
            1: {'path': f'{img_folder_path}enemie.png', 'life': 1, 'speed': 1 },
            2: {'path': f'{img_folder_path}enemie2.png', 'life': 2, 'speed': 1 },
            3: {'path': f'{img_folder_path}enemie3.png', 'life': 3, 'speed': 1 },
            4: {'path': f'{img_folder_path}enemie4.png', 'life': 1, 'speed': 2 },
            5: {'path': f'{img_folder_path}enemie5.png', 'life': 4, 'speed': 1 },
        }
        self.original_image = pygame.image.load(enemy_by_level[random_level]['path']).convert_alpha()
        self.life = enemy_by_level[random_level]['life']
        self.speed = enemy_by_level[random_level]['speed']

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