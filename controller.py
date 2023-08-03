import pygame, os
from entities import Player, Enemy, Spaceship
from utils.button import Button
from utils.Menu_section import MenuOptionsSection
from utils.load_image import load_image
from utils.display_text import display_text
 
class Controller():
    def __init__(self) -> None:
        self.running = True
        self.main_menu = True
        self.paused = False
        self.options = False
        self.level = 1
        self.enemy_count = 4
        self.clock = pygame.time.Clock()
        self.score = 0
        self.player_skin = 'Rodolfo'
        self.spaceship_skin = 'Fighter'

    def load_game_features(self):
        self.player = Player((self.screen_width, self.screen_heigth), self.player_skin)
        self.spaceship = Spaceship((self.screen_width, self.screen_heigth), self.spaceship_skin)
        
        shop_characters_path = 'sprites/shop_images/characters/'
        best_score = int(self.best_score(0))
        characters_shop_dict = {
            'Rodolfo': {
                'price': 0,
                'image_path': f'{shop_characters_path}Rodolfo_character.png',
                'image': load_image(f'{shop_characters_path}Rodolfo_character.png', True, (80, 80)),
                'image_locked': None,
                'coordinate_x': 80,
                'coordinate_y': 200,
            },
            'Pink': {
                'price': 3600,
                'image_path': f'{shop_characters_path}Pink_character.png',
                'image': load_image(f'{shop_characters_path}Pink_character.png', True, (80, 80)),
                'image_locked': load_image(f'{shop_characters_path}Pink_character_locked.png', True, (100, 100)),
                'coordinate_x': 205,
                'coordinate_y': 200,
            },
            'Yeti': {
                'price': 4500,
                'image_path': f'{shop_characters_path}Yeti_character.png',
                'image': load_image(f'{shop_characters_path}Yeti_character.png', True, (80, 80)),
                'image_locked': load_image(f'{shop_characters_path}Yeti_character_locked.png', True, (100, 100)),
                'coordinate_x': 325,
                'coordinate_y': 200,
            }
        }
        self.player_skin_section = MenuOptionsSection(characters_shop_dict, self.player_skin, self.screen, best_score)

        shop_spaceships_path = 'sprites/shop_images/spaceships/'
        spaceship_shop_dict = {
            'Fighter': {
                'price': 0,
                'image_path': f'{shop_spaceships_path}Fighter.png',
                'image': load_image(f'{shop_spaceships_path}Fighter.png', True, (80, 80)),
                'image_locked': load_image(f'{shop_spaceships_path}Fighter_locked.png', True, (100, 100)),
                'coordinate_x': 80,
                'coordinate_y': 400,
            },
            'Scout': {
                'price': 2780,
                'image_path': f'{shop_spaceships_path}Scout.png',
                'image': load_image(f'{shop_spaceships_path}Scout.png', True, (80, 80)),
                'image_locked': load_image(f'{shop_spaceships_path}Scout_locked.png', True, (100, 100)),
                'coordinate_x': 205,
                'coordinate_y': 400,
            },
            'Battlecruiser': {
                'price': 3500,
                'image_path': f'{shop_spaceships_path}Battlecruiser.png',
                'image': load_image(f'{shop_spaceships_path}Battlecruiser.png', True, (80, 80)),
                'image_locked': load_image(f'{shop_spaceships_path}Battlecruiser_locked.png', True, (100, 100)),
                'coordinate_x': 325,
                'coordinate_y': 400,
            },
            'Dreadnought': {
                'price': 4230,
                'image_path': f'{shop_spaceships_path}Dreadnought.png',
                'image': load_image(f'{shop_spaceships_path}Dreadnought.png', True, (80, 80)),
                'image_locked': load_image(f'{shop_spaceships_path}Dreadnought_locked.png', True, (105, 105)),
                'coordinate_x': 450,
                'coordinate_y': 400,
            },
        }
        self.spaceship_skin_section = MenuOptionsSection(spaceship_shop_dict, self.spaceship_skin, self.screen, best_score)

    def create_enemy(self, enemy_group):
        enemy = Enemy((self.screen_width, self.screen_heigth), self.level)
        enemy_group.add(enemy)

    def get_screen_size(self):
        desktop_sizes = pygame.display.get_desktop_sizes()
        screensize = desktop_sizes[0]

        if screensize > (1100, 1000):
            self.screen_width, self.screen_heigth = (600, 800)
        elif (820, 914) < screensize <= (1100, 1000):
            self.screen_width, self.screen_heigth = (600, screensize[1] - 50)
        else:
            self.screen_width, self.screen_heigth = screensize

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_heigth), pygame.SCALED)

    def change_cursor(self):
        self.cursor = load_image('sprites/cross hair.png', True, (40, 40))
        win_icon = load_image('icon.ico', False)

        pygame.display.set_icon(win_icon)

    def set_background(self):
        imgs_list = os.listdir('sprites/background/')
        for image in sorted(imgs_list, reverse=True):
            if image == "sky.png": 
                scale = (self.screen_width, self.screen_heigth)
                position = (0, 0)
            else: 
                scale = (self.screen_width, 324)
                position = (0, self.screen_heigth/2+75)

            img = load_image(f'sprites/background/{image}', True, scale)
            self.screen.blit(img, position)

    def pause(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_ESCAPE] and self.paused == False:
            self.paused = True
        
    def display_pause_menu(self):
        image = load_image('sprites/buttons/exit_button.png', True, (120, 50))
        exit_button = Button(self.screen_width/2-100, self.screen_heigth/2+10, image)

        image = load_image('sprites/buttons/return_button.png', True, (200, 50))
        return_button = Button(self.screen_width/2-100, self.screen_heigth/2-50, image)

        display_text(self.screen, 'Paused', (self.screen_width/2-100, 100), 60)

        if return_button.draw(self.screen): self.paused = False
        if exit_button.draw(self.screen): self.running = False

    def display_main_menu(self, groups):
        images_path = 'sprites/buttons/'

        image = load_image(f'{images_path}newGame_button.png', True, (200, 50))
        new_game_button = Button(self.screen_width/2-100, self.screen_heigth/2-60, image)

        image = load_image(f'{images_path}options_button.png', True, (200, 50))
        options_button = Button(self.screen_width/2-100, self.screen_heigth/2, image)

        image = load_image(f'{images_path}exit_button.png', True, (120, 50))
        exit_button = Button(self.screen_width/2-100, self.screen_heigth/2+60, image)

        best_score = self.best_score(0)
        display_text(self.screen, 'Shooter Game', (self.screen_width/2-140, 100), 40)
        display_text(self.screen, f'Best score: {best_score}', (self.screen_width/2-140, 160), 40)

        if self.score > 0: display_text(self.screen, f'Run score: {self.score}', (self.screen_width/2-140, 200), 40)
        if new_game_button.draw(self.screen): self.reset_game(groups)
        if options_button.draw(self.screen): 
            self.display_options_menu()
            self.main_menu = False
            self.options = True
        if exit_button.draw(self.screen): self.running = False

    def display_options_menu(self):
        display_text(self.screen, 'Characters', (80, 140), 50)
        display_text(self.screen, 'Spaceships', (80, 340), 50)

        image = load_image('sprites/buttons/return_arrow.png', True, (40, 40))
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
        self.spaceship = Spaceship((self.screen_width, self.screen_heigth), self.spaceship_skin)
        groups[0].empty()
        groups[1].add(self.player)
        groups[2].empty()
        groups[3].add(self.spaceship)
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
        self.get_screen_size()
        self.load_game_features()
        pygame.display.set_caption("Shooter game")
        pygame.mouse.set_visible(False)
        self.change_cursor()

        player_group = pygame.sprite.Group()
        bullet_group = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()
        spaceship_group = pygame.sprite.Group()

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
                    self.spaceship.life -= 1
                if len(spaceship_group.sprites()) <= 0:
                    self.best_score(self.score)
                    self.load_game_features()
                    self.main_menu = True
                    self.paused = True
                
                bullet_collied_enemy = pygame.sprite.groupcollide(enemy_group, bullet_group, False, True)
                if bullet_collied_enemy:
                    enemy_hit = bullet_collied_enemy.popitem()[0]
                    enemy_hit.life -= 1
                    self.score += 10

                spaceship_group.draw(self.screen)
                bullet_group.draw(self.screen)
                player_group.draw(self.screen)
                enemy_group.draw(self.screen)
                enemy_group.update(self.player)
                player_group.update()
                spaceship_group.update()

                for bullet in bullet_group.sprites():
                    if bullet.update():
                        self.score -= 20

                display_text(self.screen, self.score, (self.screen_width-160, 20), 60)
       
            elif self.paused and not (self.main_menu or self.options):
                self.display_pause_menu()
            elif self.main_menu:
                self.display_main_menu([enemy_group, player_group, bullet_group, spaceship_group])
            elif self.options:
                self.screen.fill('black')
                self.display_options_menu()

            self.screen.blit(self.cursor, pygame.mouse.get_pos())

            pygame.display.flip()
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    Controller().start()