import pygame, os, ctypes
from entities import Player, Enemy
from utils.button import Button
from utils.Menu_section import MenuOptionsSection

class Controller():
    def __init__(self) -> None:
        self.running = True
        self.main_menu = True
        self.paused = False
        self.options = False
        self.level = 1
        self.enemy_count = 4
        self.clock = pygame.time.Clock()
        self.get_screen_size()
        self.score = 0
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_heigth), pygame.SCALED)
        self.player_skin = 'Rodolfo'
        self.spaceship_skin = 'Fighter'
        self.load_game_features()

    def load_game_features(self):
        self.player = Player((self.screen_width, self.screen_heigth), self.player_skin)
        
        shop_characters_path = 'sprites/shop_images/characters/'
        best_score = int(self.best_score(0))
        characters_shop_dict = {
            'Rodolfo': {
                'is_unlocked': True,
                'image': pygame.transform.scale(pygame.image.load(f'{shop_characters_path}Rodolfo_character.png').convert_alpha(), (80, 80)),
                'image_locked': None,
                'coordinate_x': 150,
                'coordinate_y': 200,
            },
            'Pink': {
                'is_unlocked': best_score >= 3600,
                'image': pygame.transform.scale(pygame.image.load(f'{shop_characters_path}Pink_character.png').convert_alpha(), (80, 80)),
                'image_locked': pygame.transform.scale(pygame.image.load(f'{shop_characters_path}Pink_character_locked.png').convert_alpha(), (80, 80)),
                'coordinate_x': 260,
                'coordinate_y': 200,
            },
            'Yeti': {
                'is_unlocked': best_score >= 4500,
                'image': pygame.transform.scale(pygame.image.load(f'{shop_characters_path}Yeti_character.png').convert_alpha(), (80, 80)),
                'image_locked': pygame.transform.scale(pygame.image.load(f'{shop_characters_path}Yeti_character_locked.png').convert_alpha(), (80, 80)),
                'coordinate_x': 370,
                'coordinate_y': 200,
            }
        }
        self.player_skin_section = MenuOptionsSection(characters_shop_dict, self.player_skin, self.screen)

        shop_spaceships_path = 'sprites/shop_images/spaceships/'
        spaceship_shop_dict = {
            'Fighter': {
                'is_unlocked': True,
                'image': pygame.transform.scale(pygame.image.load(f'{shop_spaceships_path}Fighter.png').convert_alpha(), (80, 80)),
                'image_locked': pygame.transform.scale(pygame.image.load(f'{shop_spaceships_path}Fighter.png').convert_alpha(), (80, 80)),
                'coordinate_x': 150,
                'coordinate_y': 400,
            },
            'Scout': {
                'is_unlocked': best_score >= 2780,
                'image': pygame.transform.scale(pygame.image.load(f'{shop_spaceships_path}Scout.png').convert_alpha(), (80, 80)),
                'image_locked': pygame.transform.scale(pygame.image.load(f'{shop_spaceships_path}Scout.png').convert_alpha(), (80, 80)),
                'coordinate_x': 260,
                'coordinate_y': 400,
            },
            'Battlecruiser': {
                'is_unlocked': best_score >= 3500,
                'image': pygame.transform.scale(pygame.image.load(f'{shop_spaceships_path}Battlecruiser.png').convert_alpha(), (80, 80)),
                'image_locked': pygame.transform.scale(pygame.image.load(f'{shop_spaceships_path}Battlecruiser.png').convert_alpha(), (80, 80)),
                'coordinate_x': 370,
                'coordinate_y': 400,
            },
            'Dreadnought': {
                'is_unlocked': best_score >= 4230,
                'image': pygame.transform.scale(pygame.image.load(f'{shop_spaceships_path}Dreadnought.png').convert_alpha(), (80, 80)),
                'image_locked': pygame.transform.scale(pygame.image.load(f'{shop_spaceships_path}Dreadnought.png').convert_alpha(), (80, 80)),
                'coordinate_x': 480,
                'coordinate_y': 400,
            },
        }
        self.spaceship_skin_section = MenuOptionsSection(spaceship_shop_dict, self.spaceship_skin, self.screen)


    def create_enemy(self, enemy_group):
        enemy = Enemy((self.screen_width, self.screen_heigth), self.level)
        enemy_group.add(enemy)

    def get_screen_size(self):
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        if screensize > (1366, 768):
            self.screen_width, self.screen_heigth = (600, 800)
        elif (820, 914) < screensize <= (1366, 768):
            self.screen_width, self.screen_heigth = (600, screensize[1] - 50)
        else:
            self.screen_width, self.screen_heigth = screensize

    def change_cursor(self):
        image = pygame.image.load('sprites/cross hair.png').convert_alpha()
        self.cursor = pygame.transform.scale(image, (40, 40))
        win_icon = pygame.image.load('icon.ico').convert_alpha()
        pygame.display.set_icon(win_icon)

    def display_text(self, text: str, location: tuple, font_size: int):
        font = pygame.font.Font('sprites/Planes_ValMore.ttf', font_size)
        text_surface = font.render(str(text), False, 'White')
        self.screen.blit(text_surface, location)

    def set_background(self):
        imgs_list = os.listdir('sprites/background/')
        spaceship = False
        for image in sorted(imgs_list, reverse=True):
            if image == "sky.png": 
                scale = (self.screen_width, self.screen_heigth)
                position = (0, 0)
            elif image == "Spaceship.png":
                scale = (200, 200)
                img = pygame.transform.scale(pygame.image.load(f"sprites/shop_images/spaceships/{self.spaceship_skin}.png").convert_alpha(), scale)
                position = (self.screen_width/2-100, self.screen_heigth/2-60)
                spaceship = True
            else: 
                scale = (self.screen_width, 324)
                position = (0, self.screen_heigth/2+75)

            if spaceship:
                img = pygame.transform.flip(img, False, True)
            else:
                img = pygame.transform.scale(pygame.image.load(f"sprites/background/{image}").convert_alpha(), scale)
            self.screen.blit(img, position)

    def pause(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_ESCAPE] and self.paused == False:
            self.paused = True
        
    def display_pause_menu(self):
        image = pygame.transform.scale(pygame.image.load(f'sprites/buttons/exit_button.png').convert_alpha(), (120, 50))
        exit_button = Button(self.screen_width/2-100, self.screen_heigth/2+10, image)
        image = pygame.transform.scale(pygame.image.load(f'sprites/buttons/return_button.png').convert_alpha(), (200, 50))
        return_button = Button(self.screen_width/2-100, self.screen_heigth/2-50, image)

        self.display_text('Paused', (self.screen_width/2-100, 100), 60)
        if return_button.draw(self.screen): self.paused = False
        if exit_button.draw(self.screen): self.running = False

    def display_main_menu(self, groups):
        image = pygame.transform.scale(pygame.image.load(f'sprites/buttons/newGame_button.png').convert_alpha(), (200, 50))
        new_game_button = Button(self.screen_width/2-100, self.screen_heigth/2-60, image)
        image = pygame.transform.scale(pygame.image.load(f'sprites/buttons/options_button.png').convert_alpha(), (200, 50))
        options_button = Button(self.screen_width/2-100, self.screen_heigth/2, image)
        image = pygame.transform.scale(pygame.image.load(f'sprites/buttons/exit_button.png').convert_alpha(), (120, 50))
        exit_button = Button(self.screen_width/2-100, self.screen_heigth/2+60, image)

        self.display_text('Shooter Game', (self.screen_width/2-140, 100), 40)
        best_score = self.best_score(self.score)
        self.display_text(f'Best score: {best_score}', (self.screen_width/2-140, 160), 40)
        if self.score > 0: self.display_text(f'Run score: {self.score}', (self.screen_width/2-140, 200), 40)
        if new_game_button.draw(self.screen): self.reset_game(groups)
        if options_button.draw(self.screen): 
            self.display_options_menu()
            self.main_menu = False
            self.options = True
        if exit_button.draw(self.screen): self.running = False

    def display_options_menu(self):
        self.display_text('Characters', (150, 140), 50)
        self.display_text('Spaceships', (150, 340), 50)

        image = pygame.transform.scale(pygame.image.load(f'sprites/buttons/return_arrow.png').convert_alpha(), (40, 40))
        return_arrow_button = Button(25, 30, image)

        if return_arrow_button.draw(self.screen):
            self.options = False
            self.main_menu = True

        self.player_skin_section.draw_menu()
        self.spaceship_skin_section.draw_menu()
        self.player_skin = self.player_skin_section.current_skin
        self.spaceship_skin = self.spaceship_skin_section.current_skin

    def reset_game(self, groups):
        pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
        self.player = Player((self.screen_width, self.screen_heigth), self.player_skin)
        groups[0].empty()
        groups[1].add(self.player)
        groups[2].empty()
        self.score = 0
        self.level = 1
        self.main_menu, self.paused, self.options = False, False, False
        self.enemy_count = 4

    def difficult_handler(self):
        if self.score >= 1000: 
            self.level = 2
            self.enemy_count = 6
        if self.score >= 2800:
            self.level = 3
            self.enemy_count = 7
        if self.score >= 3400:
            self.level = 4
            self.enemy_count = 8
        if self.score >= 4250:
            self.level = 5
            self.enemy_count = 6

    def best_score(self, new_score):
        with open('best_score.txt', mode='r+') as txt:
            best_score = txt.readline()
            if new_score and int(new_score) > int(best_score):
                txt.seek(0)
                txt.truncate()
                txt.write(str(new_score))
                return str(new_score)
            else:
                return str(best_score)

    def start(self):
        pygame.init()
        pygame.display.set_caption("Shooter game")
        pygame.mouse.set_visible(False)
        self.change_cursor()

        player_group = pygame.sprite.Group()
        bullet_group = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and not self.paused:
                    bullet_group.add(self.player.create_bullet())

            self.set_background()
            self.difficult_handler()
            if not self.paused and not (self.main_menu or self.options):
                if self.score <= 0: self.score = 0
                self.pause()

                if len(enemy_group) < self.enemy_count:
                    self.create_enemy(enemy_group)

                if pygame.sprite.spritecollide(self.player, enemy_group, False):
                    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                    self.clock.tick(20)
                    self.player.life -= 1
                if len(player_group.sprites()) <= 0:
                    self.main_menu = True
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

                self.display_text(self.score, (self.screen_width-160, 20), 60)
       
            elif self.paused and not (self.main_menu or self.options):
                self.display_pause_menu()
            elif self.main_menu:
                self.display_main_menu([enemy_group, player_group, bullet_group])
            elif self.options:
                self.screen.fill('black')
                self.display_options_menu()

            self.screen.blit(self.cursor, pygame.mouse.get_pos())

            pygame.display.flip()
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    Controller().start()