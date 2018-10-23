import random
import json
import os

from pico2d import *


class Data:

    def __init__(self):
        self.index_x, self.index_y = 0, 0
        self.item = {'arrow': 0, 'fire_arrow': 0, 'ice_arrow': 0, 'poison_arrow': 0,'water': 0, 'poison': 0, 'fire': 0, 'bomb': 0}
        self.image = load_image('inventory.png')


    def m_insert(self, item_type):
        self.item[item_type] += 1
        pass

    def m_mix(self):

        pass

    def update(self):

        pass

    def draw(self):
        self.image.draw(900, 300)
        pass