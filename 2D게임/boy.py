from pico2d import *
from ball import Ball

import game_world
import math
# Boy Event
RIGHT_BUTTON_DOWN, LEFT_BUTTON_DOWN, RIGHT_BUTTON_UP, LEFT_BUTTON_UP, SLEEP_TIMER, SPACE, SHIFT_DOWN, SHIFT_UP = range(8)

key_event_table = {
    (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_RIGHT): RIGHT_BUTTON_DOWN,
    (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT): LEFT_BUTTON_DOWN,
    (SDL_MOUSEBUTTONUP, SDLK_RIGHT): RIGHT_BUTTON_UP,
    (SDL_MOUSEBUTTONUP, SDLK_LEFT): LEFT_BUTTON_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_LSHIFT): SHIFT_DOWN,
    (SDL_KEYUP, SDLK_LSHIFT): SHIFT_UP,
    (SDL_KEYDOWN, SDLK_RSHIFT): SHIFT_DOWN,
    (SDL_KEYUP, SDLK_RSHIFT): SHIFT_UP
}


# Boy States


class IdleState:

    @staticmethod
    def enter(boy, event):
        boy.t = 0
        pass

    @staticmethod
    def exit(boy, event):
        # fill here
        if event == SPACE:
            boy.fire_ball()
        pass

    @staticmethod
    def do(boy):
        boy.degreeAT = math.atan2(boy.y - boy.mouse_y, boy.x - boy.mouse_x)

    @staticmethod
    def draw(boy):
        boy.image.rotate_draw(boy.degreeAT + 3.14, boy.x, boy.y)


class RunState:

    @staticmethod
    def enter(boy, event):

        pass

    @staticmethod
    def exit(boy, event):
        # fill here
        if event == SPACE:
            boy.fire_ball()
        pass

    @staticmethod
    def do(boy):
        boy.t += 1
        boy.x = (1 - boy.t) * boy.start_x + boy.t * boy.mouse_x
        boy.y = (1 - boy.t) * boy.start_y + boy.t * boy.mouse_y
        if boy.t == 50:
            boy.add_event(RIGHT_BUTTON_UP)

    @staticmethod
    def draw(boy):
        boy.image.rotate_draw(boy.degreeAT + 3.14, boy.x, boy.y)


class DashState:

    @staticmethod
    def enter(boy, event):
        boy.timer = 30
        pass

    @staticmethod
    def exit(boy, event):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 2) % 8
        boy.timer -= 1
        boy.x += boy.velocity
        boy.x += boy.velocity * 10
        boy.x = clamp(25, boy.x, 1600 - 25)
        if boy.timer <= 0:
            boy.add_event(SHIFT_UP)

    @staticmethod
    def draw(boy):
        if boy.velocity == 1:
            boy.image.clip_draw(boy.frame * 100, 100, 100, 100, boy.x, boy.y)
        else:
            boy.image.clip_draw(boy.frame * 100, 0, 100, 100, boy.x, boy.y)


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
        if boy.dir == 1:
            boy.image.clip_composite_draw(boy.frame * 100, 300, 100, 100,
                                          3.141592 / 2, '', boy.x - 25, boy.y - 25, 100, 100)
        else:
            boy.image.clip_composite_draw(boy.frame * 100, 200, 100, 100,
                                          -3.141592 / 2, '', boy.x + 25, boy.y - 25, 100, 100)
    pass





next_state_table = {
    IdleState: {RIGHT_BUTTON_UP: RunState, LEFT_BUTTON_UP: RunState,
                RIGHT_BUTTON_DOWN: RunState, LEFT_BUTTON_DOWN: RunState,
                SLEEP_TIMER: SleepState, SPACE: IdleState,
                SHIFT_DOWN: IdleState, SHIFT_UP: IdleState},
    RunState: {RIGHT_BUTTON_UP: RunState, LEFT_BUTTON_UP: RunState,
               LEFT_BUTTON_DOWN: RunState, RIGHT_BUTTON_DOWN: RunState,
               SPACE: RunState, SHIFT_DOWN: DashState,  SHIFT_UP: RunState},
    SleepState: {LEFT_BUTTON_DOWN: RunState, RIGHT_BUTTON_DOWN: RunState,
                 LEFT_BUTTON_UP: RunState, RIGHT_BUTTON_UP: RunState,
                 SPACE: IdleState, SHIFT_DOWN: IdleState,  SHIFT_UP: IdleState},

    DashState: {SHIFT_DOWN: DashState,  SHIFT_UP: RunState,
                RIGHT_BUTTON_UP:IdleState, LEFT_BUTTON_UP: IdleState,
                RIGHT_BUTTON_DOWN: IdleState, LEFT_BUTTON_DOWN: IdleState,
                }
}

class Boy:

    def __init__(self):
        self.x, self.y = 1600 // 2, 90
        self.image = load_image('actorTop.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.timer = 0
        self.degreeAT = 0
        self.mouse_x = 0
        self.mouse_y = 0
        self.start_x = 0
        self.start_y = 0
        self.t = 0;
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)


    def fire_ball(self):
        # fill here
        ball = Ball(self.x, self.y, self.dir*3)
        game_world.add_object(ball,1)
        pass



    def add_event(self, event):
        self.event_que.insert(0, event)

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
        if event.type == SDL_MOUSEMOTION or event.type == SDL_MOUSEBUTTONUP:
            self.mouse_x, self.mouse_y = event.x, 600 - event.y
        elif event.type == SDL_MOUSEBUTTONDOWN:
            self.start_x, self.start_y = self.x, self.y

        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

