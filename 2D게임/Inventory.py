from pico2d import *


def color(data):
    return clamp(0, data, 255)

class inventory:

    def __init__(self):
        self.image = load_image('ui\\inventory.png')
        self.font = load_font('font\\godoMaum.ttf', 50)
        self.item = {'fire_arrow': 255, 'ice_arrow': 100, 'arrow': 100, 'powder': 100, 'bomb': 100, 'water': 100, 'fire': 100, 'poison': 100}
        pass

    def insert(self, data):
        self.item[data] += 1

    def pop(self, data):
        if self.item[data] > 0:
            self.item[data] -= 1
            return True
        else:
            return False

    def update(self):
        pass

    def draw(self):

        self.image.draw(900, 300)
        self.font.draw(900, 570, ' %3d' % self.item['fire_arrow'], (color(255 - self.item['fire_arrow']), 0, 0))
        self.font.draw(900, 520, ' %3d' % self.item['ice_arrow'], (color(255 - self.item['ice_arrow']), 0, 0))
        self.font.draw(900, 470, ' %3d' % self.item['arrow'], (color(255 - self.item['arrow']), 0, 0))
        self.font.draw(900, 420, ' %3d' % self.item['powder'], (color(255 - self.item['powder']), 0, 0))
        self.font.draw(900, 370, ' %3d' % self.item['bomb'], (color(255 - self.item['bomb']), 0, 0))
        self.font.draw(900, 320, ' %3d' % self.item['water'], (color(255 - self.item['water']), 0, 0))
        self.font.draw(900, 270, ' %3d' % self.item['fire'], (color(255 - self.item['fire']), 0, 0))
        self.font.draw(900, 220, ' %3d' % self.item['poison'], (color(255 - self.item['poison']), 0, 0))
        pass

    def handle_event(self, event):
        pass

