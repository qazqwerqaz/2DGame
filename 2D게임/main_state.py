import random
import json
import os

from pico2d import *

import game_framework
import title_state
import pause_state
import numpy as np

name = "MainState"

boy = None
grass = None
font = None


def draw_Map(image, map_x, map_y, Map_type):
    x, y = 0, 0
    type = Map_type
    while type >= 16:
        type = type - 16
        y += 1
    while type > 1:
        type = type - 1
        x += 1
    image.clip_draw(x * 20, y * 20, 20, 20, map_x * 20, map_y * 20)

class Grass:
    def __init__(self):
        self.image = load_image('Mdesert.png')
        self.Map = [[0]*41 for i in range(31)]
        with open('Map.txt', 'r') as self.file:
            self.line = np.loadtxt('Map.txt', delimiter=' ')
    def draw(self):
        map_x, map_y = 0, 0
        for i in self.line:
            for j in i:
                draw_Map(self.image, map_x, map_y, j)
                map_x = map_x + 1
            map_x = 0
            map_y = map_y +1




class Boy:
    def __init__(self):
        self.x, self.y = 0, 90
        self.frame = 0
        self.image = load_image('run_animation.png')
        self.dir = 1

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += self.dir
        if self.x >= 800:
            self.dir = -1
        elif self.x <= 0:
            self.dir = 1

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)


def enter():
    global boy, grass
    boy = Boy()
    grass = Grass()
    pass


def exit():
    global boy, grass
    del(boy)
    del(grass)
    pass


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.push_state(pause_state)
    pass


def update():
    boy.update()
    pass


def draw():
    clear_canvas()
    grass.draw()
    boy.draw()
    update_canvas()
    pass





