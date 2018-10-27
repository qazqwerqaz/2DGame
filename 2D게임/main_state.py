import random
import json
import os

from pico2d import *

import game_framework
import title_state
import pause_state
import math
import inventory
import Map
name = "MainState"

boy = None
boy1 = None
grass = None
font = None
inven = None
grass = None

RIGHT_BUTTON_DOWN, LEFT_BUTTON_DOWN, RIGHT_BUTTON_UP, LEFT_BUTTON_UP = range(4)
key_event_table = {
    (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_RIGHT): RIGHT_BUTTON_DOWN,
    (SDL_MOUSEBUTTONUP, SDL_BUTTON_RIGHT): LEFT_BUTTON_DOWN,
    (SDL_MOUSEBUTTONDOWN, SDLK_RIGHT): RIGHT_BUTTON_UP,
    (SDL_MOUSEBUTTONDOWN, SDLK_LEFT): LEFT_BUTTON_UP
}


class Boy:
    def __init__(self):
        self.x, self.y = 500, 300
        self.frame = 0
        self.image = load_image('actorTop.png')
        self.imageW = load_image('actorW.png')
        self.move = 0
        self.moveRatio = 0
        self.total_moveRatio = 1
        self.start_x = 0
        self.start_y = 0
        self.mouse_x = 0
        self.mouse_y = 0
        self.degreeAT = 0
        self.state = 0
    def update(self):
        if self.moveRatio <= self.total_moveRatio:
            self.moveRatio += 1
            self.state = 0
            t = self.moveRatio / self.total_moveRatio
            self.x = (1-t)*self.start_x + t*self.mouse_x
            self.y = (1-t)*self.start_y + t*self.mouse_y
            a = int(self.x) // 20 + 1
            b = int(self.y) // 20 + 1
            if grass.line[int(b)][int(a)] == 31:
                self.moveRatio -= 1
            elif grass.line[int(b)][int(a)] == 115 or grass.line[int(b)][int(a)] == 114:
                self.state = 1
                self.moveRatio -= 1
            elif grass.line[int(b)][int(a)] == 85:
                self.state = 2
                self.moveRatio -= 1

    def draw(self):
        self.image.rotate_draw(self.degreeAT, self.x, self.y)


def enter():
    global boy, boy1, grass, inven
    grass = Map.Grass()
    boy = Boy()
    boy1 = Boy()
    inven = inventory.Data()


def exit():
    global boy, boy1, grass
    del(boy)
    del(boy1)
    del(grass)


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
                    boy.total_moveRatio = math.sqrt((( boy.mouse_x - boy.start_x) ** 2 + (boy.mouse_y - boy.start_y) ** 2))/5
                    boy.moveRatio = 0
                elif boy1.move == 0:
                    boy1.mouse_x, boy1.mouse_y = event.x, 600 - event.y
                    boy1.start_x, boy1.start_y = boy1.x, boy1.y
                    boy1.total_moveRatio = math.sqrt(((boy1.mouse_x - boy1.start_x) ** 2 + (boy1.mouse_y - boy1.start_y) ** 2))/5
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
    inven.update()
    pass


def draw():
    clear_canvas()
    grass.draw()
    boy.draw()
    boy1.draw()
    inven.draw()
    update_canvas()
    pass





