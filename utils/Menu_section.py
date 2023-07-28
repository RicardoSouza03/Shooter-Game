from utils.button import Button
from utils.load_image import load_image
from utils.display_text import display_text

class MenuOptionsSection():
    def __init__(self, menu_dict, curr_skin, screen, best_score):
        self.menu_dict = menu_dict
        self.screen = screen
        self.current_skin = curr_skin
        self.best_score = best_score

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

            if self.best_score >= self.menu_dict[key]['price']:
                key_button = Button(self.menu_dict[key]['coordinate_x'], self.menu_dict[key]['coordinate_y'], self.menu_dict[key]['image'])
                price_text_info = {'text': '', 'coordinate': (0,0), 'font_size': 0}
            else:
                key_button = Button(self.menu_dict[key]['coordinate_x'], self.menu_dict[key]['coordinate_y'], self.menu_dict[key]['image_locked'])
                price_text_info = {
                    'text': self.menu_dict[key]['price'], 
                    'coordinate': (self.menu_dict[key]['coordinate_x']+ 30, self.menu_dict[key]['coordinate_y']+105), 
                    'font_size': 30
                }

            buttons_list.append({'skin_name': key, 'button': key_button, 'is_enabled': self.best_score >= self.menu_dict[key]['price'], 'price_text': price_text_info})
        return buttons_list
    
    def draw_buttons(self):
        buttons_list = self.create_dict_buttons()
        for button in buttons_list:
            if button['is_enabled']:
                if button['button'].draw(self.screen):
                    self.current_skin = button['skin_name']
            else:
                button['button'].draw(self.screen)
                display_text(self.screen, button['price_text']['text'], button['price_text']['coordinate'], button['price_text']['font_size'])
        
    def draw_menu(self):
        self.draw_buttons()