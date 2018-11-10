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

name = "MainState"

boy = None
boy1 = None
grass = None
Inventory = None
monsters = None
Boy_ID = 0
Monster_Spawn_time = 0

def enter():
    global boy, boy1, grass, Inventory
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
    global Monster_Spawn_time
    Monster_Spawn_time += game_framework.frame_time
    if Monster_Spawn_time >= 2:
        global monsters
        monsters = [Slime() for i in range(10)]
        game_world.add_objects(monsters, 1)
        Monster_Spawn_time = 0

    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()








