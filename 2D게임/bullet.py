from pico2d import *
import time
import game_framework
import math
import game_world

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

FRAMES_PER_ACTION = 5
EFFECT_FRAMES_PER_ACTION = 6

class Bullet:

    arrow_image = None
    fire_arrow_image = None
    ice_arrow_image = None

    fire_explosion_image = None
    ice_explosion_image = None

    def __init__(self, x = 400, y = 300, velocity = 1, degreeAT = 1, data = 1):
        if Bullet.arrow_image == None:
            Bullet.arrow_image = load_image('arrow\\arrow.png')
        if Bullet.fire_arrow_image == None:
            Bullet.fire_arrow_image = load_image('arrow\\fire_arrow.png')
        if Bullet.ice_arrow_image == None:
            Bullet.ice_arrow_image = load_image('arrow\\ice_arrow.png')


        if Bullet.fire_explosion_image == None:
            Bullet.fire_explosion_image = load_image('arrow\\fire_arrow_effect.png')
        if Bullet.ice_explosion_image == None:
            Bullet.ice_explosion_image = load_image('arrow\\ice_arrow_effect.png')
        self.x, self.y, self.velocity, self.degreeAT = x, y, velocity, degreeAT
        self.move_x, self.move_y = self.velocity * math.cos(self.degreeAT+3.141592), self.velocity * math.sin(self.degreeAT+3.141592)
        self.move_per_pixel_x, self.move_per_pixel_y = math.cos(self.degreeAT+3.141592),  math.sin(self.degreeAT+3.141592)
        self.data = data
        self.frame = 0
        self.effect_frame = 0
        self.timer = 0
        self.explosion = False
        self.shoot_time = 0
        self.start_time = time.time()*10

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def explosion_range(self):
        if self.data == 'arrow' or self.data == 'sector_form_arrow':
            return self.x - 20, self.y - 10, self.x + 20, self.y + 10
        else:
            return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def draw(self):
        if not self.explosion:
            if self.data == 'fire_arrow' or self.data == 'sector_form_fire_arrow':
                self.fire_arrow_image.clip_composite_draw(int(self.frame) * 90, 0, 90, 30, self.degreeAT, '',self.x, self.y, 90, 30)
            elif self.data == 'ice_arrow'or self.data == 'sector_form_ice_arrow':
                self.ice_arrow_image.clip_composite_draw(int(self.frame) * 90, 0, 90, 30, self.degreeAT, '',self.x, self.y, 90, 30)
            elif self.data == 'arrow':
                self.arrow_image.rotate_draw(self.degreeAT + 3.141592, self.x, self.y)
            elif self.data == 'sector_form_arrow':
                self.arrow_image.rotate_draw(self.degreeAT + 3.141592, self.x, self.y)
        else:
            if self.data == 'fire_arrow' or self.data == 'sector_form_fire_arrow':
                self.fire_explosion_image.clip_composite_draw(int(self.effect_frame) * 70, 0, 70, 70,
                                                              self.degreeAT, '', self.x, self.y, 70, 70)
            elif self.data == 'ice_arrow'or self.data == 'sector_form_ice_arrow':
                self.ice_explosion_image.clip_composite_draw(int(self.effect_frame) * 45, 0, 45, 30,
                                                             self.degreeAT, '', self.x, self.y, 70, 70)
            elif self.data == 'arrow':
                self.arrow_image.rotate_draw(self.degreeAT + 3.141592, self.x, self.y)



    def update(self):
        # 화살은 시간이 지날 수록 점점 느려 진다
        if not self.explosion:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
            self.shoot_time = time.time()*10 - self.start_time
            if self.shoot_time == 0:
                self.shoot_time = 1

            self.timer += game_framework.frame_time

            if self.timer > 0.01:
                self.timer = 0
                self.move_x -= (self.move_per_pixel_x * self.shoot_time**2)
                self.move_y -= (self.move_per_pixel_y * self.shoot_time**2)

            self.x += self.move_x * game_framework.frame_time
            self.y += self.move_y * game_framework.frame_time
            if self.x < 25 or self.x > 1600 - 25:
                game_world.remove_object(self)

            if self.move_per_pixel_x > 0 and self.move_x < 0:
                game_world.remove_object(self)
            elif self.move_per_pixel_x < 0 and self.move_x > 0:
                game_world.remove_object(self)
        else:
            if self.data == 'arrow':
                game_world.remove_object(self)
            self.effect_frame = (self.effect_frame+EFFECT_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
            if int(self.effect_frame) >= 6:
                game_world.remove_object(self)
