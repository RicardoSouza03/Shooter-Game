import pygame, os
from entities import Player, Enemy
from utils.button import Button

class Controller():
    def __init__(self) -> None:
        self.running = True
        self.paused = False
        self.main_menu = True
        self.level = 1
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
        win_icon = pygame.image.load('icon.ico').convert_alpha()
        pygame.display.set_icon(win_icon)

    def display_text(self, text: str, location: tuple, font_size: int):
        font = pygame.font.Font('sprites/Planes_ValMore.ttf', font_size)
        text_surface = font.render(str(text), False, 'White')
        self.screen.blit(text_surface, location)

    def set_background(self):
        imgs_list = os.listdir('sprites/background/')
        reversed_img = False
        for image in sorted(imgs_list, reverse=True):
            if image == "sky.png": 
                scale = (self.screen_width, self.screen_heigth)
                position = (0, 0)
            elif image == "Spaceship.png":
                scale = (45, 45)
                position = (self.screen_width/2-25, self.screen_heigth/2+18)
                reversed_img = True
            else: 
                scale = (self.screen_width, 324)
                position = (0, self.screen_heigth/2+75)

            if reversed_img:
                img = pygame.transform.scale(pygame.image.load(f"sprites/background/{image}").convert_alpha(), scale)
                img = pygame.transform.rotate(img, 180)
            else:
                img = pygame.transform.scale(pygame.image.load(f"sprites/background/{image}").convert_alpha(), scale)
            self.screen.blit(img, position)

    def pause(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_ESCAPE] and self.paused == False:
            self.paused = True
        
    def display_pause_menu(self, groups):
        buttons_list = []
        for button in os.listdir('sprites/buttons'):
            if button == 'exit_button.png': 
                image = pygame.transform.scale(pygame.image.load(f'sprites/buttons/{button}').convert_alpha(), (160, 50))
                buttons_list.append(Button(self.screen_width/2-100, self.screen_heigth/2+20, image))
            else:
                image = pygame.transform.scale(pygame.image.load(f'sprites/buttons/{button}').convert_alpha(), (200, 50))
                buttons_list.append(Button(self.screen_width/2-100, self.screen_heigth/2-50, image))
        
        if self.main_menu:
            self.display_text('Shooter Game', (self.screen_width/2-140, 100), 40)
            best_score = self.best_score(self.score)
            self.display_text(f'Best score: {best_score}', (self.screen_width/2-140, 160), 40)
            if self.score > 0: self.display_text(f'Run score: {self.score}', (self.screen_width/2-140, 200), 40)
            if buttons_list[1].draw(self.screen): self.reset_game(groups)
            if buttons_list[0].draw(self.screen): self.running = False
        else:
            self.display_text('Paused', (self.screen_width/2-100, 100), 60)
            if buttons_list[2].draw(self.screen): self.paused = False
            if buttons_list[0].draw(self.screen): self.running = False

    def reset_game(self, groups):
        pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
        self.player = Player((self.screen_width, self.screen_heigth))
        groups[0].empty()
        groups[1].add(self.player)
        groups[2].empty()
        self.score = 0
        self.level = 1
        self.main_menu, self.paused = False, False
        self.enemy_count = 4

    def difficult_handler(self):
        if self.score >= 1000: 
            self.level = 2
            self.enemy_count = 6
        if self.score >= 2800:
            self.level = 3
            self.enemy_count = 7

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
            if not self.paused and not self.main_menu:
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
       
            elif self.paused or self.main_menu:
                self.display_pause_menu([enemy_group, player_group, bullet_group])

            self.screen.blit(self.cursor, pygame.mouse.get_pos())

            pygame.display.flip()
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    Controller().start()