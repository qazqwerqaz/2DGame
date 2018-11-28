from pico2d import *
import numpy as np

import game_framework


TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

FRAMES_PER_ACTION = 7
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
        self.castle_hp_image = load_image('ui\\castle_hp.png')
        self.castle_hp = 300
        self.hp_frame = 0
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
        self.castle_hp_image.clip_draw(int(self.hp_frame) * 393, 0, 393, 90,
                                                      600 + (300 - self.castle_hp)/2, 20, self.castle_hp, 20)

    def update(self):
        self.hp_frame = self.hp_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
        self.hp_frame = self.hp_frame % 7
        pass

    def attacked(self):
        self.castle_hp -= 5

