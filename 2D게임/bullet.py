from pico2d import *

import math
import game_world


class Bullet:

    arrow_image = None
    fire_arrow_image = None
    ice_arrow_image = None

    def __init__(self, x = 400, y = 300, velocity = 1, degreeAT = 1, data = 1):
        if Bullet.arrow_image == None:
            Bullet.arrow_image = load_image('arrow.png')
        if Bullet.fire_arrow_image == None:
            Bullet.fire_arrow_image = load_image('fire_arrow.png')
        if Bullet.ice_arrow_image == None:
            Bullet.ice_arrow_image = load_image('ice_arrow.png')
        self.x, self.y, self.velocity, self.degreeAT = x, y, velocity, degreeAT
        self.move_x, self.move_y = self.velocity * math.cos(self.degreeAT+3.141592), self.velocity * math.sin(self.degreeAT+3.141592)
        self.data = data
        self.frame = 0

    def draw(self):
        self.frame = (self.frame+1) % 5
        if self.data == 'fire_arrow':
            self.fire_arrow_image.clip_composite_draw(self.frame * 90, 0, 90, 30, self.degreeAT, '',self.x, self.y, 90, 30)
        elif self.data == 'ice_arrow':
            self.ice_arrow_image.clip_composite_draw(self.frame * 90, 0, 90, 30, self.degreeAT, '',self.x, self.y, 90, 30)
        elif self.data == 'arrow':
            self.arrow_image.rotate_draw(self.degreeAT + 3.141592, self.x, self.y)

    def update(self):
        self.x += self.move_x
        self.y += self.move_y
        if self.x < 25 or self.x > 1600 - 25:
            game_world.remove_object(self)
