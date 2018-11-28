from pico2d import *
import game_framework
import time
from bullet import Bullet

import game_world
import math

# Boy Event

RIGHT_BUTTON_DOWN, LEFT_BUTTON_DOWN, RIGHT_BUTTON_UP, LEFT_BUTTON_UP, TMP = range(5)

key_event_table = {
    (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_RIGHT): RIGHT_BUTTON_DOWN,
    (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT): LEFT_BUTTON_DOWN,
    (SDL_MOUSEBUTTONUP, SDL_BUTTON_RIGHT): RIGHT_BUTTON_UP,
    (SDL_MOUSEBUTTONUP, SDL_BUTTON_LEFT): LEFT_BUTTON_UP,
    (SDL_KEYDOWN, SDLK_SPACE): TMP,
}

PIXEL_PER_METER = (10 / 0.33)  # 30pixel -> 100cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
# 화살 속도 초당 20m
ARROW_SPEED_PPS = (20 * PIXEL_PER_METER)

# Boy States

class IdleState:
    @staticmethod
    def enter(boy, event):
        boy.t = 0
        boy.start_x, boy.start_y = boy.x, boy.y

        pass

    @staticmethod
    def exit(boy, event):
        # fill here
        if event == LEFT_BUTTON_UP:
            boy.fire_ball(boy.bullet_type, boy.click_time)
            boy.click_time = 0
        pass

    @staticmethod
    def do(boy):
        boy.degreeAT = math.atan2(boy.y - boy.view_mouse_y, boy.x - boy.view_mouse_x)


    @staticmethod
    def draw(boy):
        boy.image.rotate_draw(boy.degreeAT + 3.14, boy.x, boy.y)
        shoot_time = clamp(0, int(time.time() * 30 - boy.click_time), 70)
        if boy.click_time != 0:
            boy.font.draw(boy.x, boy.y + 20, ' %3d' % shoot_time, (shoot_time * 3, 0, 0))





class RunState:

    @staticmethod
    def enter(boy, event):
        boy.t = 0
        boy.start_x, boy.start_y = boy.x, boy.y
        boy.tile_x, boy.tile_y = int(boy.x) // 20 + 1, int(boy.y) // 20 + 1

        pass

    @staticmethod
    def exit(boy, event):
        boy.start_x, boy.start_y = boy.x, boy.y
        # fill her
        pass

    @staticmethod
    def do(boy):

        boy.degreeAT = math.atan2(boy.y - boy.view_mouse_y, boy.x - boy.view_mouse_x)
        boy.t += game_framework.frame_time
        a = boy.t / boy.total_moveRatio
        boy.x = (1 - a) * boy.start_x + a * boy.move_mouse_x
        boy.y = (1 - a) * boy.start_y + a * boy.move_mouse_y
        boy.tile_x, boy.tile_y = int(boy.x) // 20 + 1, int(boy.y) // 20 + 1
        if boy.Map[boy.tile_y][boy.tile_x] == 115 or boy.Map[boy.tile_y][boy.tile_x] == 114 or \
                boy.Map[boy.tile_y][boy.tile_x] == 109 or boy.Map[boy.tile_y][boy.tile_x] == 110 \
                or boy.t >= boy.total_moveRatio:
            boy.t -= game_framework.frame_time
            a = boy.t / boy.total_moveRatio
            boy.x = (1 - a) * boy.start_x + a * boy.move_mouse_x
            boy.y = (1 - a) * boy.start_y + a * boy.move_mouse_y
            boy.add_event(TMP)
            return
        elif boy.Map[boy.tile_y][boy.tile_x] == 31:
            boy.t -= game_framework.frame_time
            a = boy.t / boy.total_moveRatio
            boy.x = (1 - a) * boy.start_x + a * boy.move_mouse_x
            boy.y = (1 - a) * boy.start_y + a * boy.move_mouse_y
            boy.add_event(TMP)
            return

    @staticmethod
    def draw(boy):
        boy.image.rotate_draw(boy.degreeAT + 3.14, boy.x, boy.y)




class SleepState:
    # fill here
    @staticmethod
    def enter(boy, event):
        boy.frame = 0

    @staticmethod
    def exit(boy, event):

        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        boy.image.rotate_draw(boy.degreeAT + 3.14, boy.x, boy.y)
    pass





next_state_table = {

    IdleState: {RIGHT_BUTTON_UP: RunState, LEFT_BUTTON_UP: IdleState,
                RIGHT_BUTTON_DOWN: RunState, LEFT_BUTTON_DOWN: IdleState,
                TMP: IdleState},

    RunState: {RIGHT_BUTTON_UP: RunState, RIGHT_BUTTON_DOWN: RunState,
               LEFT_BUTTON_DOWN: IdleState, LEFT_BUTTON_UP: IdleState,
               TMP: IdleState},

    SleepState: {LEFT_BUTTON_DOWN: RunState, RIGHT_BUTTON_DOWN: RunState,
                 LEFT_BUTTON_UP: RunState, RIGHT_BUTTON_UP: RunState,
                 TMP: IdleState}
                }




class Boy:

    def __init__(self):
        self.x, self.y = 1000 // 2, 300
        self.image = load_image('actor\\actorTop1.png')
        self.Map = None
        self.inventory = None
        self.velocity = 0
        self.frame = 0
        self.click_time = 0.0
        self.degreeAT = 0
        self.move_mouse_x = 0
        self.move_mouse_y = 0
        self.view_mouse_x = 0
        self.view_mouse_y = 0
        self.start_x = 0
        self.start_y = 0
        self.tile_x = 0
        self.tile_y = 0
        self.t = 0
        self.bullet_type = 'arrow'
        self.shoot_timer = time.time()

        self.font = load_font('font\\godoMaum.ttf', 50)
        self.total_moveRatio = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def fire_ball(self, data, speed):
        if time.time() - self.shoot_timer > 0.3 and self.inventory.pop(data):

            self.shoot_timer = time.time()
            ball = Bullet(self.x, self.y, ARROW_SPEED_PPS + speed * PIXEL_PER_METER, self.degreeAT, data)
            game_world.add_object(ball, 2)
        pass

    def add_event(self, event):
        self.event_que.insert(0, event)

    def Get_maptile(self, line):
        self.Map = line

    def Get_inven(self, inventory):
        self.inventory = inventory
        pass

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                self.click_time = time.time() * 30
            elif event.button == SDL_BUTTON_RIGHT:
                self.t = 0
                self.start_x, self.start_y = self.x, self.y
                self.move_mouse_x, self.move_mouse_y = event.x, 600 - event.y
                self.total_moveRatio = math.sqrt(((self.move_mouse_x - self.start_x) ** 2 +
                                                  (self.move_mouse_y - self.start_y) ** 2))/RUN_SPEED_PPS
                if self.move_mouse_x >= 800 and self.move_mouse_x <= 1000:
                    if self.move_mouse_y >= 550 and self.move_mouse_y <= 600:
                        self.bullet_type = 'fire_arrow'
                        return
                    elif self.move_mouse_y >= 500 and self.move_mouse_y <= 550:
                        self.bullet_type = 'ice_arrow'
                        return
                    elif self.move_mouse_y >= 450 and self.move_mouse_y <= 500:
                        self.bullet_type = 'arrow'
                        return
        if event.button == SDL_BUTTON_LEFT and event.type == SDL_MOUSEBUTTONUP:
            self.click_time = time.time() * 30 - self.click_time
            self.click_time = clamp(0, self.click_time, 70)

        if event.type == SDL_MOUSEMOTION:
            self.view_mouse_x, self.view_mouse_y = event.x, 600 - event.y

        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

        if (event.type, event.button) in key_event_table:
            key_event = key_event_table[(event.type, event.button)]
            self.add_event(key_event)

