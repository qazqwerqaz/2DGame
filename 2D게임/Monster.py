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
    (False, ''): IDLE,

}


# Boy States


class RunState:

    @staticmethod
    def enter(Monster, event):
       pass

    @staticmethod
    def exit(Monster, event):
        pass

    @staticmethod
    def do(Monster):
        pass

    @staticmethod
    def draw(Monster):
        pass


class Fire_Attacked_State:

    @staticmethod
    def enter(Monster, event):
       pass

    @staticmethod
    def exit(Monster, event):
        pass

    @staticmethod
    def do(Monster):
        pass

    @staticmethod
    def draw(Monster):
        pass


class Ice_Attacked_State:

    @staticmethod
    def enter(Monster, event):
       pass

    @staticmethod
    def exit(Monster, event):
        pass

    @staticmethod
    def do(Monster):
        pass

    @staticmethod
    def draw(Monster):
        pass


class Attacked_State:

    @staticmethod
    def enter(Monster, event):
       pass

    @staticmethod
    def exit(Monster, event):
        pass

    @staticmethod
    def do(Monster):
        pass

    @staticmethod
    def draw(Monster):
        pass


next_state_table = {

    RunState: {FIRE_ATTACK: RunState, ICE_ATTACK: RunState, ARROW_ATTACK: RunState, IDLE: RunState}

}

class Monster:

    def __init__(self):
        self.x, self.y = 0, random.randint(0, 600)
        self.image = load_image('animation_sheet.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.timer = 0
        self.event_que = []
        self.cur_state = RunState
        self.cur_state.enter(self, None)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def draw(self):
        self.cur_state.draw(self)

    def Attacked(self):
        pass

