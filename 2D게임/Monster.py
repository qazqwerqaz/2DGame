import random

import math
import game_framework
import game_world
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from pico2d import *
import main_state
# Boy Event
FIRE_ATTACK, ICE_ATTACK, ARROW_ATTACK, IDLE, ATTACK = range(5)

key_event_table = {
    (True, 'fire_arrow'): FIRE_ATTACK,
    (True, 'ice_arrow'): ICE_ATTACK,
    (True, 'arrow'): ARROW_ATTACK,
    (False, 'a'): IDLE,
    (False, 'b'): ATTACK
}

PIXEL_PER_METER = (10 / 0.33)  # 30pixel -> 100cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


class RunState:

    @staticmethod
    def enter(Slime):
        Slime.timer = 0
        if Slime.HP <= 0:
            game_world.remove_object(Slime)
        if Slime.damage != 0:
            Slime.HP -= Slime.damage
            Slime.damage = 0

    @staticmethod
    def exit(Slime):

        pass

    @staticmethod
    def do(Slime):
        Slime.x += RUN_SPEED_PPS * math.cos(Slime.dir) * game_framework.frame_time
        Slime.y += RUN_SPEED_PPS * math.sin(Slime.dir) * game_framework.frame_time

        if Slime.x >= 420:
            Slime.x -= RUN_SPEED_PPS * math.cos(Slime.dir) * game_framework.frame_time
            Slime.add_event(ATTACK)

        if Slime.x < 0 or Slime.x > 1600 - 25:
            game_world.remove_object(Slime)
        pass

    @staticmethod
    def draw(Slime):
        Slime.image.rotate_draw(Slime.dir, Slime.x, Slime.y)
        pass


class Attack_State:

    @staticmethod
    def enter(Slime):
        pass

    @staticmethod
    def exit(Slime):
        pass

    @staticmethod
    def do(Slime):
        if Slime.charge:
            Slime.x += (RUN_SPEED_PPS * math.cos(Slime.dir) * game_framework.frame_time)*2
        else:
            Slime.x -= RUN_SPEED_PPS * math.cos(Slime.dir) * game_framework.frame_time
        if Slime.x >= 420:
            Slime.charge = False
        if Slime.x <= 380:
            Slime.charge = True

        pass

    @staticmethod
    def draw(Slime):
        Slime.image.rotate_draw(Slime.dir, Slime.x, Slime.y)
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
        Slime.timer += game_framework.frame_time
        back_move_ratio = Slime.timer / game_framework.frame_time
        Slime.x += (Slime.arrow_speed_x / back_move_ratio * game_framework.frame_time)
        Slime.y += (Slime.arrow_speed_y / back_move_ratio * game_framework.frame_time)
        if Slime.timer >= 0.2:
            Slime.add_event(IDLE)
        pass

    @staticmethod
    def draw(Slime):
        Slime.image.rotate_draw(Slime.dir, Slime.x, Slime.y)
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
        Slime.timer += game_framework.frame_time
        if Slime.timer >= 0.2:
            Slime.add_event(IDLE)
        pass

    @staticmethod
    def draw(Slime):
        Slime.image.rotate_draw(Slime.dir, Slime.x, Slime.y)
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
        Slime.x += (Slime.arrow_speed_x / back_move_ratio * game_framework.frame_time)
        Slime.y += (Slime.arrow_speed_y / back_move_ratio * game_framework.frame_time)
        if Slime.timer >= 0.2:
            Slime.add_event(IDLE)
        pass

    @staticmethod
    def draw(Slime):
        Slime.image.rotate_draw(0, Slime.x, Slime.y)
        pass


next_state_table = {
    RunState: {FIRE_ATTACK: Fire_Attacked_State, ICE_ATTACK: Ice_Attacked_State,
               ARROW_ATTACK: Attacked_State, IDLE: RunState, ATTACK: Attack_State},
    Fire_Attacked_State: {FIRE_ATTACK: Fire_Attacked_State, ICE_ATTACK: Ice_Attacked_State,
                          ARROW_ATTACK: Attacked_State, IDLE: RunState, ATTACK: RunState},
    Ice_Attacked_State: {FIRE_ATTACK: Fire_Attacked_State, ICE_ATTACK: Ice_Attacked_State,
                         ARROW_ATTACK: Attacked_State, IDLE: RunState, ATTACK: RunState},
    Attacked_State: {FIRE_ATTACK: Fire_Attacked_State, ICE_ATTACK: Ice_Attacked_State,
                     ARROW_ATTACK: Attacked_State, IDLE: RunState, ATTACK: RunState},
    Attack_State: {FIRE_ATTACK: Fire_Attacked_State, ICE_ATTACK: Ice_Attacked_State,
                     ARROW_ATTACK: Attacked_State, IDLE: RunState, ATTACK: Attack_State}
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
        self.dir_timer = 0
        self.arrow_speed_x = 0.0
        self.arrow_speed_y = 0.0
        self.damage = 0
        self.charge = False
        self.In_Collide_Range = False
        self.build_behavior_tree()
        self.event_que = []
        self.cur_state = RunState
        self.cur_state.enter(self)

    def wander(self):
        # fill here
        self.dir_timer -= game_framework.frame_time
        if self.dir_timer < 0:
            self.dir_timer += 1.0
            self.dir = random.random() * 2 * math.pi
        return BehaviorTree.SUCCESS

    def find_player(self):
        # fill here
        boy = main_state.get_boy()

        distance = (boy.x - self.x) ** 2 + (boy.y - self.y) ** 2
        if distance < (PIXEL_PER_METER * 10) ** 2:
            self.dir = math.atan2(boy.y - self.y, boy.x - self.x)
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to_player(self):
        # fill here
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        # fill here
        wander_node = LeafNode("Wander", self.wander)
        find_player_node = LeafNode("Find Player", self.find_player)
        move_to_player_node = LeafNode("Move to Player", self.move_to_player)
        chase_node = SequenceNode("Chase")
        chase_node.add_children(find_player_node, move_to_player_node)
        wander_chase_node = SelectorNode("WanderChase")
        wander_chase_node.add_children(chase_node, wander_node)
        self.bt = BehaviorTree(wander_chase_node)


    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.bt.run()
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
        self.arrow_speed_x = arrow_speed_x*2
        self.arrow_speed_y = arrow_speed_y*2
        self.damage = (arrow_speed_x**2 + arrow_speed_y**2)/1000
        if (self.In_Collide_Range, data) in key_event_table:
            key_event = key_event_table[(self.In_Collide_Range, data)]
            self.add_event(key_event)
        pass

