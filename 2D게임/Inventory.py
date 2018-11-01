
from pico2d import *


class inventory:
    def __init__(self):
        self.image = load_image('inventory.png')
        pass

    def update(self):
        pass

    def draw(self):
        self.image.draw(900, 300)
        pass

    def handle_event(self, event):
        pass

