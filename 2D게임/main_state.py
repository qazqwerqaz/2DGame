import random
import json
import os

from pico2d import *

import game_framework
import title_state
import pause_state
import numpy as np
import math

name = "MainState"

boy = None
boy1 = None
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
        self.x, self.y = 500, 300
        self.frame = 0
        self.image = load_image('actorTop.png')
        self.move = 0
        self.moveRatio = 0
        self.total_moveRatio = 1
        self.start_x = 0
        self.start_y = 0
        self.mouse_x = 0
        self.mouse_y = 0
        self.degreeAT = 0

    def update(self):
        if self.moveRatio <= self.total_moveRatio:
            self.moveRatio += 1
            t = self.moveRatio / self.total_moveRatio
            self.x = (1-t)*self.start_x + t*self.mouse_x
            self.y = (1-t)*self.start_y + t*self.mouse_y

    def draw(self):
        self.image.rotate_draw(self.degreeAT ,self.x, self.y)


def enter():
    global boy, boy1, grass
    boy = Boy()
    boy1 = Boy()
    grass = Grass()


def exit():
    global boy, boy1, grass
    del(boy)
    del(boy1)
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
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_p:
                game_framework.push_state(pause_state)
            elif event.key == SDLK_1:
                boy.move = 1
                boy1.move = 0
            elif event.key == SDLK_2:
                boy.move = 0
                boy1.move = 1
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_RIGHT:
                if boy.move == 0:
                    boy.mouse_x, boy.mouse_y = event.x, 600 - event.y
                    boy.start_x, boy.start_y = boy.x, boy.y
                    boy.total_moveRatio = math.sqrt((( boy.mouse_x - boy.start_x) ** 2 + (boy.mouse_y - boy.start_y) ** 2))
                    boy.moveRatio = 0
                elif boy1.move == 0:
                    boy1.mouse_x, boy1.mouse_y = event.x, 600 - event.y
                    boy1.start_x, boy1.start_y = boy1.x, boy1.y
                    boy1.total_moveRatio = math.sqrt(((boy1.mouse_x - boy1.start_x) ** 2 + (boy1.mouse_y - boy1.start_y) ** 2))
                    boy1.moveRatio = 0
        elif event.type == SDL_MOUSEMOTION:
            if boy.move == 0:
                boy.degreeAT = math.atan2(600 - event.y - boy.y, event.x - boy.x)
            elif boy1.move == 0:
                boy1.degreeAT = math.atan2(600 - event.y - boy1.y, event.x - boy1.x)
    pass



def update():
    boy.update()
    boy1.update()
    pass


def draw():
    clear_canvas()
    grass.draw()
    boy.draw()
    boy1.draw()
    update_canvas()
    pass





