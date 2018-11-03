from pico2d import *


class inventory:

    def __init__(self):
        self.image = load_image('inventory.png')
        self.font = load_font('godoMaum.ttf', 50)
        self.item = {'fire_arrow': 255, 'ice_arrow': 100, 'arrow': 100, 'powder': 100, 'bomb': 100, 'water': 100, 'fire': 100, 'poison': 100}
        pass

    def insert(self, data):
        self.item[data] += 1

    def pop(self, data):
        self.item[data] -= 1

    def update(self):

        pass

    def draw(self):
        self.image.draw(900, 300)
        self.font.draw(900, 570, ' %3d' % self.item['fire_arrow'], (255 - self.item['fire_arrow'], 0,0 ))
        self.font.draw(900, 520, ' %3d' % self.item['ice_arrow'], (255, 255, 0))
        self.font.draw(900, 470, ' %3d' % self.item['arrow'], (255, 255, 0))
        self.font.draw(900, 420, ' %3d' % self.item['powder'], (255, 255, 0))
        self.font.draw(900, 370, ' %3d' % self.item['bomb'], (255, 255, 0))
        self.font.draw(900, 320, ' %3d' % self.item['water'], (255, 255, 0))
        self.font.draw(900, 270, ' %3d' % self.item['fire'], (255, 255, 0))
        self.font.draw(900, 220, ' %3d' % self.item['poison'], (255, 255, 0))
        pass

    def handle_event(self, event):
        pass

