from pico2d import *
import numpy as np

def draw_Map(image, map_x, map_y, Map_type):

    x, y = 0, 0
    type = Map_type
    while type > 16:
        type = type - 16
        y += 1
    while type > 1:
        type = type - 1
        x += 1
    image.clip_draw(x * 20, y * 20, 20, 20, map_x * 20, map_y * 20)

class Grass:
    def __init__(self):
        self.image = load_image('Mdesert.png')
        self.castle_hp = 500
        with open('Map.txt', 'r') as self.file:
            self.line = np.loadtxt('Map.txt', delimiter=' ')

    def draw(self):
        map_x, map_y = 0, 0
        for i in self.line:
            for j in i:
                draw_Map(self.image, map_x, map_y, j)
                map_x = map_x + 1
            map_x = 0
            map_y = map_y +1


    def update(self):
        pass

