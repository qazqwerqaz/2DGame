from pico2d import *

import random
import game_world
import game_framework

# Boy Event
FIRE_ATTACK, ICE_ATTACK, ARROW_ATTACK, IDLE = range(4)

key_event_table = {
    (True, 'fire_arrow'): FIRE_ATTACK,
    (True, 'ice_arrow'): ICE_ATTACK,
    (True, 'arrow'): ARROW_ATTACK,
    (False, 'a'): IDLE,
}


# Boy States


class RunState:

    @staticmethod
    def enter(Slime):
       pass

    @staticmethod
    def exit(Slime):
        pass

    @staticmethod
    def do(Slime):
        Slime.x += 1
        if Slime.x < 0 or Slime.x > 1600 - 25:
            game_world.remove_object(Slime)
        pass

    @staticmethod
    def draw(Slime):
        Slime.image.rotate_draw(0, Slime.x, Slime.y)
        pass


class Fire_Attacked_State:

    @staticmethod
    def enter(Slime):
       pass

    @staticmethod
    def exit(Slime):
        pass

    @staticmethod
    def do(Slime):
        pass

    @staticmethod
    def draw(Slime):
        pass


class Ice_Attacked_State:

    @staticmethod
    def enter(Slime):
       pass

    @staticmethod
    def exit(Slime):
        pass

    @staticmethod
    def do(Slime):
        pass

    @staticmethod
    def draw(Slime):
        pass


class Attacked_State:

    @staticmethod
    def enter(Slime):
       pass

    @staticmethod
    def exit(Slime):
        pass

    @staticmethod
    def do(Slime):
        pass

    @staticmethod
    def draw(Slime):
        pass


next_state_table = {

    RunState: {FIRE_ATTACK: RunState, ICE_ATTACK: RunState, ARROW_ATTACK: RunState, IDLE: RunState}

}

class Slime:

    def __init__(self):
        self.x, self.y = 0, random.randint(0, 600)
        self.image = load_image('Monster1.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.timer = 0
        self.collide_event = False
        self.data = 'a'
        self.event_que = []
        self.cur_state = RunState
        self.cur_state.enter(self)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self)
            self.cur_state = next_state_table[self.cur_state][IDLE]
            self.cur_state.enter(self)
        if (self.collide_event, self.data) in key_event_table:
            key_event = key_event_table[(self.collide_event, self.data)]
            self.add_event(key_event)

    def draw(self):
        self.cur_state.draw(self)

    def Attacked(self):
        pass

