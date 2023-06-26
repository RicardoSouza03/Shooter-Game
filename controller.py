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
        self.life = 1
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
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_size, enemy_level) -> None:
        super().__init__()
        self.enemy_randomizer(enemy_level)
        self.spawn(screen_size)
        self.screen_size = screen_size
        self.speed = 1
        self.image = pygame.transform.scale(self.original_image, (40,40))
        self.explosion_list = []
        for i in range(1,4):
            img = pygame.image.load(f'sprites/pop_0{i + 1}.png').convert_alpha()
            img = pygame.transform.scale(img, (40,40))
            self.explosion_list.append(img)
        self.explosion_index = 0
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.frame_counter = 0

    def update(self, player):
        # Move enemy towards player.
        direction_x, direction_y = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        distance = math.hypot(direction_x, direction_y)
        direction_x, direction_y = direction_x / distance, direction_y / distance
        self.rect.x += direction_x * self.speed
        self.rect.y += direction_y * self.speed

        self.frame_counter += 1

        if self.life <= 0:
            if self.explosion_animation():
                self.kill()

    def explosion_animation(self):
        explosion_speed = 1

        if self.frame_counter >= explosion_speed and self.explosion_index < len(self.explosion_list) - 1:
            self.frame_counter = 0
            self.explosion_index += 1
            self.image = self.explosion_list[self.explosion_index]

        if self.explosion_index >= len(self.explosion_list) - 1 and self.frame_counter >= explosion_speed:
            return True

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

class Button():
    def __init__(self, x, y, image) -> None:
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, screen):
        action = False

        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

class Controller():
    def __init__(self) -> None:
        self.running = True
        self.paused = False
        self.level = 1
        self.lost = False
        self.enemy_count = 4
        self.clock = pygame.time.Clock()
        self.screen_width = 600
        self.screen_heigth = 800
        self.score = 0
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_heigth))
        self.player = Player((self.screen_width, self.screen_heigth))

    def create_enemy(self, enemy_group):
        enemy = Enemy((self.screen_width, self.screen_heigth), self.level)
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

    def pause(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_ESCAPE] and self.paused == False:
            self.paused = True
        
    def display_pause_menu(self, groups):
        return_btn_img = pygame.transform.scale(pygame.image.load('sprites/buttons/return_button.png').convert_alpha(), (180, 50))
        exit_btn_img = pygame.transform.scale(pygame.image.load('sprites/buttons/exit_button.png').convert_alpha(), (140, 50))
        try_again_btn_img = pygame.transform.scale(pygame.image.load('sprites/buttons/newGame_button.png').convert_alpha(), (180, 50))
        return_btn = Button(self.screen_width/2-100, self.screen_heigth/2-50, return_btn_img)
        exit_btn = Button(self.screen_width/2-100, self.screen_heigth/2+20, exit_btn_img)
        try_again_btn = Button(self.screen_width/2-100, self.screen_heigth/2-50, try_again_btn_img)
        
        if self.lost:
            if try_again_btn.draw(self.screen): self.reset_game(groups)
            if exit_btn.draw(self.screen): self.running = False
        else:
            if return_btn.draw(self.screen): self.paused = False
            if exit_btn.draw(self.screen): self.running = False

    def reset_game(self, groups):
        self.player = Player((self.screen_width, self.screen_heigth))
        groups[0].empty()
        groups[1].add(self.player)
        groups[2].empty()
        self.score = 0
        self.level = 1
        self.lost = False
        self.enemy_count = 4
        self.paused = False

    def difficult_handler(self):
        if self.score >= 1000: 
            self.level = 2
            self.enemy_count = 6
        if self.score >= 2800:
            self.level = 3
            self.enemy_count = 7

    def start(self):
        pygame.init()
        pygame.display.set_caption("Shooter game")
        pygame.mouse.set_visible(False)
        self.change_cursor()

        player_group = pygame.sprite.Group()
        bullet_group = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()

        player_group.add(self.player)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and not self.paused:
                    bullet_group.add(self.player.create_bullet())

            self.set_background()
            self.difficult_handler()
            if not self.paused:
                if self.score <= 0: self.score = 0
                self.pause()

                if len(enemy_group) < self.enemy_count:
                    self.create_enemy(enemy_group)

                if pygame.sprite.spritecollide(self.player, enemy_group, False): 
                    self.player.life -= 1
                    self.clock.tick(40)
                    if len(player_group) <= 0:
                        self.lost = True
                        self.paused = True
                bullet_collied_enemy = pygame.sprite.groupcollide(enemy_group, bullet_group, False, True)
                if bullet_collied_enemy:
                    enemy_hit = bullet_collied_enemy.popitem()[0]
                    enemy_hit.life -= 1
                    self.score += 10

                bullet_group.draw(self.screen)
                player_group.draw(self.screen)
                enemy_group.draw(self.screen)
                enemy_group.update(self.player)
                player_group.update()

                for bullet in bullet_group.sprites():
                    if bullet.update():
                        self.score -= 20

                self.display_score()
       
            elif self.paused == True:
                self.display_pause_menu([enemy_group, player_group, bullet_group])

            self.screen.blit(self.cursor, pygame.mouse.get_pos())

            pygame.display.flip()
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    Controller().start()