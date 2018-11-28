from pico2d import *


def color(data):
    return clamp(0, data, 255)

class inventory:

    def __init__(self):
        self.image = load_image('ui\\inventory.png')
        self.font = load_font('font\\godoMaum.ttf', 50)
        self.item = {'fire_arrow': 0, 'ice_arrow': 0, 'arrow': 0, 'sector_form_arrow': 0}

    def insert(self, data):
        self.item[data] += 1

    def pop(self, data):
        if data != 'arrow':
            self.item['arrow'] -= 10
        if self.item[data] > 0:
            self.item[data] -= 1
            return True
        else:
            self.item['arrow'] += 10
            if self.item['arrow'] == 10:
                self.item['arrow'] = 0
            return False

    def update(self):
        pass

    def draw(self):
        self.image.draw(900, 300)
        self.font.draw(900, 570, ' %3d' % self.item['fire_arrow'], (color(255 - self.item['fire_arrow']), 0, 0))
        self.font.draw(900, 520, ' %3d' % self.item['ice_arrow'], (color(255 - self.item['ice_arrow']), 0, 0))
        self.font.draw(900, 470, ' %3d' % self.item['arrow'], (color(255 - self.item['arrow']), 0, 0))
        pass

    def handle_event(self, event):
        pass

