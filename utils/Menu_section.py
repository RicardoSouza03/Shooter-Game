import pygame
from utils.button import Button
from utils.load_image import load_image

class MenuOptionsSection():
    def __init__(self, menu_dict, curr_skin, screen):
        self.menu_dict = menu_dict
        self.screen = screen
        self.current_skin = curr_skin

    def change_selected_skin(self):
        for character in self.menu_dict:
            if character == self.current_skin:
                self.menu_dict[character]['image'] = load_image(self.menu_dict[character]['image_path'], True, (115, 115))
            else:
                self.menu_dict[character]['image'] = load_image(self.menu_dict[character]['image_path'], True, (105, 105))

    def create_dict_buttons(self):
        buttons_list = []
        for key in self.menu_dict:
            self.change_selected_skin()

            if self.menu_dict[key]['is_unlocked']:
                key_button = Button(self.menu_dict[key]['coordinate_x'], self.menu_dict[key]['coordinate_y'], self.menu_dict[key]['image'])
            else:
                key_button = Button(self.menu_dict[key]['coordinate_x'], self.menu_dict[key]['coordinate_y'], self.menu_dict[key]['image_locked'])

            buttons_list.append({'skin_name': key, 'button': key_button, 'is_enabled': self.menu_dict[key]['is_unlocked']})
        return buttons_list
    
    def draw_buttons(self):
        buttons_list = self.create_dict_buttons()
        for button in buttons_list:
            if button['button'].draw(self.screen) and button['is_enabled']:
                self.current_skin = button['skin_name']
        
    def draw_menu(self):
        self.draw_buttons()