import random
import json
import os

from pico2d import *
import game_framework
import game_world

from boy import Boy
from grass import Grass
from ball import Ball
from Inventory import inventory


name = "MainState"

boy = None
boy1 = None
grass = None
Inventory = None
move_boy = 0


def enter():
    global boy, boy1, grass, Inventory
    boy = Boy()
    boy1 = Boy()
    Inventory = inventory()
    grass = Grass()
    game_world.add_object(grass, 0)
    game_world.add_object(Inventory, 0)
    game_world.add_object(boy,1)
    game_world.add_object(boy1, 1)

def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    global move_boy
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_1:
                move_boy = 1
            elif event.key == SDLK_2:
                move_boy = 0
        else:
            if move_boy == 0:
                boy.handle_event(event)
            else:
                boy1.handle_event(event)
            Inventory.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()








