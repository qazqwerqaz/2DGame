import random
import json
import os
import time

from pico2d import *
import game_framework
import game_world

from boy import Boy
from grass import Grass
from Inventory import inventory
from Monster import Slime
from bullet import Bullet
name = "MainState"

boy = None
boy1 = None
grass = None
Inventory = None
monsters = None

bullet = None
monster_corps = []

Boy_ID = 0
Monster_Spawn_time = 0

SlimeHp = 100

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def In_Collide_Range(a, b):
    left_a, bottom_a, right_a, top_a = a.explosion_range()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def enter():
    global boy, boy1, grass, Inventory, bullet
    bullet = Bullet()
    boy = Boy()
    boy1 = Boy()

    Inventory = inventory()
    grass = Grass()
    boy.Get_maptile(grass.line)
    boy1.Get_maptile(grass.line)
    boy.Get_inven(Inventory)
    boy1.Get_inven(Inventory)
    game_world.add_object(grass, 0)
    game_world.add_object(Inventory, 0)
    game_world.add_object(boy, 1)
    game_world.add_object(boy1, 1)

    global Monster


def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    global Boy_ID
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_1:
                Boy_ID = 1
            elif event.key == SDLK_2:
                Boy_ID = 0
        else:
            if Boy_ID == 0:
                boy.handle_event(event)
            else:
                boy1.handle_event(event)
            Inventory.handle_event(event)


def update():
    global Monster_Spawn_time, monster_corps

    Monster_Spawn_time += game_framework.frame_time
    if Monster_Spawn_time >= 2:
        global monsters, SlimeHp
        SlimeHp += 10
        monsters = [Slime(random.randint(SlimeHp - 50, SlimeHp + 50), random.randint(0, 3)) for i in range(10)]
        game_world.add_objects(monsters, 3)
        Monster_Spawn_time = 0
        monster_corps += monsters

    for game_object in game_world.all_objects():
        game_object.update()

    bullets = game_world.Return_layer2_obj()

    if len(bullets) != 0:
        for monster in monster_corps:
            for bullet in bullets:
                if In_Collide_Range(bullet, monster):
                    monster.In_Collide_Range = True
                else:
                    monster.In_Collide_Range = False

        for monster in monster_corps:
            for bullet in bullets:
                if collide(bullet, monster):
                    for monster in monster_corps:
                        if monster.In_Collide_Range == True:
                            monster.Attacked(bullet.data, bullet.move_x, bullet.move_y)
                            bullet.explosion = True





def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()


def get_boy():
    if Boy_ID == 0:
        return boy
    else:
        return boy1








