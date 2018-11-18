import random

import game_framework
import game_world
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from pico2d import *

# Boy Event
FIRE_ATTACK, ICE_ATTACK, ARROW_ATTACK, IDLE = range(4)

key_event_table = {
    (True, 'fire_arrow'): FIRE_ATTACK,
    (True, 'ice_arrow'): ICE_ATTACK,
    (True, 'arrow'): ARROW_ATTACK,
    (False, 'a'): IDLE,
}

PIXEL_PER_METER = (10 / 0.33)  # 30pixel -> 100cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


class RunState:

    @staticmethod
    def enter(Slime):
       pass

    @staticmethod
    def exit(Slime):
        pass

    @staticmethod
    def do(Slime):
        Slime.x += RUN_SPEED_PPS * game_framework.frame_time
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
        Slime.timer = 0
        pass

    @staticmethod
    def exit(Slime):

        pass

    @staticmethod
    def do(Slime):
        Slime.timer += game_framework.frame_time
        back_move_ratio = Slime.timer / game_framework.frame_time
        Slime.x += Slime.arrow_speed_x / back_move_ratio * game_framework.frame_time
        Slime.y += Slime.arrow_speed_y / back_move_ratio * game_framework.frame_time
        if Slime.timer >= 0.2:
            Slime.add_event(IDLE)
        pass

    @staticmethod
    def draw(Slime):
        Slime.image.rotate_draw(0, Slime.x, Slime.y)
        pass


class Ice_Attacked_State:

    @staticmethod
    def enter(Slime):
        Slime.timer = 0
        pass

    @staticmethod
    def exit(Slime):

        pass

    @staticmethod
    def do(Slime):
        Slime.timer += game_framework.frame_time
        if Slime.timer >= 0.2:
            Slime.add_event(IDLE)
        pass

    @staticmethod
    def draw(Slime):
        Slime.image.rotate_draw(0, Slime.x, Slime.y)
        pass


class Attacked_State:

    @staticmethod
    def enter(Slime):
        Slime.timer = 0
        pass

    @staticmethod
    def exit(Slime):
        pass

    @staticmethod
    def do(Slime):
        # 약한화살에 맞으면 조금 밀려가고 강한화살에 맞으면 멀리 밀려간다
        Slime.timer += game_framework.frame_time
        back_move_ratio = Slime.timer / game_framework.frame_time
        Slime.x += Slime.arrow_speed_x/back_move_ratio * game_framework.frame_time
        Slime.y += Slime.arrow_speed_y/back_move_ratio * game_framework.frame_time
        if Slime.timer >= 0.2:
            Slime.add_event(IDLE)
        pass

    @staticmethod
    def draw(Slime):
        Slime.image.rotate_draw(0, Slime.x, Slime.y)
        pass


next_state_table = {
    RunState: {FIRE_ATTACK: Fire_Attacked_State, ICE_ATTACK: Ice_Attacked_State,
               ARROW_ATTACK: Attacked_State, IDLE: RunState},
    Fire_Attacked_State: {FIRE_ATTACK: Fire_Attacked_State, ICE_ATTACK: Ice_Attacked_State,
                          ARROW_ATTACK: Attacked_State, IDLE: RunState},
    Ice_Attacked_State: {FIRE_ATTACK: Fire_Attacked_State, ICE_ATTACK: Ice_Attacked_State,
                         ARROW_ATTACK: Attacked_State, IDLE: RunState},
    Attacked_State: {FIRE_ATTACK: Fire_Attacked_State, ICE_ATTACK: Ice_Attacked_State,
                     ARROW_ATTACK: Attacked_State, IDLE: RunState}
}


class Slime:

    image = None
    def __init__(self, hp, type):
        self.x, self.y = 0, random.randint(0, 600)
        if Slime.image == None:
            Slime.image = load_image('Monster1.png')
        self.HP = hp
        self.move_type = type
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.timer = 0
        self.arrow_speed_x = 0
        self.arrow_speed_y = 0
        self.In_Collide_Range = False
        self.event_que = []
        self.cur_state = RunState
        self.cur_state.enter(self)

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self)

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())

    def Attacked(self, data, arrow_speed_x, arrow_speed_y):
        self.arrow_speed_x = arrow_speed_x
        self.arrow_speed_y = arrow_speed_y
        if (self.In_Collide_Range, data) in key_event_table:
            key_event = key_event_table[(self.In_Collide_Range, data)]
            self.add_event(key_event)
        pass

